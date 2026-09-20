# Publication Tables Plan

**Target Tables:** Summary of Audited Datasets and Cross-Validated Model Benchmarks

---

## Table 1: Summary of Audited Spaceflight Pharmaceutical Datasets
* **Contents:** Flight mission (ISS/Shuttle), duration (days in microgravity), dosimetry (cumulative radiation dose in mGy), formulations evaluated, and ground-matched controls.
* **Source:** Synthesized from `docs/04_DATASET_INVENTORY.md`.

---

## Table 2: Benchmark Model Performance Across Grouped Cross-Validation
* **Contents:** Model architectures (Linear baselines, Random Forest, XGBoost, LightGBM, SVR, Symbolic Regression), with test RMSE, MAE, and $R^2$ along with empirical 95% bootstrap confidence intervals $[CI_{\text{lower}}, CI_{\text{upper}}]$.
* **Source:** Extracted from `results/tables/` and `docs/08_RESULTS.md`.

---

## Table 3: Parsimonious Discovered Mathematical Equations
* **Contents:** Candidate symbolic regression closed-form equations $S_{\text{space}} = f(\dots)$, Pareto complexity scores, and goodness-of-fit metrics.
* **Source:** Extracted from `results/formulas/`.
