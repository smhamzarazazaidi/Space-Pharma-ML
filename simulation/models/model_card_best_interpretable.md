# Model Card: best_interpretable

- **Model:** OLS
- **Purpose:** Candidate endpoint stability prediction
- **Target:** delta_api_percent
- **Features:** tpsa, xlogp, molecular_weight
- **Training data:** 32 lots, 8 unique APIs
- **Validation:** Nested leave-one-drug-out
- **LODO R2:** 0.363
- **LODO MAE:** 2.771%
- **LODO RMSE:** 3.608%
- **Worst held-out API:** Naloxone
- **Uncertainty:** grouped-bootstrap predictive interval
- **Allowed use:** Research-only within chemical domain with explicit interval and domain status.
- **Disallowed interpretation:** Clinical decision support, causal environmental claims, or out-of-domain assurance.
- **Out-of-domain behavior:** Return warning and no decision-grade interpretation.
