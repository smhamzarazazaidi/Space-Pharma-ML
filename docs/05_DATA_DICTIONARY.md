# 05. Empirical & Engineered Data Dictionary

**Project:** Interpretable Small-Data ML for Predicting Pharmaceutical Response and Stability Under Long-Duration Spaceflight Conditions  
**Primary Reference:** [`docs/RESEARCH_DOCUMENT.md`](file:///d:/Space%20medicne/docs/RESEARCH_DOCUMENT.md) (Section 9)  
**Audited Dataset:** `DS-01` (Nowadly et al., 2026, *Wilderness & Environmental Medicine*)

---

## 1. Primary Empirical Variables (`nowadly_2026_iss_medication_characteristics.csv`)

| Variable Name | Description | Measurement Unit | Data Type | Source Table | Missingness (%) | Chemical / Biological Meaning | ML Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `mission` | Spaceflight cargo/resupply mission ID | Categorical (String) | String | Table 1 | 0% | Mission environment and launch vehicle (SpX-15, SpX-16, SpX-17, NG-11, SpX-18, SpX-20) | Group Identifier / Context |
| `launch_date` | Mission launch date | YYYY-MM-DD | Date | Table 1 | 0% | Temporal anchor for space radiation solar cycle / ISS epoch | Metadata / Temporal Alignment |
| `medication` | Active Pharmaceutical Ingredient (API) entity | Categorical (String) | String | Table 1 | 0% | Active drug molecule (Caffeine, Diazepam, Diphenhydramine, Epinephrine, Ketamine, Lidocaine, Naloxone, Promethazine) | Entity Identifier / LODO Grouping |
| `formulation` | Physical dosage form | Categorical (String) | String | Table 1 | 0% | Physical state: Solid oral (Tablet, Capsule) vs. Liquid parenteral (Solution, Autoinjector) | Categorical Predictor |
| `dosage` | Labeled API strength per unit | mg or mg/mL | String | Table 1 | 0% | Nominal active ingredient concentration/amount on manufacturer label | Reference Metric |
| `days_in_space` | Duration from launch to landing aboard the ISS | Days ($d$) | Integer | Table 1 | 0% | Microgravity and ambient low-dose space radiation exposure duration (range: 132–972 d) | Primary Predictor (Flight Stressor) |
| `days_expired` | Duration from labeled expiration date to analytical testing | Days ($d$) | Integer | Table 1 | 0% | Total shelf-life degradation timeline including post-flight terrestrial storage (range: 549–1676 d) | Primary Predictor (Aging Stressor) |
| `manufacturer` | Commercial pharmaceutical manufacturer | Categorical (String) | String | Table S1 | 0% | Formulation excipient and manufacturing process source | Categorical Predictor / Excipient Proxy |
| `packaging` | In-flight containment barrier | Categorical (String) | String | Table S1 | 0% | Moisture/oxygen barrier: Amber ziplock (JSC), Blister pack (MFR), Single-dose vial (MFR), Multi-dose vial (MFR), Syringe (MFR) | Categorical Predictor (Barrier Quality) |

---

## 2. Analytical Chemistry & Instrument Variables (`nowadly_2026_supp_table_s2_analytical_calibrators.csv`, `nowadly_2026_supp_table_s3_ms_parameters.csv`)

| Variable Name | Description | Measurement Unit | Data Type | Source Table | Missingness (%) | Chemical Meaning | ML Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `target_concentration_ug_ml` | Target analytical concentration in assay | $\mu\text{g/mL}$ | Float | Table S2 | 0% | Assay target concentration | Quality Assurance Metadata |
| `calibrator_25pct_ug_ml` | 25% calibration standard | $\mu\text{g/mL}$ | Float | Table S2 | 0% | Lower analytical calibration point | Quality Assurance Metadata |
| `calibrator_50pct_ug_ml` | 50% calibration standard | $\mu\text{g/mL}$ | Float | Table S2 | 0% | Mid calibration point | Quality Assurance Metadata |
| `calibrator_100pct_ug_ml`| 100% calibration standard | $\mu\text{g/mL}$ | Float | Table S2 | 0% | Nominal 100% calibration point | Quality Assurance Metadata |
| `diluent` | Sample extraction solvent | Formula | String | Table S2 | 0% | 10% MeOH or 10% MeOH + 0.1% Formic Acid | Assay Protocol Metadata |
| `dilution_factor` | Sample dilution ratio | Numeric ratio | String | Table S2 | 0% | Volumetric dilution applied before UHPLC-MS/MS | Analytical Correction |
| `parent_ion_mz` | MS precursor ion mass-to-charge | $m/z$ | Float | Table S3 | 0% | Protonated molecular ion $[M+H]^+$ | Molecular Mass Verification |
| `daughter_ion_mz` | MS/MS product ion mass-to-charge | $m/z$ | Float | Table S3 | 0% | Characteristic fragmentation fragment | Specificity Verification |
| `retention_time_min` | UHPLC chromatographic retention time | Minutes ($\text{min}$) | Float | Table S3 | 0% | Hydrophobicity/column interaction indicator | Physicochemical Marker |
| `cone_voltage_v` | ESI source cone voltage | Volts (V) | Integer | Table S3 | 0% | Ionization parameter | Instrument Metadata |
| `collision_voltage_v` | Collision cell dissociation voltage | Volts (V) | Integer | Table S3 | 0% | Collision-induced dissociation energy | Instrument Metadata |
| `dwell_time_ms` | Multiple Reaction Monitoring dwell time | Milliseconds ($\text{ms}$) | Integer | Table S3 | 0% | Mass spectrometer scan duration | Instrument Metadata |

---

## 3. Environmental Exposure & Radiation Variables (`master_dataset_v1.csv`)

| Variable Name | Description | Measurement Unit | Data Type | Source | Missingness (%) | Scientific Meaning | ML Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `start_date` | Date medication lot arrived on ISS | YYYY-MM-DD | Date | Nowadly 2026 Table 1 & Manifests | 0% | ISS exposure window start | Context / Alignment |
| `end_date` | Date medication lot departed ISS | YYYY-MM-DD | Date | Nowadly 2026 Table 1 & Manifests | 0% | ISS exposure window end | Context / Alignment |
| `total_exposure_hours` | Duration of ISS storage in hours | Hours | Float | Derived ($24 \times \text{days}$) | 0% | Exposure time | Predictor |
| `radiation_measurements_count` | Number of DosTel telemetry records | Count | Integer | NASA RadLab DosTel 1+2 | 0% | Measurement sample size | Data Quality Indicator |
| `radiation_coverage_percent` | Percentage of mission window with telemetry | % | Float | NASA RadLab DosTel 1+2 | 0% | Temporal completeness | Data Quality Indicator |
| `mean_dose_rate_uGy_h` | Mean absorbed dose rate during lot window | $\mu\text{Gy/hour}$ | Float | NASA RadLab DosTel 1+2 | 0% | Average environmental ionizing radiation intensity | Predictor |
| `mean_daily_dose_rate_uGy_d` | Mean daily absorbed dose rate | $\mu\text{Gy/day}$ | Float | NASA RadLab DosTel 1+2 | 0% | Scaled daily radiation intensity | Predictor |
| `estimated_cumulative_iss_dose_mGy` | Integrated cumulative ambient absorbed dose | $\text{mGy}$ | Float | NASA RadLab DosTel 1+2 | 0% | Estimated cumulative ionizing radiation exposure in Columbus module | Primary Predictor (Radiation Stressor) |
| `dosimetry_nature` | Clarification of exposure measurement | Categorical | String | System Metadata | 0% | Ambient environmental estimate (not direct sample dosimeter) | Metadata / Provenance |

---

## 4. In Silico Physicochemical Drug Descriptors (`master_dataset_v1.csv`)

| Variable Name | Description | Measurement Unit | Data Type | Source | Missingness (%) | Chemical / Pharmacological Meaning | ML Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `pubchem_cid` | PubChem Compound ID | Integer | Integer | PubChem REST API | 0% | Unique molecular identifier | Identity |
| `molecular_weight_gmol` | Molecular Weight | $\text{g/mol}$ | Float | PubChem REST API | 0% | Molecular size | Predictor |
| `xlogp` | Octanol-water partition coefficient | Unitless | Float | PubChem REST API | 0% | Lipophilicity / Hydrophilicity balance | Predictor |
| `tpsa_angstrom2` | Topological Polar Surface Area | $\text{Å}^2$ | Float | PubChem REST API | 0% | Polar atom surface area / solvation capacity | Predictor |
| `rotatable_bonds` | Rotatable bond count | Count | Integer | PubChem REST API | 0% | Molecular flexibility | Predictor |
| `hbond_donors` | Hydrogen bond donor count | Count | Integer | PubChem REST API | 0% | Hydrogen bonding capability (solvation/oxidation) | Predictor |
| `hbond_acceptors` | Hydrogen bond acceptor count | Count | Integer | PubChem REST API | 0% | Hydrogen bonding capability | Predictor |
| `heavy_atom_count` | Heavy (non-H) atom count | Count | Integer | PubChem REST API | 0% | Skeletal complexity | Predictor |
| `molecular_complexity` | Bertz molecular complexity index | Unitless | Float | PubChem REST API | 0% | Structural complexity & stereochemical density | Predictor |
| `inchikey` | IUPAC International Chemical Identifier hash | String | String | PubChem REST API | 0% | Unique chemical key | Identity |
| `isomeric_smiles` | Isomeric SMILES representation | String | String | PubChem REST API | 0% | Molecular structure & stereochemistry | In Silico Vector |

---

## 5. Verified Quantitative Pharmaceutical Stability Outcomes (`master_dataset_v1.csv`)

| Variable Name | Description | Measurement Unit | Data Type | Source | Missingness (%) | Pharmaceutical Meaning | ML Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `flight_percent_api_remaining` | Spaceflight lot active ingredient content | `% of labeled claim` | Float | Nowadly 2026 Figures 2 & 3 | 0% | Measured API potency remaining after spaceflight | Primary Target Variable ($y_1$) |
| `ground_control_percent_api_remaining` | Terrestrial lot-matched control API content | `% of labeled claim` | Float | Nowadly 2026 Figures 2 & 3 | 0% | Baseline terrestrial degradation under 1g ambient storage | Comparator / Covariate |
| `relative_percent_diff_vs_control` | Relative difference vs terrestrial control | `%` | Float | Nowadly 2026 Fig 1-3 | 0% | Spaceflight-attributable potency delta: $\frac{\text{flight} - \text{ground}}{\text{ground}} \times 100$ | Secondary Target Variable ($y_2$) |
| `sd_flight_api` | Standard deviation across 10 analytical replicates | `% of labeled claim` | Float | Nowadly 2026 Figures 2 & 3 | 0% | Analytical assay measurement uncertainty (flight) | Uncertainty Weight |
| `sd_ground_control_api` | Standard deviation across 10 analytical replicates | `% of labeled claim` | Float | Nowadly 2026 Figures 2 & 3 | 0% | Analytical assay measurement uncertainty (ground) | Uncertainty Weight |
| `anova_p_value_exposure` | Two-way ANOVA spaceflight exposure main effect | String / P-value | String | Nowadly 2026 Figures 2 & 3 | 0% | Statistical significance of difference between flight and ground control | Statistical Annotation |
| `outcome_source` | Exact literature source citation | String | String | Nowadly et al. (2026) | 0% | Provenance reference | Quality Assurance |
| `outcome_extraction_method` | Method of numerical recovery | String | String | System Metadata | 0% | Calibrated optical digitization of UHPLC-MS/MS assay data | Quality Assurance |

