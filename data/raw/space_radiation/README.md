# Raw Space Radiation & Environmental Dosimetry Data

## 1. Data Classification
* **Category:** Environmental Dosimetry & Space Radiation Environment Measurements
* **Target Domain:** Absorbed dose rates ($\mu\text{Gy/day}$), dose equivalent ($\mu\text{Sv/day}$), Galactic Cosmic Ray (GCR) particle spectra, Solar Particle Event (SPE) indices, and spacecraft shielding factors.

## 2. Original Sources
* NASA OSDR Environmental Data / RadLab portal: https://visualization.osdr.nasa.gov/radlab/gui/leo/iss/
* ISS Columbus module DOSIS 3D experiment: DosTel 1 and DosTel 2 (ESA/DLR) — Continuous since 2012.
* ISS Onboard Active and Passive Dosimeter logs (e.g., TEPC, REM, LIDAL, Liulin-5, PADLES).
* NASA Space Radiation Analysis Group (SRAG) historical mission dose reports.

## 3. Recommended Primary Instrument

**DosTel 1 + DosTel 2** (DOSIS 3D experiment, ESA/DLR):
* Location: Columbus module
* Coverage: Continuous from 2012 through present day; confirmed active 2018–2022
* Measurements: Absorbed dose rate (µGy/h), particle flux, linear energy transfer (LET)
* Time resolution: ~1 minute
* Download path: RadLab GUI → ISS → DosTel 1/2 → select date range → CSV

## 4. Download Rules & Protocol
* Acquire radiation datasets corresponding to the exact mission flights and temporal intervals of audited pharmaceutical stability samples.
* **Full coverage window required: 2018-06-01 to 2022-11-01** (spans all DS-01 missions with buffer).
* Record download details in `data/DOWNLOAD_MANIFEST.csv`.
* See detailed audit: `docs/RADLAB_AUDIT.md`

## 5. Naming Convention
* Standard format: `RAD_<mission_or_instrument>_<start_year>_<end_year>.<ext>`
* Primary file: `RAD_ISS_Columbus_DosTel_2018_2022.csv`
* Example segmented: `RAD_mission_SpX15_2018-07-02_2019-09-01.csv`

## 6. Raw Data Preservation Rules
* **IMMUTABLE:** Raw radiation time-series and tabular logs must remain in their original formats without manual edits.
* Do not rename columns in raw files. Add a `README_columns.md` if column names are unclear.

## 7. Provenance Requirements
* Record detector type, location/module within the spacecraft, shielding thickness estimates, and calibration metadata in `docs/RESEARCH_DOCUMENT.md`.

## 8. Automated Downloading
* **RadLab REST API is currently NON-FUNCTIONAL (2026-09-17)** — see `docs/RADLAB_AUDIT.md` for details.
* **Use the RadLab Portal GUI at https://visualization.osdr.nasa.gov/radlab/gui/leo/iss/** to manually download the DosTel CSV.
* ALLOWED: Automated post-processing via scripts in `src/data/` once raw files are downloaded.

## 9. Current Status
* `STATUS: IDENTIFIED — PENDING MANUAL PORTAL DOWNLOAD`
* Audit complete: See `docs/RADLAB_AUDIT.md`
* Literature-based dose rate estimates documented in `docs/RADLAB_AUDIT.md` Section 5 (for planning only).
* No raw datasets downloaded yet. Awaiting human operator download via RadLab portal GUI.

## 10. Mission Radiation Windows (from DS-01 audit)

| Mission | Deliver Date | Max `days_in_space` | Radiation Query End Date |
| :--- | :--- | :--- | :--- |
| SpX-15 | 2018-07-02 | 424 d | ~2019-09-01 |
| SpX-16 | 2018-12-08 | 265 d | ~2019-09-01 |
| NG-11 | 2019-04-19 | 132 d | ~2019-09-01 |
| SpX-17 | 2019-05-06 | 248 d | ~2020-01-15 |
| SpX-18 | 2019-07-27 | 257 d | ~2020-04-10 |
| SpX-20 | 2020-03-09 | 972 d | ~2022-10-10 |
