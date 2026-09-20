# DS-02 Space Radiation Dosimetry Validation Report

## 1. File Verification Details

| Parameter | Observed Value |
| :--- | :--- |
| **Raw Filename** | `data/raw/space_radiation/RAD_ISS_Columbus_DosTel_2018_2022.csv` |
| **File Size** | 163,791,275 bytes (156.2 MB) |
| **Total Row Count** | 2,336,764 records |
| **SHA256 Hash** | `89567A16C4F46303E5D7F994A7E12B0B50EAB8DFE3CE5D2DE19E9CE0A6200D00` |
| **Columns** | `timestamp`, `instrument_id`, `absorbed_dose_rate`, `instrument`, `module`, `spacecraft` |
| **Date/Time Column** | `timestamp` (ISO 8601 string, e.g. `"2018-06-01T00:00:28"`) |
| **Minimum Timestamp** | `2018-06-01 00:00:28` |
| **Maximum Timestamp** | `2022-11-01 23:56:35` |
| **Missing Values** | 0 (Zero nulls across all 6 columns) |
| **Duplicate Exact Rows** | 0 |
| **Negative/Zero Values**| 0 negative values, 0 zero values |

---

## 2. Instrument & Measurement Structure

The Columbus module hosts the DOSIS 3D experiment with two distinct silicon semiconductor detector telescopes:

* **DosTel1 (Detector 1):** 889,458 readings
  - Mean Absorbed Dose Rate: $32.93\ \mu\text{Gy/hour}$
  - Median: $5.32\ \mu\text{Gy/hour}$
  - Interquartile Range: $5.32 - 9.96\ \mu\text{Gy/hour}$
  - Peak (South Atlantic Anomaly): $865.23\ \mu\text{Gy/hour}$
* **DosTel2 (Detector 2):** 1,447,306 readings
  - Mean Absorbed Dose Rate: $28.87\ \mu\text{Gy/hour}$
  - Median: $5.22\ \mu\text{Gy/hour}$
  - Interquartile Range: $5.22 - 9.53\ \mu\text{Gy/hour}$
  - Peak (South Atlantic Anomaly): $828.69\ \mu\text{Gy/hour}$

### Scientific Aggregation Strategy
DosTel1 and DosTel2 are orthogonally mounted detectors inside the same DOSIS 3D hardware unit in the Columbus module. They record directional absorbed doses from galactic cosmic radiation (GCR) and trapped protons. Both instruments report identical physical units ($\mu\text{Gy/hour}$). To represent the isotropic environmental field inside Columbus, readings are combined via time-weighted Riemann integration across each medication lot's active ISS interval.

---

## 3. Time Series Gaps & Quality Assessment

* Median sampling interval: $\sim 1.67\ \text{minutes}$ ($\sim 100\ \text{seconds}$).
* $>99\%$ of measurement steps occur within $3.33\ \text{minutes}$.
* Gaps $> 1\ \text{hour}$: Only 10 in DosTel1 and 7 in DosTel2 across the entire 4.4-year flight period.
* Gaps $> 24\ \text{hours}$: 5 occurrences (associated with payload power cycles or ISS maintenance).
* **Overall Coverage:** $>99.8\%$ temporal coverage across all 6 target mission intervals (SpX-15, SpX-16, SpX-17, NG-11, SpX-18, SpX-20).

---

## 4. Nature of Dosimetry (Critical Distinction)

> [!IMPORTANT]
> **Environmental Estimate vs Direct Dosimetry:**
> The radiation exposure assigned to each medication lot is an **environmental ISS radiation estimate** derived from DosTel measurements in the Columbus module during the medication's on-station interval. It is **not** direct medication-level dosimetry. No active dosimeter was embedded inside the pharmaceutical packages.
