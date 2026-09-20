# 06. Modeling & Validation Methodology

**Project:** Interpretable Small-Data ML for Predicting Pharmaceutical Response and Stability Under Long-Duration Spaceflight Conditions  
**Primary Reference:** [`docs/RESEARCH_DOCUMENT.md`](file:///d:/Space%20medicne/docs/RESEARCH_DOCUMENT.md) (Sections 10, 11, 12, 13)

---

## 1. Small-Data Machine Learning Stack
* **Baseline Benchmarks:** Non-learning Mean/Median regressors, Ordinary Least Squares (OLS), Ridge ($L_2$), Lasso ($L_1$), ElasticNet.
* **Classical Machine Learning:** Random Forest Regressor, Gradient Boosting (XGBoost, LightGBM), Support Vector Regressor (SVR with RBF/Linear kernels), k-Nearest Neighbors.
* **Feature Selection:** L1 penalty paths, Recursive Feature Elimination (RFE), Permutation Feature Importance.

## 2. Explainable AI (XAI)
* **SHAP (SHapley Additive exPlanations):** TreeSHAP for tree ensembles, KernelSHAP for non-tree algorithms to extract directional feature attributions, beeswarm plots, and non-linear feature dependency curves.

## 3. Symbolic Regression
* Closed-form discovery of candidate equations $S_{\text{space}} = f(\text{radiation}, \text{duration}, \text{descriptors})$.
* Selection along the Pareto frontier balancing predictive accuracy ($R^2$, RMSE) and complexity (operator length).

## 4. Leakage-Free Validation Strategy
* **Leave-One-Drug-Out (LODO):** Evaluates generalizability to unseen active pharmaceutical ingredients.
* **Leave-One-Study-Out (LOSO):** Evaluates generalizability across independent mission/batch environments.
* **Uncertainty Quantification:** 1,000-iteration non-parametric bootstrap resampling for all primary metrics.
