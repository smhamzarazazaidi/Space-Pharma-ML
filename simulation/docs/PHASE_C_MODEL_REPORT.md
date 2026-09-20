# Phase C - Interpretable Pharmaceutical Stability Prediction Engine

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

Best interpretable candidate: OLS / FS-A_Chemistry_Core: LODO R2 0.363, RMSE 3.608%, MAE 2.771%.

Best predictive candidate: OLS / FS-A_Chemistry_Core: LODO R2 0.363, RMSE 3.608%, MAE 2.771%.

Uncertainty-aware GPR candidate: GPR / FS-A_Chemistry_Core: LODO R2 -0.182, RMSE 4.912%, MAE 3.422%.

The Phase B M4 benchmark was LODO R2 about 0.363, RMSE 3.608%, MAE 2.771%. Phase C can only claim an improvement where the strict LODO comparison table shows it. Training performance is reported alongside LODO performance to expose memorization.

## 7. Per-drug results and uncertainty

Every lot has a held-out prediction, absolute error, signed error, data-driven chemical-domain status, and a 95% grouped-bootstrap predictive interval. The interval resamples training APIs and adds residuals from inner held-API predictions. It is a predictive interval, not a confidence interval for the mean. With only eight APIs it is necessarily unstable and should be used as a warning bound, not a clinical guarantee.

## 8. Out-of-distribution detection

Chemical-domain status is based on standardized nearest-neighbor distance among API-level descriptor centroids. The in-domain/boundary cut points are the median and 95th percentile of leave-one-centroid-out nearest-neighbor distances in the fold training data. This makes the threshold empirical rather than arbitrary. Out-of-domain inputs should return a warning and should not support a decision-grade estimate.

## 9. Interaction and exposure results

Best chemistry-only: OLS / FS-A_Chemistry_Core: LODO R2 0.363, RMSE 3.608%, MAE 2.771%.

Best chemistry plus radiation: GradientBoosting / FS-D_Chemistry_Radiation: LODO R2 -0.076, RMSE 4.688%, MAE 3.283%.

Best chemistry plus formulation: GradientBoosting / FS-E_Chemistry_Formulation: LODO R2 -0.093, RMSE 4.725%, MAE 3.213%.

Best interaction variant: GradientBoosting / FS-F_Radiation_TPSA_Interaction: LODO R2 -0.037, RMSE 4.601%, MAE 3.179%.

These comparisons test prediction performance, not causality. If radiation or its interactions do not beat chemistry-only LODO error, the Phase B associations do not survive as reliable cross-API predictors in this dataset.

## 10. Duration versus radiation and rate target

Duration and cumulative dose were not interpreted independently in one additive OLS model due to collinearity. The rate-target diagnostic gives 0.013% per day MAE and R2 0.260; it is retained only as a diagnostic because dividing endpoint change by duration changes the estimand and can amplify short-duration noise.

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
