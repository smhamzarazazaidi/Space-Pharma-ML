# Phase A.2 — Historical Exposure & Outcome Reconciliation Report

**Date of Execution:** 20 September 2026 (Asia/Karachi)  
**Parent Workspace:** `d:/Space medicne` / `simulation`  
**Status:** Audit & Reconciliation Complete — Checkpoint Before Phase B  

---

## Executive Summary

Phase A identified four major obstacles preventing sound predictive modeling and machine learning:
1. **29/32 outcome disagreement** between `master_dataset_v1.csv` and `nowadly_outcome_mapping_qc.csv`.
2. **2–3 day exposure date shift** in legacy duration calculations.
3. **3,481 conflicting duplicate timestamps** in the historical RadLab radiation telemetry.
4. **Severe environmental telemetry missingness** (0–38% coverage across cabin atmospheric variables).

Through Phase A.2, each discrepancy has been traceably investigated against the original Nowadly et al. (2026) publication, supplementary materials, NASA flight manifests, and raw instrument archives. All 32 experimental lots have been reconciled to primary source figures and tables. Exposure windows have been corrected to formal launch-to-landing definitions. The radiation duplicates have been statistically characterized and isolated. Environmental availability has been mapped across all 32 lots into a formal multi-variable coverage matrix and confidence framework.

---

## 1. Resolution of the 29/32 Outcome Mapping Disagreements

### Root Cause Investigation
Investigation revealed that the 29/32 disagreement stemmed from **two separate compounding errors** in legacy processing:
1. **Positional Vector Assignment Error in `master_dataset_v1.csv`:** In `scratch/digitize_all_lots.py`, digitized outcome values were constructed in drug-grouped order (4 Caffeine, 2 Diazepam, 3 Diphenhydramine capsules, etc.). When populating `master_dataset_v1.csv`, a direct positional assignment `df_master1['flight_percent_api_remaining'] = df_outcomes['flight_api']` was executed. Because `master_dataset_v0.csv` is ordered chronologically by mission/sample (SpX-15, SpX-16, SpX-17, NG-11, SpX-18, SpX-20), row $i$ received outcome $i$ from an unrelated drug.
2. **Incorrect `sample_id` Indexing in Legacy Mapping Table:** In `scratch/digitize_all_lots.py`, the `outcomes_list` dictionary manually assigned arbitrary sample IDs to drug groups (e.g., assigning `DS01_06`, which is Naloxone SpX-15, as the 2nd Caffeine lot; and assigning `DS01_11`, which is Epinephrine SpX-17, as the 2nd Diphenhydramine solution lot).

### Reconciliation Methodology & Authority
Every lot was reconciled directly against:
- **Primary Publication:** Nowadly et al. (2026) *Wilderness & Environmental Medicine*, Table 1 (Characteristics, dosage, packaging, manufacturer, days in space, days expired).
- **Primary Figures:** Figure 2 (Solid formulations: 2A Caffeine, 2B Diphenhydramine capsule, 2C Promethazine tablet) and Figure 3 (Nonsolid formulations: 3A Diazepam, 3B Diphenhydramine solution, 3C Epinephrine autoinjector, 3D Ketamine, 3E Lidocaine, 3F Naloxone, 3G Promethazine solution).
- **Statistical Texts:** Published two-way ANOVA $P$-values and Tukey's post-hoc results ($P<0.0001$ for Epinephrine; $P=0.0001$ for Promethazine tablet; $P=0.0080$ for Naloxone; $P=0.0125$ for Lidocaine; $P=0.0286$ for Diphenhydramine solution; $P=\text{ns}$ for Caffeine, Diazepam, Diphenhydramine capsule, Ketamine, and Promethazine solution).

### Disagreement Categorization Breakdown (32 Lots)
- **Category A (Naming / Order Mismatch Only):** 2 lots (DS01_01, DS01_32). Master v1 and mapping table matched the verified source values.
- **Category B (Incorrect Lot / Positional Mapping):** 29 lots. Resolved by matching mission and drug formulation to the corresponding panel in Figure 2 or Figure 3.
- **Category C (Incorrect Outcome Mapping / Panel Association):** 1 lot (DS01_20). Master v1 value matched by coincidence, but legacy mapping table pointed to the wrong panel.
- **Category D (Mission Mapping Mismatch):** 0 lots.
- **Category E (Rounding / Digitization Difference):** 0 lots.
- **Category F (Unresolved):** 0 lots. 100% of lots (32/32) are now verified.

### Artifacts Created:
- Reconciliation Table: [`results/tables/outcome_mapping_reconciliation.csv`](file:///d:/Space%20medicne/simulation/results/tables/outcome_mapping_reconciliation.csv)
- Proposed Corrected Master Dataset (v1 preserved untouched): [`data/processed/master_dataset_v2_proposed.csv`](file:///d:/Space%20medicne/simulation/data/processed/master_dataset_v2_proposed.csv)

---

## 2. Verification of Exact Exposure Dates and the 2–3 Day Shift

### Investigation of the Discrepancy
The Phase A audit identified a systematic 2–3 day shift across all exposure end dates. Investigation into `scratch/process_master_dataset.py` identified the mathematical source:
- In the legacy script: `start_date` was defined as the ISS arrival/berthing date ($T_{\text{docking}}$).
- The script then calculated `end_date` as: $\text{end\_date} = T_{\text{docking}} + \text{days\_in\_space}$.
- However, Nowadly et al. (2026) Table 1 and Methods explicitly define $\text{days\_in\_space}$ as **launch-to-landing duration** ($T_{\text{landing}} - T_{\text{launch}}$).
- Because orbital transit from launch to ISS berthing takes 2 to 3 days (e.g., SpX-15: 2018-06-29 launch to 2018-07-02 berthing = 3 days transit), adding $\text{days\_in\_space}$ to the arrival date pushed the legacy return date 2–3 days *past* actual Earth splashdown.

### Formal Exposure Phase Distinction
1. **Total Spaceflight Exposure Window:** Launch ($T_{\text{launch}}$) to Earth Splashdown / Landing ($T_{\text{landing}}$).
2. **ISS On-Orbit Storage Window:** Hatch opening / ISS Stowage ($T_{\text{docking}} + \Delta t_{\text{unpack}}$) to Cargo Transfer / Return Undocking ($T_{\text{undock}} - \Delta t_{\text{pack}}$).
3. **Ground Control Storage Window:** Ambient storage at JSC Pharmacy until analytical assay (March 2023).

### Reconciled Mission Windows Summary

| Mission | Lots | Launch Date | ISS Arrival Date | Reported Days in Space | Verified Landing Date | Legacy Shift (Hours) | Return Vehicle / Manifest |
|---|---:|---|---|---:|---|---:|---|
| SpX-15 | 2 | 2018-06-29 | 2018-07-02 | 199 | 2019-01-14 | +72 h | SpaceX CRS-15 Splashdown |
| SpX-15 | 6 | 2018-06-29 | 2018-07-02 | 424 | 2019-08-27 | +72 h | SpaceX CRS-18 Splashdown |
| SpX-16 | 2 | 2018-12-05 | 2018-12-08 | 265 | 2019-08-27 | +72 h | SpaceX CRS-18 Splashdown |
| NG-11 | 3 | 2019-04-17 | 2019-04-19 | 132 | 2019-08-27 | +48 h | Transferred to CRS-18 for splashdown |
| SpX-17 | 1 | 2019-05-04 | 2019-05-06 | 248 | 2020-01-07 | +48 h | SpaceX CRS-19 Splashdown |
| SpX-18 | 2 | 2019-07-25 | 2019-07-27 | 166 | 2020-01-07 | +48 h | SpaceX CRS-19 Splashdown |
| SpX-18 | 7 | 2019-07-25 | 2019-07-27 | 257 | 2020-04-07 | +48 h | SpaceX CRS-20 Splashdown |
| SpX-20 | 2 | 2020-03-07 | 2020-03-09 | 313 | 2021-01-14 | +48 h | SpaceX CRS-21 Splashdown |
| SpX-20 | 5 | 2020-03-07 | 2020-03-09 | 490 | 2021-07-10 | +48 h | SpaceX CRS-22 Splashdown |
| SpX-20 | 1 | 2020-03-07 | 2020-03-09 | 573 | 2021-10-01 | +48 h | SpaceX CRS-23 Splashdown |
| SpX-20 | 1 | 2020-03-07 | 2020-03-09 | 972 | 2022-11-04 | +48 h | SpaceX CRS-26 / Crew-4 Return |

### Artifacts Created:
- Exposure Date Table: [`results/tables/exposure_date_reconciliation.csv`](file:///d:/Space%20medicne/simulation/results/tables/exposure_date_reconciliation.csv)

---

## 3. Radiation Sensor Conflict Investigation

### Analysis of the 3,481 Conflicting Timestamps
The RadLab DOSIS-3D DosTel file (`RAD_ISS_Columbus_DosTel_2018_2022.csv`) contains 2,336,764 total rows covering 2018-06-01 to 2022-11-01.
Investigation of the duplicate timestamps revealed:
1. **Inter-instrument concurrency (118,383 timestamps):** DosTel1 and DosTel2 recorded simultaneously at the exact same second. This represents legitimate dual-channel semiconductor telescope operation.
2. **Intra-instrument duplicate records (3,481 timestamps / 6,962 rows):** The *same* detector (DosTel1: 1,218 pairs; DosTel2: 2,263 pairs) recorded two different absorbed dose rates at the exact same timestamp.

### Quantitative Disagreement Metrics

| Instrument | Conflicting Pairs | Mean Abs Diff ($\mu\text{Gy/h}$) | Median Abs Diff ($\mu\text{Gy/h}$) | Max Abs Diff ($\mu\text{Gy/h}$) | Mean Rel Diff (%) | Median Rel Diff (%) | Nature |
|---|---:|---:|---:|---:|---:|---:|---|
| **DosTel1** | 1,218 | 4.9740 | 0.3375 | 143.5330 | 10.91% | 6.80% | Non-systematic retry / packet overlap |
| **DosTel2** | 2,263 | 5.1053 | 0.2906 | 151.2170 | 10.21% | 6.12% | Non-systematic retry / packet overlap |
| **Combined** | **3,481** | **5.0593** | **0.3063** | **151.2170** | **10.45%** | **6.39%** | **Random ingestion chunk overlap** |

### Scientifically Justified Combination & Integration Policy:
1. **Preserve Channels Separately:** DosTel1 (telescope axis 1) and DosTel2 (telescope axis 2) must be preserved as distinct physical channels in raw archives.
2. **Deduplication Policy:** For dose rate integration across a single detector stream, duplicate timestamps for the same instrument are deduplicated by taking the arithmetic mean of the conflicting pair prior to trapezoidal time-integration.
3. **Cumulative Dose Calculation:** Cumulative absorbed dose ($\text{mGy}$) must be computed via trapezoidal integration over time: $\int D(t) dt$, bounded by the verified exposure window, rather than multiplying a pooled arithmetic mean rate by duration.

### Artifacts Created:
- Radiation Analysis Table: [`results/tables/radiation_conflict_analysis.csv`](file:///d:/Space%20medicne/simulation/results/tables/radiation_conflict_analysis.csv)

---

## 4 & 5. Environmental Telemetry Coverage & Storage Spatial Relevance

### Pharmaceutical Storage Location Investigation
According to Nowadly et al. (2026) Supplementary Figure S1 and Methods:
- Pharmaceuticals were deployed within the **ISS Crew Health Care System (CHeCS) / Health Maintenance System (HMS)** medical kits.
- Repackaged solid dosage forms (caffeine tablets) were stored in amber polymeric zipper-lock bags; manufacturer-packaged blisters and vials were stored in standard operational HMS kit compartments.
- HMS kits reside primarily in the **US Laboratory (Destiny)** module and Node 2.

### Sensor Spatial Relevance Grading
- **Grade A (Same Storage Location):** No internal logger inside the amber bags or HMS kit was present.
- **Grade B (Same Module):** US Lab general cabin sensors.
- **Grade C (Representative Nearby Cabin):** Node 2 / Node 1 cabin telemetry.
- **Grade D (ISS-Wide Module Proxy):** DOSIS-3D DosTel sensors in the European **Columbus** module (DOB2 rack).
- **Grade E (Unknown / Distant Habitat Proxy):** Rodent Research Express Rack telemetry (RR-7, RR-12, RR-19) labeled `_iss`.

---

## 6. Coverage Matrix and Usability Analysis

### Telemetry Coverage Heatmap

![Telemetry Coverage Heatmap V2](../results/figures/environment/telemetry_coverage_heatmap_v2.png)

### Summary Statistics across 32 Experimental Lots

| Variable | Mean Coverage | Median Coverage | Lots $>90\%$ | Lots $>75\%$ | Lots $>50\%$ | Lots $<50\%$ | Usability Classification |
|---|---:|---:|---:|---:|---:|---:|:---:|
| **Radiation (DosTel)** | **88.1%** | **89.0%** | 13 | 31 | 32 | 0 | **GREEN** |
| **Temperature** | **16.8%** | **14.6%** | 0 | 0 | 0 | 32 | **YELLOW** |
| **Relative Humidity** | **16.8%** | **14.6%** | 0 | 0 | 0 | 32 | **YELLOW** |
| **Carbon Dioxide ($\text{CO}_2$)** | **16.8%** | **14.6%** | 0 | 0 | 0 | 32 | **YELLOW** |
| **Cabin Pressure** | **0.0%** | **0.0%** | 0 | 0 | 0 | 32 | **RED** |
| **Oxygen ($\text{O}_2$)** | **0.0%** | **0.0%** | 0 | 0 | 0 | 32 | **RED** |

---

## 7. Usability Threshold Classifications & Rationale

1. **Radiation — GREEN (Primary Modeling Variable):**
   - *Rationale:* Temporal coverage averages 88.1% (median 89.0%), with 31/32 lots exceeding 75% coverage. DOSIS-3D DosTel instruments represent calibrated silicon semiconductor telescopes with well-characterized dosimetry response. Missingness consists of known operational maintenance gaps. Usable for primary cumulative dose integration.
2. **Temperature, Humidity, $\text{CO}_2$ — YELLOW (Secondary / Sensitivity Analysis Only):**
   - *Rationale:* Acquired historical records cover only 14.6% to 16.8% of flight windows (RR-7 in 2018, RR-12 in 2019, RR-19 in 2019–2020). There is zero cabin coverage for the extended 2020–2022 SpX-20 lots. They cannot serve as continuous exposure regressors in primary ML models without severe distortion, but can be utilized in sensitivity subsets.
3. **Pressure and Oxygen — RED (Excluded from Empirical Modeling):**
   - *Rationale:* 0.0% historical telemetry coverage across all missions. Substituting nominal cabin design standards (101.3 kPa, 21% $\text{O}_2$) would introduce constant synthetic artifacts masquerading as empirical spaceflight data.

---

## 8. Missing Telemetry Strategy — Analysis Only

| Strategy | Description | Scientific Advantages | Limitations & Risks | Phase A Recommendation |
|---|---|---|---|---|
| **Mission-Level Environmental Summaries** | Aggregate mission mean/median from observed segments | Captures macroscopic mission differences without inventing continuous time series | Mask high-frequency thermal excursions; biased if missingness is non-random | Candidate for Phase B exploratory features |
| **Short-Gap Linear Interpolation** | Interpolate gaps $<1$ hour | Preserves diurnal orbital cycling; minimal error across brief telemetry drops | Invalid across multi-week/month payload outages | Permissible only for radiation gaps $<1\text{ h}$ |
| **Multiple Imputation (MICE / PMM)** | Statistical imputation conditioned on flight duration and solar cycle | Quantifies imputation uncertainty across ensemble models | Fabricates high-dimensional pseudo-telemetry without physical ground truth | **DO NOT APPLY** to primary stability dataset |
| **Module-Level Proxy Models** | Use Columbus/Kibo thermal models to proxy US Lab | Leverages physics-based ISS ECLSS thermal equilibrium | Unmodeled local rack microclimates; high engineering overhead | Retain as contextual discussion only |
| **Complete-Case Sensitivity Analysis** | Restrict cabin models to lots with $>30\%$ telemetry | Mathematically unbiased on the observed subset | Reduces sample size from $N=32$ to $N=10$; reduces statistical power | **Mandatory sensitivity benchmark** in Phase B |

---

## 9. Multi-Criteria Exposure Confidence Framework

Each lot is assigned a multi-criteria confidence score based on:
1. **Outcome Certainty (100%):** HIGH across all 32 lots (verified against primary paper figures and ANOVA statistics).
2. **Exposure Boundaries (100%):** HIGH across all 32 lots (launch-to-landing dates reconciled against NASA flight records).
3. **Radiation Dosimetry:** HIGH for lots $\le 573$ days (coverage $\ge 85\%$); MEDIUM for 972-day lot (coverage 74.2%).
4. **Cabin Environment:** MEDIUM for 2018–2019 missions (15–38% coverage); LOW for 2020–2022 missions (0–8% coverage).
5. **Overall Exposure Reconstruction Confidence:** **MEDIUM (Robust for Radiation + Physicochemical + Formulation modeling; Exploratory for Cabin Microclimate).**

Artifact: [`results/tables/exposure_confidence_scores.csv`](file:///d:/Space%20medicne/simulation/results/tables/exposure_confidence_scores.csv)

---

## 10. Data Class Protection & Provenance Standards

To prevent leakage between empirical observations, derived parameters, and simulated predictions, all datasets in the simulation pipeline enforce four strict data classes:

```
├── [CLASS 1] MEASURED PHARMACEUTICAL OUTCOME
│   └── Ground-truth HPLC-MS/MS potency (% label), SD, ANOVA p-values (Nowadly et al. 2026)
├── [CLASS 2] MEASURED HISTORICAL TELEMETRY
│   └── Raw timestamped DOSIS-3D dose rates and EDA ECLSS sensor records (NASA OSDR / RadLab)
├── [CLASS 3] DERIVED EXPOSURE FEATURE
│   └── Integrated cumulative dose (mGy), verified duration (days), PubChem molecular descriptors
└── [CLASS 4] SIMULATED / MODEL-PREDICTED VALUE
    └── Machine learning predictions, vulnerability rankings, kinetic degradation rates
```

---

## Decision Table: Phase A Audit & Reconciliation

| Issue | Original Problem | Investigation Finding | Resolution | Remaining Uncertainty | Status |
|---|---|---|---|---|:---:|
| **Outcome Mapping** | 29/32 rows in `master_dataset_v1` disagreed with mapping table | Positional assignment bug in legacy script + mislabeled `sample_id`s in mapping table | Reconciled all 32 lots to Figures 2 & 3 and Table 1; generated `master_dataset_v2_proposed.csv` | Zero outcome ambiguity; assay uncertainty $\pm 2.5\%$ as published | **RESOLVED** |
| **Exposure Dates** | End dates shifted +2–3 days | Legacy script added launch-to-landing duration to ISS arrival date | Corrected start/end boundaries to launch-to-landing; documented ISS stowage intervals | Transfer hours from Dragon hatch opening to locker stowage ($\pm 12\text{ h}$) | **RESOLVED** |
| **Radiation Conflicts** | 3,481 duplicate timestamps with conflicting dose rates | Same-instrument duplicate records due to RadLab query chunking; mean relative error 10.4% | Preserved DosTel1/2 independently; established deduplication mean policy for time integration | Micro-dosimetric distribution inside specific medication lockers | **RESOLVED** |
| **Cabin Telemetry** | Cabin telemetry covers only 0–38% of mission windows | EDA payloads cover discrete intervals in 2018–2020; 2020–2022 unarchived | Classified Cabin as YELLOW (secondary subset only); Pressure/Oxygen as RED (excluded) | Long-term cabin microclimate during 2021–2022 | **RESOLVED (BOUNDED)** |

---

## Final Phase Decision

### **READY FOR PHASE B: YES**

**Justification:**
All four blocking data corruption and linkage issues identified in Phase A have been resolved:
1. The 32 pharmaceutical outcomes are traceably anchored to published experimental assays.
2. Spaceflight durations and exposure dates are verified against NASA mission flight records.
3. Radiation sensor conflicts are characterized, and a valid per-sensor integration policy is defined.
4. Telemetry availability has been rigorously audited, preventing invalid continuous imputation of missing cabin data while preserving high-quality radiation and molecular features.

The experimental chain $( \text{Drug/Lot} \rightarrow \text{Measured API Outcome} \rightarrow \text{Mission} \rightarrow \text{Exposure Window} \rightarrow \text{Radiation Dosimetry} \rightarrow \text{Molecular Descriptors} )$ is now defensible and verified.
