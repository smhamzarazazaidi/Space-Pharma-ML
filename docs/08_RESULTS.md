# 08. Experimental Results and Performance Tracking

**Project:** Interpretable Small-Data ML for Predicting Pharmaceutical Response and Stability Under Long-Duration Spaceflight Conditions
**Primary Reference:** docs/RESEARCH_DOCUMENT.md (Section 15)

---

> [!NOTE]
> **Status:** EDA COMPLETE - Steps 6 and 7 of 17 Done
> Static OLS baseline formula established. ML phase not yet started.

## 1. Baseline Model Performance

| Model | Cross-Validation | RMSE (%) | R2 | Status |
| :--- | :--- | :--- | :--- | :--- |
| Mean Regressor (naive) | LODO | NOT YET RUN | 0 (by definition) | Pending |
| OLS Linear Regression (5 features) | LODO | 4.287 | -4.097 (95%CI: -11.668--0.043) | DONE |
| Ridge Regression | LODO | NOT YET RUN | NOT YET RUN | Pending |
| Lasso Regression | LODO | NOT YET RUN | NOT YET RUN | Pending |

## 2. Machine Learning Leaderboard
Status: NOT YET RUN - pending Step 10

## 3. Discovered Symbolic Regression Equations
Status: NOT YET RUN - pending Step 13

## 4. Static OLS Baseline Formula

```
DeltaAPI = -1.0230 - 0.07911*Days + 106.05147*Dose_Gy - 0.06874*XLogP - 0.01586*TPSA - 0.83379*IsSolid
```

| Metric | Value |
|---|---|
| Training R2 | 0.0718 |
| LODO R2 (mean) | -4.0972 |
| LODO 95% CI | [-11.668, -0.043] |
| LODO RMSE (mean) | 4.2868 % |
| n samples | 32 |
| Cross-validation | Leave-One-Drug-Out (LODO) |
