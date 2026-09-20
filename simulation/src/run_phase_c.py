"""Phase C: reproducible, nested leave-one-drug-out stability model evaluation."""
import json
import os
import sys
import warnings
from pathlib import Path

SIM_DIR = Path(__file__).resolve().parents[1]
DEPS = SIM_DIR / ".deps"
sys.path.insert(0, str(DEPS))
os.environ.setdefault("MPLCONFIGDIR", str(SIM_DIR / ".cache" / "matplotlib"))

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.base import clone
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern, RBF, WhiteKernel
from sklearn.inspection import permutation_importance
from sklearn.linear_model import ElasticNet, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, median_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
RANDOM_SEED = 20260920
RNG = np.random.default_rng(RANDOM_SEED)

DATA = SIM_DIR / "data" / "processed" / "master_dataset_v2_verified.csv"
SNAPSHOT = SIM_DIR / "data" / "processed" / "modeling_dataset_phase_c.csv"
VALIDATION = SIM_DIR / "data" / "processed" / "simulator_validation_cases.csv"
TABLES = SIM_DIR / "results" / "tables"
FIGURES = SIM_DIR / "results" / "figures" / "phase_c"
MODELS = SIM_DIR / "models"
DOCS = SIM_DIR / "docs"
for directory in (TABLES, FIGURES, MODELS, DOCS):
    directory.mkdir(parents=True, exist_ok=True)

FEATURE_SETS = {
    "FS-A_Chemistry_Core": ["tpsa", "xlogp", "molecular_weight"],
    "FS-B_Chemistry_Extended": ["tpsa", "xlogp", "rotatable_bonds"],
    "FS-C_Chemistry_Duration": ["tpsa", "xlogp", "rotatable_bonds", "days_in_space"],
    "FS-D_Chemistry_Radiation": ["tpsa", "xlogp", "rotatable_bonds", "cumulative_dose_combined_mGy"],
    "FS-E_Chemistry_Formulation": ["tpsa", "xlogp", "rotatable_bonds", "is_solid"],
    "FS-F_Radiation_TPSA_Interaction": ["tpsa", "xlogp", "rotatable_bonds", "cumulative_dose_combined_mGy", "radiation_x_tpsa"],
    "FS-G_Radiation_XLogP_Interaction": ["tpsa", "xlogp", "rotatable_bonds", "cumulative_dose_combined_mGy", "radiation_x_xlogp"],
    "FS-H_MeanRate_Duration": ["tpsa", "xlogp", "rotatable_bonds", "mean_dose_rate_uGy_h", "days_in_space"],
}

MODEL_SPECS = {
    "OLS": [{"label": "ordinary_least_squares"}],
    "Ridge": [{"alpha": a} for a in (0.1, 1.0, 10.0)],
    "ElasticNet": [{"alpha": a, "l1_ratio": l} for a in (0.05, 0.2) for l in (0.2, 0.8)],
    "PLS": [{"n_components": c} for c in (1, 2)],
    "RandomForest": [{"n_estimators": 50, "max_depth": d, "min_samples_leaf": 5, "max_features": "sqrt"}
                     for d in (1, 2)],
    "GradientBoosting": [{"n_estimators": n, "learning_rate": lr, "max_depth": 1, "min_samples_leaf": 5}
                         for n, lr in ((20, 0.05), (40, 0.05))],
    "GPR": [{"kernel": k, "length_scale": ls, "noise": noise}
            for k in ("RBF", "Matern") for ls in (0.75, 1.5) for noise in (0.3,)],
}

def make_model(name, params, n_features):
    if name == "OLS":
        return Pipeline([("scaler", StandardScaler()), ("model", LinearRegression())])
    if name == "Ridge":
        return Pipeline([("scaler", StandardScaler()), ("model", Ridge(alpha=params["alpha"]))])
    if name == "ElasticNet":
        return Pipeline([("scaler", StandardScaler()), ("model", ElasticNet(**params, max_iter=50000, random_state=RANDOM_SEED))])
    if name == "PLS":
        components = min(params["n_components"], n_features)
        return Pipeline([("scaler", StandardScaler()), ("model", PLSRegression(n_components=components, max_iter=1000))])
    if name == "RandomForest":
        return RandomForestRegressor(**params, random_state=RANDOM_SEED, n_jobs=1)
    if name == "GradientBoosting":
        return GradientBoostingRegressor(**params, random_state=RANDOM_SEED, loss="huber")
    if name == "GPR":
        base = RBF(params["length_scale"]) if params["kernel"] == "RBF" else Matern(params["length_scale"], nu=1.5)
        kernel = ConstantKernel(1.0, constant_value_bounds="fixed") * base + WhiteKernel(params["noise"], noise_level_bounds="fixed")
        return Pipeline([("scaler", StandardScaler()), ("model", GaussianProcessRegressor(kernel=kernel, optimizer=None, normalize_y=True, random_state=RANDOM_SEED))])
    raise ValueError(name)

def fit_predict(name, params, x_train, y_train, x_test, return_std=False):
    model = make_model(name, params, x_train.shape[1])
    model.fit(x_train, y_train)
    if name == "GPR" and return_std:
        scaler = model.named_steps["scaler"]
        mean, sd = model.named_steps["model"].predict(scaler.transform(x_test), return_std=True)
        return np.asarray(mean).ravel(), np.asarray(sd).ravel(), model
    prediction = np.asarray(model.predict(x_test)).ravel()
    return prediction, model

def metric_dict(y, p):
    return {
        "r2": r2_score(y, p),
        "rmse": float(np.sqrt(mean_squared_error(y, p))),
        "mae": float(mean_absolute_error(y, p)),
        "median_absolute_error": float(median_absolute_error(y, p)),
        "max_absolute_error": float(np.max(np.abs(np.asarray(y) - np.asarray(p)))),
    }

def parameter_text(params):
    return json.dumps(params, sort_keys=True)

def inner_select(name, x, y, groups):
    """Choose settings only with leave-one-API-out folds inside an outer training fold."""
    candidates = []
    unique = np.unique(groups)
    for params in MODEL_SPECS[name]:
        errors = []
        for api in unique:
            test = groups == api
            train = ~test
            try:
                pred, _ = fit_predict(name, params, x[train], y[train], x[test])
                errors.extend(np.abs(y[test] - pred).tolist())
            except Exception:
                errors = [np.inf]
                break
        candidates.append((float(np.mean(errors)), params))
    return min(candidates, key=lambda item: item[0])[1]

def nested_lodo(name, feature_set, frame):
    cols = FEATURE_SETS[feature_set]
    x = frame[cols].to_numpy(float)
    y = frame["delta_api_percent"].to_numpy(float)
    groups = frame["api"].to_numpy(str)
    records = []
    for held_api in np.unique(groups):
        test = groups == held_api
        train = ~test
        params = inner_select(name, x[train], y[train], groups[train])
        try:
            if name == "GPR":
                pred, sd, _ = fit_predict(name, params, x[train], y[train], x[test], return_std=True)
            else:
                pred, _ = fit_predict(name, params, x[train], y[train], x[test])
                sd = np.full(test.sum(), np.nan)
        except Exception:
            pred, sd = np.full(test.sum(), np.nan), np.full(test.sum(), np.nan)
        for idx, prediction, posterior_sd in zip(np.where(test)[0], pred, sd):
            records.append({
                "lot_id": frame.iloc[idx]["lot_id"], "api": held_api, "model_family": name,
                "feature_set": feature_set, "features": ", ".join(cols), "measured_delta_api_percent": y[idx],
                "lodo_predicted_delta_api_percent": prediction, "absolute_error_percent": abs(y[idx] - prediction),
                "signed_error_percent": prediction - y[idx], "gpr_posterior_sd": posterior_sd,
                "outer_fold_selected_hyperparameters": parameter_text(params),
            })
    pred_frame = pd.DataFrame(records)
    valid = pred_frame.dropna(subset=["lodo_predicted_delta_api_percent"])
    full_params = inner_select(name, x, y, groups)
    full_pred, full_model = fit_predict(name, full_params, x, y, x)
    metrics = metric_dict(valid["measured_delta_api_percent"], valid["lodo_predicted_delta_api_percent"])
    train_metrics = metric_dict(y, full_pred)
    return pred_frame, metrics, train_metrics, full_params, full_model

def diagnostic_tables(frame):
    diagnostics = ["cumulative_dose_combined_mGy", "days_in_space", "mean_dose_rate_uGy_h", "tpsa", "xlogp", "molecular_weight", "hba", "hbd", "rotatable_bonds", "heavy_atom_count", "complexity", "is_solid"]
    corr = frame[diagnostics].corr(method="pearson")
    rows = []
    for i, a in enumerate(diagnostics):
        for b in diagnostics[i + 1:]:
            rho, p = spearmanr(frame[a], frame[b])
            rows.append({"diagnostic_type": "pairwise_correlation", "feature": a, "comparison_feature": b,
                         "pearson_r": corr.loc[a, b], "spearman_rho": rho, "spearman_p_value": p,
                         "flag": "HIGH_REDUNDANCY" if abs(corr.loc[a, b]) >= 0.8 else ""})
    x = frame[diagnostics].astype(float).to_numpy()
    for i, feature in enumerate(diagnostics):
        try:
            others = np.delete(x, i, axis=1)
            fitted = LinearRegression().fit(others, x[:, i])
            r_squared = fitted.score(others, x[:, i])
            vif = np.inf if r_squared >= 0.999999 else 1.0 / (1.0 - r_squared)
        except Exception:
            vif = np.nan
        rows.append({"diagnostic_type": "vif", "feature": feature, "comparison_feature": "",
                     "pearson_r": np.nan, "spearman_rho": np.nan, "spearman_p_value": np.nan,
                     "vif": vif, "flag": "HIGH_VIF" if np.isfinite(vif) and vif >= 10 else ""})
    output = pd.DataFrame(rows)
    output.to_csv(TABLES / "phase_c_feature_diagnostics.csv", index=False)
    corr.to_csv(TABLES / "phase_c_feature_correlation_matrix.csv")
    plt.figure(figsize=(11, 9))
    plt.imshow(corr, vmin=-1, vmax=1, cmap="coolwarm")
    plt.colorbar(label="Pearson correlation")
    plt.xticks(range(len(diagnostics)), diagnostics, rotation=55, ha="right", fontsize=8)
    plt.yticks(range(len(diagnostics)), diagnostics, fontsize=8)
    plt.title("Phase C feature correlation matrix")
    plt.tight_layout(); plt.savefig(FIGURES / "feature_correlation_matrix.png", dpi=300); plt.close()
    return output

def bootstrap_intervals(name, feature_set, frame, predictions, n_boot=200):
    cols = FEATURE_SETS[feature_set]
    x = frame[cols].to_numpy(float); y = frame["delta_api_percent"].to_numpy(float); groups = frame["api"].to_numpy(str)
    rows = []
    for held_api in np.unique(groups):
        test = groups == held_api; train = ~test
        xtr, ytr, gtr = x[train], y[train], groups[train]
        params = inner_select(name, xtr, ytr, gtr)
        # Inner held-API residuals approximate irreducible lot-level error.
        residuals = []
        for inner_api in np.unique(gtr):
            itest = gtr == inner_api; itrain = ~itest
            try:
                pp, _ = fit_predict(name, params, xtr[itrain], ytr[itrain], xtr[itest])
                residuals.extend((ytr[itest] - pp).tolist())
            except Exception:
                pass
        if not residuals: residuals = [0.0]
        draws = [[] for _ in range(test.sum())]
        api_choices = np.unique(gtr)
        for _ in range(n_boot):
            sampled_apis = RNG.choice(api_choices, size=len(api_choices), replace=True)
            sample_idx = np.concatenate([np.where(gtr == api)[0] for api in sampled_apis])
            try:
                pp, _ = fit_predict(name, params, xtr[sample_idx], ytr[sample_idx], x[test])
                eps = RNG.choice(residuals, size=len(pp), replace=True)
                for j, value in enumerate(pp + eps): draws[j].append(value)
            except Exception:
                continue
        test_lots = frame.loc[test, "lot_id"].tolist()
        for lot, values in zip(test_lots, draws):
            if len(values) < 20: values = [predictions.loc[predictions.lot_id == lot, "lodo_predicted_delta_api_percent"].iloc[0]]
            rows.append({"lot_id": lot, "prediction_interval_lower_95": np.percentile(values, 2.5),
                         "prediction_interval_upper_95": np.percentile(values, 97.5),
                         "bootstrap_draws": len(values),
                         "interval_definition": "Grouped bootstrap predictive interval: resampled training APIs plus inner-LODO residual draw"})
    return pd.DataFrame(rows)

def domain_status(frame, feature_set, lot_id):
    cols = FEATURE_SETS[feature_set]; row = frame[frame.lot_id == lot_id].iloc[0]
    train = frame[frame.api != row.api]
    scaler = StandardScaler().fit(train[cols])
    train_api = train.groupby("api", as_index=False)[cols].mean()
    z_train = scaler.transform(train_api[cols]); z_test = scaler.transform(pd.DataFrame([row[cols].to_dict()]))[0]
    distances = np.sqrt(((z_train - z_test) ** 2).sum(axis=1))
    api_means = train_api[cols].to_numpy(float)
    nearest = []
    if len(api_means) > 1:
        for i in range(len(api_means)):
            others = np.delete(api_means, i, axis=0)
            zz = scaler.transform(pd.DataFrame(others, columns=cols))
            zi = scaler.transform(pd.DataFrame([api_means[i]], columns=cols))[0]
            nearest.append(float(np.min(np.sqrt(((zz - zi) ** 2).sum(axis=1)))))
    median_cut = float(np.median(nearest)); boundary_cut = float(np.percentile(nearest, 95))
    d = float(np.min(distances))
    status = "IN_DOMAIN" if d <= median_cut else ("NEAR_BOUNDARY" if d <= boundary_cut else "OUT_OF_DOMAIN")
    return d, median_cut, boundary_cut, status

def plot_outputs(pred, comparison, selected_id, selected_feature, uncertainty, frame):
    selected = pred[(pred.model_family == selected_id) & (pred.feature_set == selected_feature)].merge(uncertainty, on="lot_id")
    lo = min(selected.measured_delta_api_percent.min(), selected.lodo_predicted_delta_api_percent.min()) - 1
    hi = max(selected.measured_delta_api_percent.max(), selected.lodo_predicted_delta_api_percent.max()) + 1
    plt.figure(figsize=(7, 6)); plt.scatter(selected.measured_delta_api_percent, selected.lodo_predicted_delta_api_percent, c="#1f77b4")
    plt.plot([lo, hi], [lo, hi], "k--", lw=1); plt.xlim(lo, hi); plt.ylim(lo, hi)
    plt.xlabel("Measured delta API (%)"); plt.ylabel("LODO predicted delta API (%)"); plt.title(f"Measured vs held-out prediction: {selected_id} / {selected_feature}")
    plt.tight_layout(); plt.savefig(FIGURES / "measured_vs_lodo_predicted.png", dpi=300); plt.close()
    family = comparison.sort_values("lodo_mae_percent").groupby("model_family", as_index=False).first()
    for metric, filename, title in [("lodo_mae_percent", "model_comparison_mae.png", "Best LODO MAE by model family"), ("lodo_rmse_percent", "model_comparison_rmse.png", "Best LODO RMSE by model family")]:
        ordered = family.sort_values(metric); plt.figure(figsize=(9, 5)); plt.bar(ordered.model_family, ordered[metric], color="#4c78a8")
        plt.ylabel("Percent delta API"); plt.title(title); plt.xticks(rotation=30, ha="right"); plt.tight_layout(); plt.savefig(FIGURES / filename, dpi=300); plt.close()
    by_api = selected.groupby("api", as_index=False).absolute_error_percent.mean().sort_values("absolute_error_percent")
    plt.figure(figsize=(9, 5)); plt.bar(by_api.api, by_api.absolute_error_percent, color="#e45756"); plt.ylabel("Mean absolute held-out error (%)"); plt.title("Per-drug held-out prediction error")
    plt.xticks(rotation=30, ha="right"); plt.tight_layout(); plt.savefig(FIGURES / "per_drug_prediction_error.png", dpi=300); plt.close()
    residual = selected.lodo_predicted_delta_api_percent - selected.measured_delta_api_percent
    plt.figure(figsize=(7, 5)); plt.scatter(selected.lodo_predicted_delta_api_percent, residual, c="#54a24b"); plt.axhline(0, color="black", ls="--", lw=1)
    plt.xlabel("LODO predicted delta API (%)"); plt.ylabel("Residual: predicted - measured (%)"); plt.title("Held-out residual plot")
    plt.tight_layout(); plt.savefig(FIGURES / "residual_plot.png", dpi=300); plt.close()
    ordered = selected.sort_values("measured_delta_api_percent").reset_index(drop=True); x = np.arange(len(ordered))
    plt.figure(figsize=(12, 5)); plt.errorbar(x, ordered.lodo_predicted_delta_api_percent, yerr=[ordered.lodo_predicted_delta_api_percent-ordered.prediction_interval_lower_95, ordered.prediction_interval_upper_95-ordered.lodo_predicted_delta_api_percent], fmt="o", label="LODO prediction and 95% predictive interval")
    plt.scatter(x, ordered.measured_delta_api_percent, marker="x", c="black", label="Measured"); plt.xticks(x, ordered.lot_id, rotation=65, ha="right", fontsize=7); plt.ylabel("Delta API (%)"); plt.title("Held-out uncertainty intervals"); plt.legend(); plt.tight_layout(); plt.savefig(FIGURES / "uncertainty_interval_plot.png", dpi=300); plt.close()
    desc = ["tpsa", "xlogp", "molecular_weight", "rotatable_bonds"]
    z = StandardScaler().fit_transform(frame.groupby("api", as_index=False)[desc].mean()[desc]); _, _, vt = np.linalg.svd(z, full_matrices=False); pc = z @ vt[:2].T
    names = frame.groupby("api").first().index.tolist(); plt.figure(figsize=(7, 6)); plt.scatter(pc[:, 0], pc[:, 1], c="#7f7f7f")
    for xx, yy, name in zip(pc[:, 0], pc[:, 1], names): plt.text(xx, yy, name, fontsize=8)
    plt.xlabel("Descriptor PC1"); plt.ylabel("Descriptor PC2"); plt.title("Chemical descriptor domain: eight API centroids"); plt.tight_layout(); plt.savefig(FIGURES / "chemical_descriptor_domain.png", dpi=300); plt.close()
    train_vs = comparison.sort_values("lodo_mae_percent").groupby("model_family", as_index=False).first()
    plt.figure(figsize=(8, 6)); plt.scatter(train_vs.training_rmse_percent, train_vs.lodo_rmse_percent, s=75)
    for _, r in train_vs.iterrows(): plt.text(r.training_rmse_percent, r.lodo_rmse_percent, r.model_family, fontsize=8)
    plt.xlabel("Training RMSE (%)"); plt.ylabel("LODO RMSE (%)"); plt.title("Training versus held-out performance"); plt.tight_layout(); plt.savefig(FIGURES / "training_vs_lodo_performance.png", dpi=300); plt.close()

def sensitivity_plots(model_name, params, feature_set, frame):
    cols = FEATURE_SETS[feature_set]; x = frame[cols].copy(); med = x.median().to_frame().T
    fig, axes = plt.subplots(1, min(4, len(cols)), figsize=(15, 3.5)); axes = np.atleast_1d(axes)
    model_x = x.to_numpy(float); model_y = frame.delta_api_percent.to_numpy(float)
    for axis, feature in zip(axes, cols[:4]):
        grid = np.linspace(x[feature].quantile(.05), x[feature].quantile(.95), 80); pts = pd.concat([med] * len(grid), ignore_index=True); pts[feature] = grid
        p, _ = fit_predict(model_name, params, model_x, model_y, pts[cols].to_numpy(float)); axis.plot(grid, p, color="#1f77b4")
        axis.set_xlabel(feature); axis.set_ylabel("Predicted delta API (%)"); axis.set_title("Model response")
    fig.suptitle(f"Sensitivity curves: {model_name} / {feature_set}"); fig.tight_layout(); fig.savefig(FIGURES / "sensitivity_curves.png", dpi=300); plt.close(fig)

def write_docs(frame, comparison, selected, uncertainty, diagnostics, rate_metrics):
    best_interpretable = comparison[comparison.model_family.isin(["OLS", "Ridge", "ElasticNet", "PLS"])].sort_values("lodo_mae_percent").iloc[0]
    best_predictive = comparison.sort_values(["lodo_mae_percent", "lodo_rmse_percent"]).iloc[0]
    best_gpr = comparison[comparison.model_family == "GPR"].sort_values("lodo_mae_percent").iloc[0]
    interaction = comparison[comparison.feature_set.isin(["FS-F_Radiation_TPSA_Interaction", "FS-G_Radiation_XLogP_Interaction"])].sort_values("lodo_mae_percent")
    radiation = comparison[comparison.feature_set == "FS-D_Chemistry_Radiation"].sort_values("lodo_mae_percent").iloc[0]
    chemistry = comparison[comparison.feature_set == "FS-A_Chemistry_Core"].sort_values("lodo_mae_percent").iloc[0]
    formulation = comparison[comparison.feature_set == "FS-E_Chemistry_Formulation"].sort_values("lodo_mae_percent").iloc[0]
    def row_text(r): return f"{r.model_family} / {r.feature_set}: LODO R2 {r.lodo_r2:.3f}, RMSE {r.lodo_rmse_percent:.3f}%, MAE {r.lodo_mae_percent:.3f}%"
    report = f"""# Phase C - Interpretable Pharmaceutical Stability Prediction Engine

## 1. Objective

This phase evaluates conservative models for predicting endpoint `delta_api_percent` from 32 pharmaceutical lots representing eight unique APIs. It does not create the simulator UI or a vulnerability ranking.

## 2. Dataset and terminology

The locked snapshot is `data/processed/modeling_dataset_phase_c.csv`. The target is Delta API = ((Flight - Ground) / Ground) x 100. Stability Ratio is retained as 100 + Delta API. Molecular descriptors are drug-level values repeated across lots; the study therefore has eight chemically independent APIs, not 32 independent drugs.

## 3. Feature diagnostics

Feature correlations and VIF are in `results/tables/phase_c_feature_diagnostics.csv`. Cumulative radiation and duration remain highly collinear, so no primary feature set contains both as independent additive cumulative-exposure terms. TPSA/HBA and molecular-size descriptors were treated as alternatives rather than accumulated indiscriminately.

## 4. Feature sets and models

Eight small feature sets were predeclared: chemistry core, chemistry extended, chemistry plus duration, chemistry plus radiation, chemistry plus formulation, two radiation-interaction variants, and mean-rate plus duration. OLS, Ridge, Elastic Net, PLS, constrained Random Forest, constrained Gradient Boosting, and simple-kernel GPR were compared. Hyperparameters were selected inside every outer fold.

## 5. Nested LODO methodology

For each held API, all of its lots were withheld. Parameters, scalers, and feature transformations were fitted only using the remaining APIs. Pooled predictions are in `results/tables/phase_c_lodo_predictions.csv`. Random row splitting was not used.

## 6. Model comparison

Best interpretable candidate: {row_text(best_interpretable)}.

Best predictive candidate: {row_text(best_predictive)}.

Uncertainty-aware GPR candidate: {row_text(best_gpr)}.

The Phase B M4 benchmark was LODO R2 about 0.363, RMSE 3.608%, MAE 2.771%. Phase C can only claim an improvement where the strict LODO comparison table shows it. Training performance is reported alongside LODO performance to expose memorization.

## 7. Per-drug results and uncertainty

Every lot has a held-out prediction, absolute error, signed error, data-driven chemical-domain status, and a 95% grouped-bootstrap predictive interval. The interval resamples training APIs and adds residuals from inner held-API predictions. It is a predictive interval, not a confidence interval for the mean. With only eight APIs it is necessarily unstable and should be used as a warning bound, not a clinical guarantee.

## 8. Out-of-distribution detection

Chemical-domain status is based on standardized nearest-neighbor distance among API-level descriptor centroids. The in-domain/boundary cut points are the median and 95th percentile of leave-one-centroid-out nearest-neighbor distances in the fold training data. This makes the threshold empirical rather than arbitrary. Out-of-domain inputs should return a warning and should not support a decision-grade estimate.

## 9. Interaction and exposure results

Best chemistry-only: {row_text(chemistry)}.

Best chemistry plus radiation: {row_text(radiation)}.

Best chemistry plus formulation: {row_text(formulation)}.

Best interaction variant: {row_text(interaction.iloc[0])}.

These comparisons test prediction performance, not causality. If radiation or its interactions do not beat chemistry-only LODO error, the Phase B associations do not survive as reliable cross-API predictors in this dataset.

## 10. Duration versus radiation and rate target

Duration and cumulative dose were not interpreted independently in one additive OLS model due to collinearity. The rate-target diagnostic gives {rate_metrics['rate_lodo_mae']:.3f}% per day MAE and R2 {rate_metrics['rate_lodo_r2']:.3f}; it is retained only as a diagnostic because dividing endpoint change by duration changes the estimand and can amplify short-duration noise.

## 11. Sensitivity analysis

Sensitivity curves show model response to one feature at a time while other selected features remain at their medians. They are model responses, not experimental time-series measurements.

## 12. Candidate models

Candidate pipelines and metadata are saved under `simulation/models/`. Model cards describe the finalists. A deployment winner is not selected automatically.

## 13. Limitations and scientific interpretation

This is proof-of-concept cross-API generalization within the studied chemical domain. Radiation is a Columbus-module proxy, cabin telemetry remains secondary because of missingness, and the evidence cannot establish general clinical pharmaceutical stability in space. Pressure and oxygen are excluded. No causal environmental mechanism is established by coefficient or feature importance.

## 14. Recommendation

Use the best interpretable candidate as the provisional research reference, retain GPR as an uncertainty comparator, and require review of model cards and held-out error before any simulator attachment.

## Answers to the Phase C questions

1. Strict LODO, not training R2, decides whether any model beats M4. See the comparison table.
2. The lowest unseen-drug MAE/RMSE is the best predictive candidate stated above.
3. GPR supplies kernel-based posterior uncertainty; grouped-bootstrap predictive intervals are more directly relevant to new lot outcomes but unstable at eight APIs.
4. Radiation improves prediction only if its radiation feature-set LODO errors beat chemistry-only. The table provides that direct comparison.
5. Formulation improves generalization only if FS-E improves LODO metrics over chemistry-only.
6. Radiation by TPSA/XLogP interactions survive only if FS-F/FS-G improve held-out prediction; statistical significance in an in-sample regression is insufficient.
7. The evidence chiefly supports chemistry-driven cross-API signal; environmental claims remain limited by exposure collinearity and sparse cabin telemetry.
8. A new drug can receive a research-only estimate inside the observed domain, with an interval and domain warning.
9. An out-of-domain drug must receive an explicit warning, broad uncertainty, and no decision-grade interpretation.
10. Endpoint data do not identify a kinetic ODE curve without strong untestable assumptions.
11. Unconstrained symbolic regression is not justified with eight unique APIs.
12. Do not freeze a simulator engine automatically; use the provisional interpretable candidate only after review.

## Stop conditions

**READY FOR STABILITY ENGINE FREEZE: NO.** Eight APIs and unstable uncertainty are insufficient for a frozen engine.

**READY TO ATTACH MODEL TO SIMULATOR: NO.** Phase C produces candidate pipelines, not a validated dynamic simulator model.

**READY FOR NEW-DRUG PREDICTION: NO for decision use; YES for clearly labeled in-domain research dry runs only.**

**READY FOR VULNERABILITY RANKING: NO.** Ranking remains downstream of a validated, calibrated stability engine.
"""
    (DOCS / "PHASE_C_MODEL_REPORT.md").write_text(report, encoding="utf-8")
    ode = """# ODE and Kinetic Model Feasibility

## Finding

An ODE such as dS/dt = -kS is not identifiable from the current endpoint-only outcomes. A single endpoint per lot cannot separate initial condition, shape, and degradation rate without imposing a curve. Multiple mission lengths exist for some APIs, but there are too few repeated conditions and no within-mission potency time series to estimate API-specific k reliably.

An ODE would therefore add an assumed trajectory rather than directly measured dynamic information. Any first-order curve would be a model prediction, not an observed potency timeline. Validation against current data could only test endpoints, not intervening dynamics.

No kinetic model is implemented in Phase C. A future ODE requires repeated potency timepoints under measured dose-rate histories, formulation-aware kinetics, and external validation.
"""
    (DOCS / "ODE_FEASIBILITY.md").write_text(ode, encoding="utf-8")
    symbolic = """# Symbolic Regression Feasibility

There are 32 lots but only eight unique molecular entities. Unconstrained symbolic regression would search far more functional forms than the independent chemical sample size can support and would be highly prone to selection-induced overfitting.

Phase C does not run symbolic regression. A later restricted evaluation would need a tiny predeclared operator set, shallow expressions, a complexity penalty, and exclusive nested LODO assessment. A simple predeclared linear formula that generalizes is scientifically preferable to a more ornate expression selected from this dataset.
"""
    (DOCS / "SYMBOLIC_REGRESSION_FEASIBILITY.md").write_text(symbolic, encoding="utf-8")
    return best_interpretable, best_predictive, best_gpr

def main():
    frame = pd.read_csv(DATA)
    frame["radiation_x_tpsa"] = frame.cumulative_dose_combined_mGy * frame.tpsa
    frame["radiation_x_xlogp"] = frame.cumulative_dose_combined_mGy * frame.xlogp
    keep = ["lot_id", "api", "mission", "formulation", "formulation_class", "is_solid", "days_in_space", "iss_storage_days", "cumulative_dose_combined_mGy", "mean_dose_rate_uGy_h", "tpsa", "xlogp", "molecular_weight", "hba", "hbd", "rotatable_bonds", "heavy_atom_count", "complexity", "delta_api_percent", "stability_ratio_percent", "radiation_x_tpsa", "radiation_x_xlogp"]
    frame[keep].to_csv(SNAPSHOT, index=False)
    diagnostics = diagnostic_tables(frame)
    all_predictions, comparisons, fitted = [], [], {}
    for feature_set in FEATURE_SETS:
        for model_name in MODEL_SPECS:
            predictions, metrics, train_metrics, full_params, full_model = nested_lodo(model_name, feature_set, frame)
            all_predictions.append(predictions)
            comparisons.append({"model_family": model_name, "feature_set": feature_set, "features": ", ".join(FEATURE_SETS[feature_set]),
                                "hyperparameters_selected_on_full_group_cv": parameter_text(full_params),
                                "training_r2": train_metrics["r2"], "training_rmse_percent": train_metrics["rmse"], "training_mae_percent": train_metrics["mae"],
                                "lodo_r2": metrics["r2"], "lodo_rmse_percent": metrics["rmse"], "lodo_mae_percent": metrics["mae"],
                                "lodo_median_absolute_error_percent": metrics["median_absolute_error"], "lodo_max_absolute_error_percent": metrics["max_absolute_error"],
                                "complexity_note": "Small predeclared feature set; nested group tuning"})
            fitted[(model_name, feature_set)] = (full_params, full_model)
    pred = pd.concat(all_predictions, ignore_index=True); comparison = pd.DataFrame(comparisons)
    pred.to_csv(TABLES / "phase_c_lodo_predictions.csv", index=False); comparison.to_csv(TABLES / "phase_c_model_comparison.csv", index=False)
    # Rate target diagnostic: same chemistry core, different target, never substituted for the primary endpoint target.
    rate = frame.copy(); rate["delta_api_percent"] = rate.delta_api_percent / rate.days_in_space
    rate_pred, rate_m, _, _, _ = nested_lodo("OLS", "FS-A_Chemistry_Core", rate)
    rate_metrics = {"rate_lodo_mae": rate_m["mae"], "rate_lodo_r2": rate_m["r2"]}
    pd.DataFrame([{**rate_metrics, "target": "delta_api_percent / days_in_space", "interpretation": "Diagnostic only; primary target remains endpoint delta_api_percent"}]).to_csv(TABLES / "phase_c_rate_target_analysis.csv", index=False)
    best_interpretable, best_predictive, best_gpr = write_docs(frame, comparison, None, None, diagnostics, rate_metrics)
    # Provisional validation candidate: lowest-MAE constrained candidate; uncertainty is always added.
    chosen = best_predictive; model_name = chosen.model_family; feature_set = chosen.feature_set
    chosen_pred = pred[(pred.model_family == model_name) & (pred.feature_set == feature_set)].copy()
    uncertainty = bootstrap_intervals(model_name, feature_set, frame, chosen_pred)
    domain_rows = []
    for lot in frame.lot_id:
        distance, in_cut, boundary_cut, status = domain_status(frame, feature_set, lot)
        domain_rows.append({"lot_id": lot, "nearest_neighbor_distance": distance, "in_domain_cutoff": in_cut, "boundary_cutoff": boundary_cut, "domain_status": status})
    domain = pd.DataFrame(domain_rows); domain.to_csv(TABLES / "phase_c_domain_status.csv", index=False)
    chosen_pred = chosen_pred.merge(uncertainty, on="lot_id").merge(domain, on="lot_id")
    chosen_pred.to_csv(TABLES / "phase_c_selected_candidate_lodo_predictions.csv", index=False)
    validation = pd.read_csv(VALIDATION).drop(columns=[c for c in ["model_predicted_delta_api_pct", "model_prediction_lower_ci_95", "model_prediction_upper_ci_95", "prediction_error_pct"] if c in pd.read_csv(VALIDATION).columns])
    validation = validation.merge(chosen_pred[["lot_id", "lodo_predicted_delta_api_percent", "prediction_interval_lower_95", "prediction_interval_upper_95", "absolute_error_percent", "domain_status"]], on="lot_id", how="left")
    validation["model_predicted_delta_api_pct"] = validation.pop("lodo_predicted_delta_api_percent")
    validation["model_prediction_lower_ci_95"] = validation.pop("prediction_interval_lower_95")
    validation["model_prediction_upper_ci_95"] = validation.pop("prediction_interval_upper_95")
    validation["prediction_error_pct"] = validation.pop("absolute_error_percent")
    validation["domain_status"] = validation.pop("domain_status")
    validation["model_id"] = model_name + " / " + feature_set
    validation.to_csv(VALIDATION, index=False)
    # Save all model-family finalists with metadata and a full-data pipeline; these are candidates, not deployment models.
    for family in MODEL_SPECS:
        best = comparison[comparison.model_family == family].sort_values("lodo_mae_percent").iloc[0]
        params, pipeline = fitted[(family, best.feature_set)]
        prefix = family.lower().replace(" ", "_") + "_candidate"
        joblib.dump(pipeline, MODELS / f"{prefix}.joblib")
        (MODELS / f"{prefix}.json").write_text(json.dumps({"model_family": family, "feature_set": best.feature_set, "features": FEATURE_SETS[best.feature_set], "hyperparameters": params, "training_dataset": str(DATA.name), "target": "delta_api_percent", "validation": "nested leave-one-drug-out", "random_seed": RANDOM_SEED, "software": {"python": sys.version, "sklearn": __import__("sklearn").__version__}, "status": "candidate_only_not_deployed"}, indent=2), encoding="utf-8")
    # Model cards.
    for label, row, uncertainty_method in [("best_interpretable", best_interpretable, "grouped-bootstrap predictive interval"), ("best_predictive", best_predictive, "grouped-bootstrap predictive interval"), ("uncertainty_aware_gpr", best_gpr, "GPR posterior SD plus grouped-bootstrap comparison")]:
        worst = pred[(pred.model_family == row.model_family) & (pred.feature_set == row.feature_set)].groupby("api").absolute_error_percent.mean().idxmax()
        card = f"# Model Card: {label}\n\n- **Model:** {row.model_family}\n- **Purpose:** Candidate endpoint stability prediction\n- **Target:** delta_api_percent\n- **Features:** {row.features}\n- **Training data:** 32 lots, 8 unique APIs\n- **Validation:** Nested leave-one-drug-out\n- **LODO R2:** {row.lodo_r2:.3f}\n- **LODO MAE:** {row.lodo_mae_percent:.3f}%\n- **LODO RMSE:** {row.lodo_rmse_percent:.3f}%\n- **Worst held-out API:** {worst}\n- **Uncertainty:** {uncertainty_method}\n- **Allowed use:** Research-only within chemical domain with explicit interval and domain status.\n- **Disallowed interpretation:** Clinical decision support, causal environmental claims, or out-of-domain assurance.\n- **Out-of-domain behavior:** Return warning and no decision-grade interpretation.\n"
        (MODELS / f"model_card_{label}.md").write_text(card, encoding="utf-8")
    # Dry-run only; use selected model fit on full data and chemical domain based on full API centroids.
    params, _ = fitted[(model_name, feature_set)]; cols = FEATURE_SETS[feature_set]; med = frame[cols].median(); spread = frame[cols].std()
    dry = pd.DataFrame([med, med + 1.5 * spread, med + 4.0 * spread], index=["IN_DOMAIN_EXAMPLE", "NEAR_BOUNDARY_EXAMPLE", "OUT_OF_DOMAIN_EXAMPLE"]).reset_index(names="scenario")
    pp, _ = fit_predict(model_name, params, frame[cols].to_numpy(float), frame.delta_api_percent.to_numpy(float), dry[cols].to_numpy(float))
    centroid = frame.groupby("api", as_index=False)[cols].mean()
    domain_scaler = StandardScaler().fit(centroid[cols])
    z_centroid = domain_scaler.transform(centroid[cols])
    nearest = [float(np.min(np.sqrt(((np.delete(z_centroid, i, axis=0) - z_centroid[i]) ** 2).sum(axis=1)))) for i in range(len(z_centroid))]
    in_cut, boundary_cut = float(np.median(nearest)), float(np.percentile(nearest, 95))
    dry_distance = [float(np.min(np.sqrt(((z_centroid - z) ** 2).sum(axis=1)))) for z in domain_scaler.transform(dry[cols])]
    dry["nearest_neighbor_distance"] = dry_distance
    dry["domain_status"] = ["IN_DOMAIN" if d <= in_cut else ("NEAR_BOUNDARY" if d <= boundary_cut else "OUT_OF_DOMAIN") for d in dry_distance]
    dry["predicted_delta_api_percent"] = pp; dry["label"] = "SIMULATED MODEL PREDICTION - NOT EXPERIMENTAL DATA"; dry.to_csv(TABLES / "phase_c_new_drug_dry_run.csv", index=False)
    plot_outputs(pred, comparison, model_name, feature_set, uncertainty, frame)
    sensitivity_plots(model_name, params, feature_set, frame)
    print(json.dumps({"snapshot": str(SNAPSHOT), "model_rows": len(comparison), "prediction_rows": len(pred), "selected": {"model": model_name, "feature_set": feature_set}}, indent=2))

if __name__ == "__main__":
    main()
