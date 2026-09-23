# Simulation Tutorial

**Orbital Pharmaceutics - Historical Research Simulator**
Phase D - Research prototype - Local use only

---

## Overview

This simulator replays the actual spaceflight environment (radiation, temperature, humidity,
CO2) recorded during ISS missions that carried the 32 pharmaceutical lot samples studied in
this project. At the end of each replay, a provisional OLS stability model predicts the
percentage change in active pharmaceutical ingredient (delta-API) using either:

- **Engine A** -- molecular chemistry only (TPSA, XLogP, molecular weight)
- **Engine B** -- chemistry + observed cumulative station radiation dose

The published laboratory outcome stays hidden until you explicitly reveal it, so each
session reproduces the original blinded prediction exercise.

---

## Requirements

| Requirement | Notes |
|-------------|-------|
| Python 3.12 (bundled) | `START_SIMULATOR.ps1` selects the bundled interpreter automatically |
| Port 8765 available | The server binds only to `127.0.0.1` -- no network access |
| A modern browser | Chrome, Edge, Firefox -- WebGL required for the 3D scene |
| All data pre-built | Run `src/build_phase_d.py` once if `data/simulator/` is missing |

---

## Step 1 -- Start the server

Open PowerShell **inside the `simulation/` folder** and run:

```powershell
.\START_SIMULATOR.ps1
```

You will see:

```
Spaceflight pharmaceutical simulator: http://127.0.0.1:8765
```

Leave that terminal open. The server runs until you close it or press `Ctrl+C`.

**Manual alternative** (if the script cannot find the bundled Python):

```powershell
python simulation/src/serve_phase_d.py --port 8765
```

Use Python 3.12. The `.deps/` folder inside `simulation/` contains pre-installed
numpy, scipy and scikit-learn for that version.

---

## Step 2 -- Open the browser

Navigate to:

```
http://127.0.0.1:8765
```

You will see the dark-themed **Orbital Pharmaceutics** interface with three tabs:

| Tab | Purpose |
|-----|---------|
| **Historical replay** | Replay a real mission with the assay outcome blinded |
| **Validation lab** | Browse all LODO and LTDO predictions with published outcomes visible |
| **Hypothetical lab** | Enter any molecular descriptors and get a domain-checked prediction |

---

## Step 3 -- Historical Replay (main workflow)

### 3a. Choose a validation experiment

In the **Flight Manifest** panel (top-left of the 3D scene):

1. **Validation experiment** dropdown:
   - `One-drug blind test (LODO)` -- train on 7 APIs, test on 1 held-out API
   - `Two-drug blind test (LTDO)` -- train on 6 APIs, test on 2 held-out APIs

2. **Held-out active ingredient** -- the API whose outcome is withheld from the model.
   Default is Caffeine (the main demonstration case).

3. **Flown sample** -- which of that API's physical lots to replay.
   The dropdown shows: mission name, lot ID, days in space.

4. **LTDO only** -- a second API and lot selector appear.
   Caffeine + Diazepam is the recommended starting demonstration (chosen for
   chemistry/formulation contrast before pair errors were examined).

The manifest label **"Published result: HIDDEN"** confirms the assay outcome is not yet
loaded into the interface.

### 3b. Load the mission

Click **Prepare historical replay**.

The server loads:
- reconstructed radiation and cabin environment streams for that mission
- the frozen LODO/LTDO model trained without this API

The 3D scene activates and charts appear in section 03 (below the scene).

### 3c. Understand the 3D scene

| Element | Description |
|---------|-------------|
| Earth globe | Procedural continent shapes -- schematic, not geographic data |
| ISS station | Box-geometry model moving along an inclined orbit ring |
| Payload dot | Small green sphere on the station marking the sample location |
| Orbit path | Faint line showing the representative LEO orbit |
| Sun disc | Fixed at upper left -- visual element only, not a stability model input |
| Star field | ~800 background points |
| Radiation particles | Orange cloud whose density scales with the current observed dose rate |

**Camera controls** (bottom-centre of the scene):

| Button | View |
|--------|------|
| `Earth view` | Wide view centred on Earth |
| `ISS view` | Close-up following the station |
| `Mission view` | Default mid-distance perspective (default) |
| `+` / `-` | Zoom in / zoom out |

You can also **drag** anywhere on the canvas to orbit the camera and **scroll** to zoom.

### 3d. Play, pause, and scrub

The **playback bar** sits immediately below the 3D scene.

| Control | Action |
|---------|--------|
| Play (triangle) | Start time-lapse replay from current position |
| Pause (double bar) | Freeze the replay |
| Restart (arrow) | Re-prepare the same mission from the beginning |
| Scrub slider | Drag to any mission moment instantly |
| TIME ACCELERATION | 1x to 10,000x or AUTO (completes in 60 real seconds) |
| `T + NNN.NN DAYS` | Elapsed simulated mission time |
| Percentage label | Fraction of the full launch-to-landing window |

> **Important:** Playback speed does not affect dose integration. Cumulative dose is
> read from pre-built prefix integrals and is independent of how fast you scrub.

Milestone labels below the slider show the mission sequence:

```
LAUNCH -> TRANSIT -> ISS ARRIVAL -> ON-ORBIT STORAGE -> DEPARTURE -> RETURN -> LANDING
```

Labels are in chronological order but are **not evenly spaced** -- on-orbit storage is
typically 90-95% of the total elapsed time.

### 3e. Read the telemetry panel

The **Historical Telemetry** panel (top-right of the 3D scene) updates every ~450 ms
during playback.

| Field | Source | Data quality grade |
|-------|--------|--------------------|
| Radiation dose rate | DosTel1/DosTel2 merged, piecewise-linear | D (Columbus proxy) |
| Temperature | NASA EDA cabin average | E (location unresolved) |
| Relative humidity | NASA EDA cabin average | E |
| CO2 | NASA EDA cabin average | E |
| Pressure | No historical data available | -- |
| Oxygen | No historical data available | -- |
| Cumulative dose | Derived integral -- gaps not filled | derived |

Each reading shows one of four statuses:

| Status | Meaning |
|--------|---------|
| MEASURED | Exact sensor observation at this timestamp |
| SHORT_GAP_INTERPOLATED | Piecewise-linear fill across a gap of 300 s or less |
| UNAVAILABLE | Outside any supported sensor interval |
| NO DATA | Sensor never acquired data for this mission |

The orange **ELEVATED RADIATION** banner lights up when the dose rate exceeds the 95th-
percentile of raw samples for that mission.

Launch and return windows always show UNAVAILABLE for all sensors -- DosTel was
aboard the station only during on-orbit storage. This is not a data error.

### 3f. Read the exposure charts

Section 03 (below the scene) shows five time-series charts:

- Radiation dose rate (uGy/h)
- Cumulative observed dose (mGy)
- Temperature (deg C)
- Relative humidity (%RH)
- CO2 (ppm)

Each chart plots **12-hour supported means**. Breaks in the line are preserved data
gaps -- they are never filled or interpolated across.

The vertical cursor tracks your current playback position.

### 3g. Evidence coverage bars

The **Evidence Coverage** section (right of the charts) shows what fraction of the
full lot flight window has supported telemetry.

| Variable | Typical coverage | Tier |
|----------|-----------------|------|
| Radiation | 88% fleet average | GREEN |
| Temperature | 17% fleet average | YELLOW |
| Relative humidity | 17% fleet average | YELLOW |
| CO2 | 17% fleet average | YELLOW |
| Pressure | 0% | RED |
| Oxygen | 0% | RED |

Missing data are **not zero exposure** -- they are genuinely unknown.

### 3h. Wait for landing (or scrub to 100%)

The **Provisional Stability Engine** panel (section 04) shows a locked placeholder
until mission progress reaches 100%.

Either let playback run to completion or drag the scrub slider fully to the right.

At landing the model computes and displays:

| Field | Meaning |
|-------|---------|
| Large percentage number | Predicted delta-API (change vs ground control) |
| Stability ratio | 100 + predicted_delta_api as % of matched ground API |
| 95% approx. interval | Bootstrap predictive interval (wide = unstable) |
| Domain status | IN_DOMAIN / NEAR_BOUNDARY / OUT_OF_DOMAIN with distance |
| Contributions | Intercept and each coefficient x feature in percentage points (not causal %) |

Switch between **Engine A** and **Engine B** tabs to compare chemistry-only vs
chemistry + dose predictions.

### 3i. Reveal the published result

Click **Reveal published experiment**.

The actual laboratory assay outcome loads and the interface shows:

- Published delta-API %
- Absolute error in percentage points
- A note on possible error sources

The manifest label changes from **HIDDEN** to **REVEALED**.

---

## Step 4 -- Validation Lab

Click the **Validation lab** tab to see all pre-computed results with published outcomes
already visible (this tab is not blinded).

1. Click **Open published comparison** to load the full table.
2. Use the filters:
   - **Validation** -- LODO (8 single-drug holdouts) or LTDO (28 two-drug pairs)
   - **Engine** -- A (chemistry only) or B (chemistry + dose)
   - **API** -- filter to one active ingredient

Table columns:

| Column | Meaning |
|--------|---------|
| Held out | Which API(s) were excluded from training |
| API / lot | Specific lot and mission |
| Prediction % | Model output |
| Published % | Laboratory assay result |
| Abs. error pp | Absolute error in percentage points |
| 95% approx. interval | Bootstrap predictive interval |
| Domain | IN_DOMAIN / NEAR_BOUNDARY / OUT_OF_DOMAIN |

**Summary metrics (pre-computed):**

| Engine | Validation | R2 | RMSE | MAE |
|--------|------------|-----|------|-----|
| A (chemistry) | LODO | 0.363 | 3.608 pp | 2.771 pp |
| B (chem + dose) | LODO | 0.490 | 3.227 pp | 2.488 pp |
| A (chemistry) | LTDO | -0.313 | 5.177 pp | 4.003 pp |
| B (chem + dose) | LTDO | -0.016 | 4.554 pp | 3.584 pp |

> LTDO R2 is negative for both engines. The model generalises poorly to completely
> unseen chemistry pairs -- expected given only 8 training APIs total.

---

## Step 5 -- Hypothetical Lab

Click the **Hypothetical lab** tab to estimate stability for a molecule not in the
dataset (research use only).

Fill in:

| Field | Description | Example |
|-------|-------------|---------|
| API or scenario name | Label only, not a model input | `New analgesic` |
| TPSA (A^2) | Topological polar surface area | `54.37` |
| XLogP | Calculated lipophilicity | `2.1` |
| Molecular weight (g/mol) | Molecular weight | `296.5` |
| Formulation | Context note, not a model input | `Solid` |
| Mission duration (days) | Informational only | `180` |

Click **Check domain and estimate endpoint**.

The output shows:
- Domain status (IN_DOMAIN / NEAR_BOUNDARY / OUT_OF_DOMAIN)
- Predicted delta-API %
- 95% approximate predictive interval
- A prominent warning if the molecule is outside the training chemical space

> SMILES parsing, molecular structure validation, and hypothetical environmental
> response are **not** implemented. This uses Engine A (chemistry descriptors only).
> All runs are logged locally to `results/simulation_runs/`.

---

## Interpreting results

### What the model is

A fixed OLS regression fitted on 32 pharmaceutical lots from 8 APIs. It estimates
delta-API as a linear combination of molecular descriptors (and optionally cumulative
station dose). It is a **retrospective research tool** -- not a validated
pharmacokinetic or regulatory stability model.

### What delta-API means

```
delta-API = (flight assay - matched ground control) / ground control * 100
```

Negative values = degradation. Positive values = apparent increase (measurement
uncertainty, formulation effects, or assay variability).

### Domain statuses

| Status | Meaning |
|--------|---------|
| IN_DOMAIN | Distance <= median leave-one-out nearest-neighbour distance among training API centroids |
| NEAR_BOUNDARY | Between median and maximum training nearest-neighbour distance |
| OUT_OF_DOMAIN | Beyond the outermost training chemistry -- uncertainty very high |

### Uncertainty intervals

400-draw group-bootstrap predictive intervals. **Not calibrated** -- actual coverage
may differ from the stated 95%. Very wide or physically impossible bounds (below -100%
or implying implausible concentration gain) indicate model instability, not a
validated prediction.

### Radiation caveat

DosTel measures dose rate in Columbus module. It is a **station proxy**, not absorbed
dose inside a drug package. Engine B's dose term reduces LODO MAE by approximately 10%
but is not distinguishable from a mission-duration proxy (Spearman rho = 1.0 between
cumulative dose and mission duration; VIF = 41). No causal radiation effect is
established by this analysis.

---

## Stopping the server

Press `Ctrl+C` in the terminal running `START_SIMULATOR.ps1`.
All run logs are saved to `results/simulation_runs/` as JSON files and persist after
the server stops.

---

## File locations

| Path | Contents |
|------|----------|
| `START_SIMULATOR.ps1` | Launch script |
| `src/serve_phase_d.py` | HTTP server (Python) |
| `app/` | Browser frontend (HTML, CSS, JS, Three.js 0.170.0) |
| `src/simulator/` | Backend modules |
| `data/simulator/catalog.json` | 32-lot manifest with molecular descriptors |
| `data/simulator/missions/` | Per-mission 12-h environmental bin data (6 missions) |
| `data/simulator/private/validation.json` | Pre-computed LODO/LTDO predictions |
| `data/simulator/environment_streams/` | Full-resolution NPZ sensor archives |
| `models/phase_d_v0/registry.json` | Saved OLS coefficients (72 folds) |
| `results/tables/` | All validation CSV and JSON outputs (41 files) |
| `results/simulation_runs/` | Per-session run logs (created on first use) |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Port 8765 already in use | Edit `START_SIMULATOR.ps1` or pass `--port 8766` to `serve_phase_d.py` |
| `No module named numpy` | Confirm the script uses the bundled Python 3.12 at `.cache/codex-runtimes/...` |
| Black 3D scene (no globe) | WebGL unavailable; the 2D fallback Earth disc appears automatically |
| Charts show NO HISTORICAL DATA | Normal -- cabin coverage is 17%; some lots have no cabin readings at all |
| Prediction never appears | Drag the scrub slider fully to the right (100%) and wait one poll cycle (~450 ms) |
| Very wide uncertainty interval | Expected for small datasets; flag as unstable and do not use for decisions |
| `SELECT one or two distinct held-out APIs` error | You chose the same API in both LTDO selectors; pick two different APIs |

---

## Related documentation

| Document | Topic |
|----------|-------|
| [HISTORICAL_SIMULATOR_METHOD.md](HISTORICAL_SIMULATOR_METHOD.md) | Integration, validation design, uncertainty, data provenance |
| [LTDO_VALIDATION.md](LTDO_VALIDATION.md) | All 28 two-drug holdout pair results and pooled metrics |
| [PHASE_D_SIMULATOR_REPORT.md](PHASE_D_SIMULATOR_REPORT.md) | Phase D Q&A readiness report and final numbers |
| [ENVIRONMENT_DATA_PROVENANCE.md](ENVIRONMENT_DATA_PROVENANCE.md) | NASA RadLab and EDA data sourcing details |
| [PHASE_B_REPORT.md](PHASE_B_REPORT.md) | Radiation-duration collinearity analysis |
| [PHASE_C_MODEL_REPORT.md](PHASE_C_MODEL_REPORT.md) | Full model candidate benchmark comparison |
