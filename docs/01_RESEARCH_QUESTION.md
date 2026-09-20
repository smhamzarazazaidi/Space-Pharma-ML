# 01. Research Questions & Working Hypotheses

**Project:** Interpretable Small-Data ML for Predicting Pharmaceutical Response and Stability Under Long-Duration Spaceflight Conditions  
**Primary Reference:** [`docs/RESEARCH_DOCUMENT.md`](file:///d:/Space%20medicne/docs/RESEARCH_DOCUMENT.md) (Sections 2, 3, 4)

---

## 1. Formal Research Questions

* **RQ1 (Data Harmonization & Leakage Avoidance):**  
  How effectively can heterogeneous, multi-mission spaceflight pharmaceutical stability assays, environmental radiation metrics, and physicochemical drug descriptors be merged into a unified tabular feature space without causing data leakage across experimental batches?

* **RQ2 (Small-Data Machine Learning Benchmarks):**  
  Which small-data-appropriate machine learning algorithms (e.g., Regularized Ridge/Lasso, Random Forests, Gradient Boosting, Support Vector Regressors, k-NN) provide the highest generalization performance when predicting pharmaceutical degradation under out-of-distribution grouped cross-validation?

* **RQ3 (Interpretable Feature Attribution via SHAP):**  
  What are the key physicochemical markers (e.g., molecular weight, topological polar surface area, rotatable bonds, oxidation susceptibility) and environmental stressors (cumulative radiation dose, mission duration) that govern spaceflight drug stability?

* **RQ4 (Closed-Form Symbolic Equation Discovery):**  
  Can symbolic regression discover parsimonious, closed-form mathematical equations $S_{\text{space}} = f(\text{radiation}, \text{duration}, \text{descriptors})$ that outperform traditional first-order Arrhenius models while remaining biologically and chemically plausible?

* **RQ5 (Extrapolation & Uncertainty Quantification):**  
  What are the quantitative uncertainty bounds (95% bootstrap confidence intervals) and sensitivity limits when model predictions are evaluated under simulated deep-space exploration mission durations (e.g., 500–1000 days)?

---

## 2. Preliminary Working Hypothesis

> [!NOTE]
> **Status:** Preliminary working hypothesis, subject to revision following the Phase 1 Dataset Audit.

It is hypothesized that active pharmaceutical ingredient (API) degradation in spaceflight environments is non-linearly accelerated relative to terrestrial $1g$ controls due to interactions between cumulative cosmic ionizing radiation and drug-specific physicochemical vulnerabilities (e.g., heteroatom count, aromaticity, photostability, excipient interactions). It is further hypothesized that regularized small-data machine learning models and Pareto-optimal symbolic regression equations can model these multi-factor interactions with significantly lower prediction error (lower RMSE/MAE) than univariate standard terrestrial shelf-life extrapolations.
