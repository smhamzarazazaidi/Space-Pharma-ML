# Phase A linkage QC

This audit produces diagnostics only. A normalized environmental matrix and master v2 are intentionally not created before Phase A review.

| Check | Result |
|---|---|
| Master rows / unique lot IDs | 32 / 32 |
| Unique drugs / launch missions | 8 / 6 |
| Parent files preserved | Hash comparison passes; see `audit_summary.json` |
| Recomputed relative delta | All legacy pairs reproduce stored relative delta within rounding; does not certify pair correctness |
| Master vs mapping outcome linkage | FAIL: 29 conflicting rows |
| Mapping vs expected drug/formulation figure panel | FAIL: 16 conflicts |
| Independently verified exact ISS intervals | 0 / 32 |
| Lot output row count | 32; unique lot IDs |
| Radiation raw sensor timestamps unique | FAIL: 3,481 extra same-sensor/timestamp records |
| Radiation null / negative values | 0 / 0 |
| Radiation completeness | Per-sensor gaps and boundary truncation; no blanket complete-exposure claim |
| Official RadLab sample comparison | 68 / 68 records match in first-hour subset only |
| Cabin source QA | Missing physical sensor metadata; repeated records and temporal gaps |
| Coverage values | Must be within 0–100%; zero means no acquired temporal support |
| Missing exact times | Blank; never fabricated |
| Numerical coverage boundary tests | Four tests: empty data, long gap/duplicates, clipping and invalid interval |

Reports can be regenerated with the README commands. `lot_variable_availability.csv` has 32 × 6 = 192 rows. Cabin sensor count is blank because the API does not identify sensors. Counts of data streams must not be mislabeled as counts of physical sensors. The radiation chart selects the best-covered individual sensor; individual sensor data remain available in the companion table.

The 5-minute radiation and 10-minute cabin gap limits are transparent audit conventions, not pharmaceutical excursion thresholds or validated interpolation policies. Radiation also reports a 1-hour sensitivity case. No large gaps are integrated or filled. Subtracting the reconstructed end date from a date-only arrival does not give exact ISS residence; every availability value is conditional on that screening envelope.
