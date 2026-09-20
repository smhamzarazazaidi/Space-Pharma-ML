# 07. Experimental Plan and Execution Checklist

**Project:** Interpretable Small-Data ML for Predicting Pharmaceutical Response and Stability Under Long-Duration Spaceflight Conditions
**Primary Reference:** docs/RESEARCH_DOCUMENT.md (Section 14)

---

## 17-Step Experimental Execution Plan

- [x] Step 1: Dataset Audit (Query NASA OSDR/ALSDA and literature)
- [x] Step 2: Dataset Selection (Filter by sample size, duration, controls)
- [x] Step 3: Data Download (Save unmodified files in data/raw/)
- [x] Step 4: Data Provenance Recording (Log checksums, URLs, DOIs)
- [x] Step 5: Data Cleaning and Standardization -> master_dataset_v1.csv (32 lots, all QC PASS)
- [x] Step 6: Exploratory Data Analysis -> docs/EDA_REPORT.md, 10 figures in results/figures/eda/
- [x] Step 7: Statistical Testing -> Spearman, Kruskal-Wallis, Mann-Whitney (saved in results/tables/)
- [ ] Step 8: Feature Engineering (master_dataset_v2.csv with interaction terms)
- [ ] Step 9: Baseline Modeling (Mean, Ridge, Lasso, ElasticNet -> results/metrics/)
- [ ] Step 10: Classical ML Comparison (Random Forest, XGBoost, LightGBM, SVR, k-NN -> models/)
- [ ] Step 11: Feature Selection (L1 paths, RFE, Permutation Importance)
- [ ] Step 12: Explainability via SHAP (TreeSHAP/KernelSHAP -> results/figures/)
- [ ] Step 13: Symbolic Regression (PySR/gplearn -> results/formulas/)
- [ ] Step 14: Rigorous Validation (LODO/LOSO and 1000-iter bootstrap CIs)
- [ ] Step 15: Sensitivity Analysis (Stress-test inputs under simulated Mars durations)
- [ ] Step 16: Final Model and Formula Selection (Log winning metrics)
- [ ] Step 17: Scientific Synthesis and Manuscript Drafting (Populate docs/paper/)
