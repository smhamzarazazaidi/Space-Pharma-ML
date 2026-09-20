# Phase D historical pharmaceutical simulator

## Q1

All 32 inherited mission windows have replay infrastructure, but complete actual local environments are NOT reconstructed. Telemetry gaps, package location and return-manifest uncertainty remain.

## Q2

DosTel radiation and intermittent EDA temperature, RH and CO2 are measured station data. Between readings, short interpolation and integrated dose are derived.

## Q3

Cabin support is sparse: mean temperature 16.3%, RH 16.3%, CO2 16.3%. Pressure and oxygen have zero historical coverage.

## Q4

Live values have measured/interpolated/unavailable status; dose is derived; final delta API is predicted; the Earth/orbit/station/sun are decorative schematic geometry.

## Q5

Engine A LODO R2 0.3626, RMSE 3.6076, MAE 2.7708 percentage points; it reproduces the M4 benchmark.

## Q6

Engine B LODO R2 0.4900, RMSE 3.2269, MAE 2.4881. Improvement on both errors: YES.

## Q7

LTDO A R2 -0.3126, RMSE 5.1769, MAE 4.0030; B MAE 3.5840. See the separate pair report.

## Q8

Caffeine LODO MAE 3.5117, mean prediction -9.6110, published mean -6.0993. All four caffeine lots are absent from its fit.

## Q9

Caffeine + Diazepam LTDO MAE 3.1918; worst of all pairs is Diazepam + Naloxone (10.2096).

## Q10

Largest Engine A LODO API errors: Naloxone (6.525) and Diphenhydramine (4.666) percentage points.

## Q11

Exploratory LODO A Spearman error/domain-distance association 0.476; repeated lots and eight APIs preclude strong inferential claims.

## Q12

Exploratory LODO A error/radiation-coverage association 0.065; this is not proof that missingness causes errors.

## Q13

For the fixed additive radiation test, improvement in both pooled LODO errors: YES. No radiation causal effect is established.

## Q14

No additional cabin factor is supported for primary prediction at this coverage. No invented environmental weights are fitted.

## Q15

No causal contribution percentages. Linear terms can be decomposed additively in delta-API percentage points, dependent on units and correlated inputs.

## Q16

Suitable for retrospective research exploration with explicit missingness, provenance and uncertainty; not a clinical tool or validated potency simulator.

## Q17

Descriptor-based research-only endpoint estimates are supported with intervals and prominent domain warnings. There is no validated hypothetical environmental response or molecular SMILES parser.

## Q18

Highest priorities: additional unseen APIs, matched controlled radiation experiments, repeated potency timepoints, package-level telemetry, exact downmass/storage/assay linkage and independently audited digitization.

## Readiness

3D HISTORICAL SPACE ENVIRONMENT: COMPLETE as schematic visualization, not historical ephemeris.

MISSION TELEMETRY REPLAY: COMPLETE for acquired streams; historical coverage remains incomplete.

CAFFEINE BLINDED REPLAY: COMPLETE as retrospective outcome-masked replay.

8-API LODO REPLAY: COMPLETE.

TWO-DRUG LTDO: COMPLETE (28 pairs).

SCIENTIFIC SIMULATOR UI: COMPLETE; see test evidence.

ENVIRONMENT-AWARE MODEL IMPROVES BASELINE: YES in this fixed exploratory comparison.

READY FOR RESEARCH-ONLY NEW DRUG SIMULATION: YES for endpoint descriptor dry runs; no validated kinetics.

READY FOR FINAL MODEL FREEZE: NO.

READY FOR VULNERABILITY RANKING: NO.

STOP FOR REVIEW.
