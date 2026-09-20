# Phase A data dictionary

| Field / artifact | Meaning and evidence type |
|---|---|
| `lot_id` | Existing `sample_id`, retained as stable join key |
| `api`, `mission`, `formulation` | Existing pharmaceutical metadata, not new observations |
| `launch_date`, `arrival_date` | Date-level mission evidence; medication transfer not established |
| `launch_datetime`, `docking_datetime` | UTC mission event when sourced; docking field holds documented robotic berthing and is qualified by notes |
| `departure_datetime`, `landing_datetime` | Blank because lot-specific exact events were not verified |
| `iss_exposure_hours` | Blank because exact transfer/departure times are unknown |
| `total_spaceflight_hours` | Published integer days × 24; derived, not timestamp precision |
| `reconstructed_landing_date` | Launch date + published days; not verified landing |
| `candidate_proxy_*_date` | Date-level screening interval for availability, not an approved exposure window |
| `legacy_end_shift_days` | Legacy reconstructed end minus launch-based reconstructed end |
| `days_expired_at_analysis` | Expiration relative to assay, not relative to launch or landing |
| `spatial_relevance_grade` | D = ISS-wide proxy (DosTel); E = sensor location not resolved (EDA). No A/B/C exposure established |
| `derived_stability_ratio` | 100 × existing Flight / existing Ground; algebraic diagnostic only until outcome linkage repaired |
| `recomputed_relative_delta` | 100 × (existing Flight − existing Ground) / existing Ground; relative percent, not percentage points |
| `observed_support_hours` | Duration between supported adjacent timestamps under declared gap limit; conditional estimate of availability |
| `coverage_percent` | 100 × observed support / provisional expected hours |
| `largest_missing_interval_hours` | Largest unsupported interior or boundary interval |
| `sensor_count` | Known distinct physical sensors only; blank for EDA |
| `missing_cells` | Nulls in raw API field, including sparse repeated rows; not a temporal gap fraction |
| `conflicting_timestamps` | Same variable/time with multiple distinct non-null values within a dataset |
| `download_status` | Completed raw acquisition or empty API response; neither implies scientific suitability |

No file in this phase contains new predictions, synthetic telemetry or corrected assay measurements.
