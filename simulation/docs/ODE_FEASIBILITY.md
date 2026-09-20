# ODE and Kinetic Model Feasibility

## Finding

An ODE such as dS/dt = -kS is not identifiable from the current endpoint-only outcomes. A single endpoint per lot cannot separate initial condition, shape, and degradation rate without imposing a curve. Multiple mission lengths exist for some APIs, but there are too few repeated conditions and no within-mission potency time series to estimate API-specific k reliably.

An ODE would therefore add an assumed trajectory rather than directly measured dynamic information. Any first-order curve would be a model prediction, not an observed potency timeline. Validation against current data could only test endpoints, not intervening dynamics.

No kinetic model is implemented in Phase C. A future ODE requires repeated potency timepoints under measured dose-rate histories, formulation-aware kinetics, and external validation.
