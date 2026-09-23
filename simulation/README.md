# ISS pharmaceutical exposure simulation research

Status: **Phase D complete — Historical Research Simulator operational.**

**→ [SIMULATION\_TUTORIAL.md](docs/SIMULATION_TUTORIAL.md) — start here to run and use the simulator.**

The simulator replays real ISS mission environments for 32 pharmaceutical lots across 8 APIs
and produces blinded LODO/LTDO stability predictions. Start the server with:

```powershell
.\START_SIMULATOR.ps1
```

Then open `http://127.0.0.1:8765` in a browser.

---

## Documentation index

| Document | Topic |
|----------|-------|
| [SIMULATION_TUTORIAL.md](docs/SIMULATION_TUTORIAL.md) | **How to run and use the simulator — start here** |
| [PHASE_D_SIMULATOR_REPORT.md](docs/PHASE_D_SIMULATOR_REPORT.md) | Phase D readiness Q&A and final metrics |
| [HISTORICAL_SIMULATOR_METHOD.md](docs/HISTORICAL_SIMULATOR_METHOD.md) | Integration, validation design, uncertainty, provenance |
| [LTDO_VALIDATION.md](docs/LTDO_VALIDATION.md) | All 28 two-drug holdout pair results |
| [PHASE_C_MODEL_REPORT.md](docs/PHASE_C_MODEL_REPORT.md) | Model candidate comparison |
| [PHASE_B_REPORT.md](docs/PHASE_B_REPORT.md) | Environmental exposure analysis and collinearity |
| [PHASE_A_AUDIT.md](docs/PHASE_A_AUDIT.md) | Original dataset audit |
| [ENVIRONMENT_DATA_PROVENANCE.md](docs/ENVIRONMENT_DATA_PROVENANCE.md) | NASA RadLab and EDA sourcing |

---

## Phase history

This folder is isolated from the parent project. Phases A through D were completed in sequence:

- **Phase A** — dataset audit; outcome linkage, radiation sensor policy, provenance.
- **Phase B** — environmental exposure matrix; coverage and collinearity analysis.
- **Phase C** — model candidate selection; OLS, Ridge, ElasticNet, GPR, RF benchmarks.
- **Phase D** — historical replay simulator; LODO/LTDO validation; blinded caffeine test.

Downloaded NASA payloads are immutable and have adjacent SHA-256 provenance records.
Generated CSV outputs are derived diagnostics, not corrected experimental measurements.

## Reproduce

With Python 3.12 and `requirements.txt` dependencies installed, run from this folder:

```powershell
python src/audit_project.py
python src/audit_environment.py
python -m unittest discover -s tests -v
```

`audit_project.py` locates the parent project relative to its own file, so it also works from the workspace root. `audit_environment.py --no-plot` runs tabular checks without matplotlib. The isolated `.deps` folder is used for the plotting dependencies in this desktop environment. No parent requirements or package installation was changed.

`src/collect_sources.py` archives only explicitly supplied HTTPS URLs on NASA's visualization domain. It refuses path traversal and preserves an existing file. Each payload has its acquisition URL, UTC time, status, byte count and checksum in a sidecar JSON. A file being downloadable does not establish scientific suitability. The collector is optional for reproduction of the already archived audit.

## Outputs

- `data/processed/medication_exposure_windows.csv`: 32 provisional lot windows with unknown exact events left blank.
- `results/tables/outcome_linkage_audit.csv`: differences between existing master and existing mapping records; neither table is promoted as corrected truth.
- `results/tables/radiation_sensor_audit.csv`: raw instrument cadence and gaps.
- `results/tables/radiation_temporal_coverage.csv`: per-sensor coverage sensitivity using 5-minute and 1-hour maximum adjacent gaps.
- `results/tables/environment_source_inventory.csv`: acquired EDA streams, units, date coverage, missingness and provenance.
- `results/tables/lot_variable_availability.csv`: provisional availability across six variables.
- `results/figures/environment_availability.png`: coverage heatmap.
- `results/tables/parent_file_inventory.csv`: hashes for parent files, checked unchanged at the end of the project audit.

## Review boundary

The first follow-on work should repair outcome provenance into a new reviewed dataset, resolve return-vehicle linkage and define the radiation sensor/duplicate policy. Only then should Phase B create the environmental exposure matrix. The original `master_dataset_v1.csv` must remain intact.
