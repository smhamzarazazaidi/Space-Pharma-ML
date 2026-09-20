# Pharmaceutical Vulnerability & Priority Ranking Design Notes

**Document Status:** Conceptual Architecture & Design Principles (Pre-Modeling)  
**Parent Project:** Interpretable Small-Data ML for Predicting Pharmaceutical Stability  
**Phase:** B.2 Checkpoint  

---

## 1. Scientific Principles of Vulnerability Ranking

Vulnerability ranking must be **strictly downstream of a validated stability prediction model**. Ranking cannot be an arbitrary scoring heuristic or weighted index constructed prior to establishing empirical predictive accuracy.

### Why Ranking Must Follow Stability Modeling:
1. **Physical Grounding:** A drug is vulnerable if its active pharmaceutical ingredient (API) is predicted to degrade past clinically significant thresholds (e.g., $<90\%$ of label claim, USP standards) under specific mission profiles.
2. **Epistemic Uncertainty:** Small-data models produce wider prediction intervals for out-of-distribution molecules. Ranking must penalize high uncertainty to avoid false confidence during deep-space medical kit manifest design.
3. **Environmental Sensitivity:** Vulnerability is not static; it is a partial derivative $\frac{\partial \Delta\text{API}}{\partial \text{Radiation}}$ and $\frac{\partial \Delta\text{API}}{\partial \text{Duration}}$.

---

## 2. Candidate Vulnerability Components (Unweighted Concept Library)

When the Phase C dynamic ML and symbolic regression engines are validated, the composite Vulnerability Index $V(d, m)$ for drug $d$ under mission scenario $m$ will synthesize six orthogonal criteria:

```
                      ┌────────────────────────────────────────┐
                      │  PHARMACEUTICAL VULNERABILITY INDEX   │
                      └───────────────────┬────────────────────┘
                                          │
        ┌───────────────────┬─────────────┴───────────┬───────────────────┐
        ▼                   ▼                         ▼                   ▼
┌──────────────┐    ┌───────────────┐         ┌───────────────┐    ┌──────────────┐
│  Predicted   │    │  Prediction   │         │ Environmental │    │  Formulation │
│  Degradation │    │  Uncertainty  │         │  Sensitivity  │    │  Modifier    │
│  |ΔAPI_pred| │    │  (95% CI Width│         │ (∂ΔAPI/∂Dose) │    │(Solid/Liquid)│
└──────────────┘    └───────────────┘         └───────────────┘    └──────────────┘
```

### Component 1: Predicted Degradation Magnitude ($\hat{\Delta}$)
- Definition: Expected API percentage loss at destination: $\hat{\Delta} = \max(0, -\hat{y}_{\text{pred}})$.
- Role: Primary clinical penalty for loss of therapeutic efficacy.

### Component 2: Epistemic & Aleatoric Uncertainty Width ($U$)
- Definition: Width of the 95% predictive posterior interval: $U = \hat{y}_{\text{upper}} - \hat{y}_{\text{lower}}$.
- Role: Safeguard against untested chemical structures where the model extrapolates.

### Component 3: Environmental Sensitivity Slope ($S_{\text{env}}$)
- Definition: Rate of degradation acceleration under increased radiation dose rate or thermal excursions: $S_{\text{rad}} = \frac{\partial \hat{y}}{\partial \text{Dose}}$.
- Role: Identifies compounds highly susceptible to Solar Particle Events (SPEs) or deep-space galactic cosmic rays (GCR).

### Component 4: Formulation Risk Modifier ($F$)
- Definition: Binary or categorical hazard penalty reflecting phase stability (Nonsolid liquid solutions exhibit higher oxidation and radical mobility than solid crystalline matrices).
- Role: Differentiates autoinjector solutions (e.g., Epinephrine) from blister-packed tablets.

### Component 5: Out-of-Distribution (OOD) Chemical Distance ($D_{\text{chem}}$)
- Definition: Mahalanobis or Tanimoto distance in PubChem descriptor space relative to the $N=8$ training API centroids.
- Role: Downgrades ranking confidence for novel pharmacophores outside the training domain.

### Component 6: Criticality / Toxic Degradant Risk ($T$)
- Definition: Penalty for formation of active/toxic degradants (e.g., Epinephrine oxidation to adrenochrome).

---

## 3. Explicit Prohibition of Premature Weights

> [!WARNING]
> **NO ARBITRARY WEIGHTS:** In accordance with Phase B guidelines, no linear weights ($w_1, w_2, \dots, w_6$) or ranking formulas are assigned at this stage. 
> Weights must be calibrated empirically in Phase C based on model validation errors, cross-validated calibration curves, and space medicine clinical requirements.
