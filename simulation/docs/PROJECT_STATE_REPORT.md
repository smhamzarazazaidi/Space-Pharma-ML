# Project-state audit — Phase A

Date: 2026-09-19. Scope: read existing research inputs; write only inside `simulation/`.

## Existing project

The parent project contains a 32-lot master CSV, eight API descriptor profiles, six delivery missions, a large DosTel radiation CSV, the Nowadly 2026 paper and supplement, extraction scripts, statistical analyses, figures and manuscript notes. It uses Python, pandas, NumPy, scipy and scikit-learn. No existing simulator application was found. Several notebooks and package modules are scaffolds. README status and outcome-status notes lag behind the populated master dataset.

## Findings before implementation

1. `scratch/digitize_all_lots.py` assigns outcome Series into the master by row index, not `sample_id`. The outcome list is grouped by drug while the master is grouped by mission. The mapping QC table itself also contains inconsistent drug/figure assignments. Neither is a validated replacement for the other. Re-extraction and independent lot-to-panel checking are required before ML.
2. `scratch/process_master_dataset.py` constructs end dates as ISS arrival plus `days_in_space`. The primary paper, Table 1 footnote, defines days in space as launch to landing. Existing end dates are reconstructed and shifted; they are not independently verified returns. Exact departure and landing timestamps remain unknown.
3. The existing cumulative radiation feature is an arithmetic pooled-sensor mean multiplied by duration. This is not the time-weighted integration described in the previous validation report. Unequal sensor sampling and uncovered intervals require explicit handling.
4. Existing EDA uses Flight minus Ground in percentage points, whereas the requested target is 100 × (Flight − Ground) / Ground. Existing EDA and formula results do not validate the requested target.
5. The radiation file ends before the longest existing lot window. Previous blanket coverage claims require recomputation. Dose units are documented externally, not embedded in the CSV header. The actual raw timestamps have no explicit timezone suffix.
6. Storage location relative to Columbus is not established. Treat radiation as Grade D ISS-wide proxy, not exact pharmaceutical dosimetry. Same-hardware exposure has not been demonstrated.

## Implementation boundary

Build a reproducible Phase A audit, per-lot provisional windows, environmental source inventory, acquisition provenance and evidence-gap reports inside this folder. Preserve all parent data and research outputs. Do not fit models, repair outcomes silently, or build the final simulator before the Phase A review required by `master-task.txt` Part 33.

The detailed results and acquisition status will be recorded in `PHASE_A_AUDIT.md` after execution.
