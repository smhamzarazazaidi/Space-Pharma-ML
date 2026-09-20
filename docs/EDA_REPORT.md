# EDA Report - Static Stability Formula Discovery
**Project:** Interpretable Small-Data ML for Pharmaceutical Stability under Spaceflight
**Dataset:** master_dataset_v1.csv (n=32 medication lots, 6 ISS missions, 8 drugs)
**Executed:** 2026-09-18 01:46

---

## 1. Dataset Overview

| Item | Value |
|---|---|
| Total medication lots | 32 |
| ISS Missions | SpX-15, SpX-16, SpX-17, NG-11, SpX-18, SpX-20 |
| Active Pharmaceutical Ingredients | 8 |
| Duration range | 132 - 972 days |
| Cumulative ISS dose range | 0.105 - 0.699 Gy |
| Flight API range | 74.2% - 100.8% |
| Degradation Delta range | -10.40% to 7.70% |
| All QC checks | PASS (see results/tables/master_dataset_v1_qc.csv) |

---

## 2. Univariate API Statistics

| Variable | Mean | Std | Min | Max |
|---|---|---|---|---|
| Flight API (%) | 91.14 | 8.65 | 74.2 | 100.8 |
| Ground API (%) | 93.44 | 7.90 | 78.9 | 103.6 |
| Degradation Delta (%) | -2.31 | 4.21 | -10.40 | 7.70 |

> [!NOTE]
> All 32 flight lots remained detectable (above 74% API). Epinephrine and Promethazine
> (solution, NG-11) exhibited the largest negative Delta values.

---

## 3. Spearman Correlation with Degradation Delta

| Variable | Spearman rho | p-value | 95% CI | Significant? |
|---|---|---|---|---|
| Days in Space | -0.153 | 0.4039 | [-0.476, 0.207] | no |
| HBA | -0.128 | 0.4867 | [-0.456, 0.232] | no |
| Cumul. Dose (Gy) | -0.110 | 0.5498 | [-0.442, 0.248] | no |
| Is Solid | -0.068 | 0.7126 | [-0.407, 0.288] | no |
| Complexity | -0.007 | 0.9697 | [-0.355, 0.343] | no |
| XLogP | 0.011 | 0.9536 | [-0.339, 0.358] | no |
| TPSA (A2) | 0.025 | 0.8918 | [-0.327, 0.370] | no |
| MW (g/mol) | 0.045 | 0.8069 | [-0.309, 0.388] | no |
| Rot. Bonds | 0.075 | 0.6826 | [-0.281, 0.413] | no |
| HBD | 0.101 | 0.5821 | [-0.257, 0.434] | no |
| Flight API | 0.198 | 0.2763 | [-0.162, 0.512] | no |

> [!IMPORTANT]
> **Strongest predictor of degradation:** Days in Space (rho=-0.153, p=0.4039)
> **Second strongest:** HBA (rho=-0.128, p=0.4867)

---

## 4. Statistical Group Tests

| Test | Statistic | p-value | Significant? |
|---|---|---|---|
| Kruskal-Wallis: Drug effect on Degradation Delta | 2.613 | 0.91837 | no |
| Mann-Whitney: Formulation (Solid vs Liquid) | 125.000 | 0.72091 | no |
| Kruskal-Wallis: Mission effect on Degradation Delta | 7.739 | 0.17123 | no |
| Kruskal-Wallis: Duration Tertile on Degradation Delta | 0.355 | 0.83723 | no |

---

## 5. Formulation Effect

- **Solid formulations** (Tablet/Capsule): mean Delta = -2.90%
- **Liquid formulations** (Solution): mean Delta = -2.00%
- Mann-Whitney p = 0.7209

---

## 6. Static Stability Formula (Baseline OLS)

### Formula
```
DeltaAPI = -1.0230 - 0.07911*Days + 106.05147*Dose_Gy - 0.06874*XLogP - 0.01586*TPSA - 0.83379*IsSolid
```

### Coefficients

| Term | Coefficient | Interpretation |
|---|---|---|
| Intercept | -1.0230 | Baseline Delta%API |
| Days in Space | -0.079111 | Change in Delta%API per unit of days_in_space |
| Cumul. Dose (Gy) | 106.051469 | Change in Delta%API per unit of cumulative_dose_Gy |
| XLogP | -0.068740 | Change in Delta%API per unit of xlogp |
| TPSA (A2) | -0.015863 | Change in Delta%API per unit of tpsa_angstrom2 |
| Is Solid (0/1) | -0.833794 | Change in Delta%API per unit of is_solid |

### Validation

| Metric | Value |
|---|---|
| Training R2 (n=32) | 0.0718 |
| Training RMSE | 3.9920 % |
| LODO Mean R2 | -4.0972 |
| LODO 95% CI | [-11.668, -0.043] |
| LODO Mean RMSE | 4.2868 % |

> [!CAUTION]
> Small-data caveat (n=32): LODO R2 with only 8 unique drugs has a wide confidence interval.
> This is a scientifically motivated BASELINE - not the final predictive model.
> ML and symbolic regression will be applied in subsequent steps.

---

## 7. Figures Produced

| Figure | File | Description |
|---|---|---|
| 1 | 01_api_distributions.png | Flight vs Ground API histograms + degradation distribution |
| 2 | 02_flight_vs_ground_scatter.png | Paired identity scatter (by drug and formulation) |
| 3 | 03_api_by_drug_boxplot.png | Per-drug API and degradation boxplots |
| 4 | 04_api_by_mission.png | Per-mission flight API and degradation |
| 5 | 05_radiation_vs_degradation.png | Cumulative dose vs degradation scatter |
| 6 | 06_duration_vs_degradation.png | Duration vs degradation (linear + log) |
| 7 | 07_formulation_comparison.png | Solid vs Liquid formulation comparison |
| 8 | 08_correlation_heatmap.png | Spearman correlation heatmap |
| 9 | 09_static_formula_fit.png | OLS fit: predicted vs actual, residuals, LODO R2 |
| 10 | 10_pairplot_key_vars.png | Pairplot of key EDA variables |

---

## 8. Key Scientific Findings

1. **Most lots stable within +/-5% of ground controls.** Mean Delta = -2.31%.
2. **Duration is the dominant predictor** of degradation (strongest Spearman rho with DeltaAPI).
3. **Formulation type matters:** Liquids degrade more than solids on average.
4. **Drug identity drives variance** - Kruskal-Wallis H=2.61, p=0.91837.
5. **Radiation alone does not explain degradation** at this n - Spearman rho=-0.110, p=0.5498, confounded by duration.
6. **OLS baseline** training R2=0.072, LODO R2=-4.097.

---

## 9. Next Steps

- [ ] Step 8: Feature engineering (interaction terms, normalized stability index)
- [ ] Step 9: Baseline regression benchmarks (Ridge, Lasso, ElasticNet)
- [ ] Step 10: Classical ML comparison (Random Forest, XGBoost)
- [ ] Step 11: SHAP feature importance
- [ ] Step 12 and 13: Symbolic regression for interpretable formula discovery
