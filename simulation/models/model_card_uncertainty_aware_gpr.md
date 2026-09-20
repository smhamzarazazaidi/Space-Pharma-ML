# Model Card: uncertainty_aware_gpr

- **Model:** GPR
- **Purpose:** Candidate endpoint stability prediction
- **Target:** delta_api_percent
- **Features:** tpsa, xlogp, molecular_weight
- **Training data:** 32 lots, 8 unique APIs
- **Validation:** Nested leave-one-drug-out
- **LODO R2:** -0.182
- **LODO MAE:** 3.422%
- **LODO RMSE:** 4.912%
- **Worst held-out API:** Epinephrine
- **Uncertainty:** GPR posterior SD plus grouped-bootstrap comparison
- **Allowed use:** Research-only within chemical domain with explicit interval and domain status.
- **Disallowed interpretation:** Clinical decision support, causal environmental claims, or out-of-domain assurance.
- **Out-of-domain behavior:** Return warning and no decision-grade interpretation.
