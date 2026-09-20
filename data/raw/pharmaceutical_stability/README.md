# Raw Pharmaceutical Stability Data

## 1. Data Classification
* **Category:** Primary Experimental Assays (Active Pharmaceutical Ingredient Stability)
* **Target Domain:** In-flight medication physical/chemical stability, potency retention (% API remaining), degradation rate constants ($k$), and impurity chromatography data from spaceflight and terrestrial control batches.

## 2. Original Sources
* Peer-reviewed space pharmacology literature (e.g., studies by Du et al., Chuong et al., Wotring et al.).
* NASA Life Sciences Data Archive (ALSDA) / NASA Open Science Data Repository (OSDR) pharmaceutical flight experiments.
* Associated ground-matched $1g$ terrestrial storage controls.

## 3. Download Rules & Protocol
* **Manual download preferred:** Most spaceflight pharmaceutical stability data are published in peer-reviewed journal tables, supplementary materials, or specialized archive packages requiring manual curation and verification.
* All downloads must be logged in `data/DOWNLOAD_MANIFEST.csv` prior to downloading.

## 4. Naming Convention
* Standard format: `<study_id>_<drug_name_or_batch>_<original_name>.<ext>`
* Example: `JSC2011_stability_assay_raw.xlsx`

## 5. Raw Data Preservation Rules
* **IMMUTABLE:** Files in this directory must **never** be edited, reformatted, or overwritten.
* All data cleaning, unit standardizations, and column harmonizations must be executed programmatically via `notebooks/02_data_cleaning.ipynb` and stored in `data/interim/`.

## 6. Provenance Requirements
* Every downloaded dataset in this directory must have a corresponding entry in `docs/04_DATASET_INVENTORY.md` and a completed `data/DATA_PROVENANCE_TEMPLATE.md` card in `docs/08_DATA_PROVENANCE.md` or `docs/RESEARCH_DOCUMENT.md`.

## 7. Automated Downloading
* **Status:** NOT ALLOWED without explicit manual verification.
* Programmatic downloading is only permissible when a verified, direct persistent URL / API is identified.

## 8. Current Status
* `STATUS: PENDING DATASET AUDIT #1`
* No raw datasets downloaded yet.
