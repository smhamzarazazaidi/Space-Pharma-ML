# DS-01 Pharmaceutical Outcome Extraction Status Report

## 1. Overview & Current Status

In accordance with strict scientific data integrity rules, **no synthetic or placeholder outcome measurements were fabricated**.

| Layer | Status | Content |
| :--- | :--- | :--- |
| **Medication Characteristics** | **EXTRACTED (Verified)** | 32 flown lots, mission, drug name, formulation, dosage, days in space, days expired, packaging, manufacturer. |
| **Quantitative Assay Outcomes** | **PENDING EXTRACTION** | Exact % API remaining for flown lots vs lot-matched ground controls. |

---

## 2. Where the Quantitative Outcomes Are Located

In the primary audited research paper:
* **Paper:** Nowadly et al. (2026), *Wilderness & Environmental Medicine*, DOI: `10.1177/10806032261466966`.
* **Figure 2:** Forest plot / bar plot displaying the mean percent active pharmaceutical ingredient (% API) remaining for each of the 32 spaceflight medication samples compared to their lot-matched ground controls.
* **Results Section:** Detailed text describing specific medication degrations (e.g. epinephrine liquid formulation stability versus solid formulations).

---

## 3. Extraction Protocol Required Before Machine Learning

1. **Extraction Source:** Table/Figure digitization or exact numerical values from Nowadly (2026) Figure 2.
2. **Target Columns to Populate:**
   - `flight_percent_api_remaining`: Measured API percentage of flown sample relative to label claim.
   - `ground_control_percent_api_remaining`: Measured API percentage of ground control lot relative to label claim.
   - `relative_percent_diff_vs_control`: `(flight - ground) / ground * 100`.
3. **Immutability Notice:** Once extracted from the primary document, these values will populate `master_dataset_v0.csv` to create `master_dataset_v1.csv` prior to exploratory data analysis (EDA) and modeling.
