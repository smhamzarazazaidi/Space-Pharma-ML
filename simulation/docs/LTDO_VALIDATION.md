# Leave-two-drugs-out validation

All 28 API pairs were evaluated on both fixed engines, fitting six APIs per fold. There are 224 repeated lot predictions per engine. No test API enters scaling, fitting, bootstrap draws or residual estimation. See phase_d_fold_metrics.csv and ltdo_validation.csv.

| Engine | Pooled R2 | RMSE | MAE | Median AE | Worst pair MAE |
|---|---:|---:|---:|---:|---:|
| A chemistry | -0.3126 | 5.1769 | 4.0030 | 2.9209 | 10.2096 |
| B chemistry + dose | -0.0157 | 4.5539 | 3.5840 | 2.7968 | 8.2023 |

Worst A pair: Diazepam + Naloxone, MAE 10.210 percentage points. Caffeine + Diazepam demonstration MAE 3.192. That pair was chosen for chemistry/formulation contrast before examining pair errors. A pooled interval coverage 97.3%, mean width 362.13; these intervals are approximate and uncalibrated. Repeated pair predictions are dependent; no independent-row significance test is used. This is a harder stress test with less training diversity, not an external validation cohort.
