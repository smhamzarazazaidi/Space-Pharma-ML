# 04. Dataset Inventory & Repository Registry

**Project:** Interpretable Small-Data ML for Predicting Pharmaceutical Response and Stability Under Long-Duration Spaceflight Conditions  
**Primary Reference:** [`docs/RESEARCH_DOCUMENT.md`](file:///d:/Space%20medicne/docs/RESEARCH_DOCUMENT.md) (Section 7)

---

## 1. Verified & Audited Dataset Inventory

| Dataset ID | Dataset Name | Source | Paper / Reference | DOI | Local File Path | Dataset Type | Samples ($n$) | Variables | Drugs | Spaceflight Duration | Ground Controls | Radiation Info | Biological Variables | Target Candidate | Missing Data | License | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DS-01** | ISS Multi-Mission Pharmaceutical Stability Assays (Nowadly 2026) | *Wilderness & Environmental Medicine* / USAF 59th MDW / COSMIC | Nowadly et al. (2026) | 10.1177/10806032261466966 | `data/raw/pharmaceutical_stability/nowadly_2026_iss_medication_characteristics.csv` | Tabular Experimental Assay (UHPLC-MS/MS) | 32 spaceflight lots paired with 32 lot-matched ground controls ($n=64$ total lots) | 9 sample attributes + 12 analytical parameters | 8 drugs (Caffeine, Diazepam, Diphenhydramine, Epinephrine, Ketamine, Lidocaine, Naloxone, Promethazine) | 132 to 972 days (mean: $340 \pm 180$ d) | Yes (32 lot-matched $1g$ ground controls stored under identical packaging and ambient conditions) | Ambient ISS GCR/trapped radiation (integrated via DS-02 DosTel telemetry) | None (pure pharmaceutical chemical stability) | % API Remaining, % Difference vs. Ground Control, Stability Threshold (<80%, 95–105%) | 0% in verified master dataset | Open Access / USAF FWH20230008N | `EXTRACTED & VERIFIED` |
| **DS-02** | ISS Environmental Radiation Dosimetry — DosTel 1+2 (DOSIS 3D) | NASA OSDR / RadLab | DOSIS 3D experiment (Berger et al. 2017) | Open RadLab Data | `data/raw/space_radiation/RAD_ISS_Columbus_DosTel_2018_2022.csv` | Environmental Time Series Telemetry | 2,336,764 readings (2018-06-01 to 2022-11-01) | Absorbed dose rate ($\mu\text{Gy/h}$), integrated cumulative mGy | *N/A* | Matched to SpX-15–SpX-20 mission dates (132 to 972 days) | *N/A* | DosTel1 & DosTel2 silicon semiconductor telescopes | *N/A* | Environmental cumulative radiation dose (`estimated_cumulative_iss_dose_mGy`) | 0% | Public Domain | `DOWNLOADED & INTEGRATED` |
| **DS-03** | Physicochemical Drug Descriptors | PubChem (NCBI / NIH) | Kim et al. (2023) | 10.1093/nar/gkac956 | `data/raw/drug_properties/ds03_pubchem_drug_descriptors_8compounds.csv` | In Silico Molecular Vectors | 8 compounds matched to DS-01 | MW, logP, TPSA, RotBonds, HBD, HBA, HeavyAtoms, Complexity, SMILES | 8 drugs from DS-01 | *N/A* | *N/A* | *N/A* | *N/A* | Physicochemical predictor vectors | 0% | Public Domain | `EXTRACTED & VERIFIED` |


---

## 2. Detailed Dataset Audit Summary for DS-01
* **Active Ingredients Studied (8 total):**
  1. *Caffeine* (Solid oral: 200 mg tablet, packaged in JSC amber ziplock bags)
  2. *Diazepam* (Liquid parenteral: 5 mg/mL solution, multi-dose vial)
  3. *Diphenhydramine* (Solid: 25 mg capsule in blister pack; Liquid: 50 mg/mL solution in single-dose vial)
  4. *Epinephrine* (Liquid parenteral: 0.1 mg/mL in Hospira autoinjector/syringe)
  5. *Ketamine* (Liquid parenteral: 50 mg/mL solution, multi-dose vial)
  6. *Lidocaine* (Liquid parenteral: 10 mg/mL solution, multi-dose vial)
  7. *Naloxone* (Liquid parenteral: 1 mg/mL solution, prefilled syringe)
  8. *Promethazine* (Solid: 25 mg tablet in blister pack; Liquid: 25 mg/mL solution in single-dose vial)
* **Spaceflight Exposure:** 6 ISS resupply missions (SpX-15, SpX-16, SpX-17, NG-11, SpX-18, SpX-20) covering 132 to 972 days in microgravity.
* **Terrestrial Controls:** All 32 spaceflight samples have exact lot-matched ground controls stored in parallel at Johnson Space Center and Lackland AFB.
