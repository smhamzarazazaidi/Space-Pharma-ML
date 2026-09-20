# Raw Spaceflight Biological & Physiological Data

## 1. Data Classification
* **Category:** Biological, Transcriptomic, Proteomic, and Physiological Spaceflight Assays
* **Target Domain:** Biomarker responses, metabolomic signatures, oxidative stress pathways, and drug-metabolizing enzyme (CYP450) expression variations under spaceflight microgravity and radiation conditions.

## 2. Original Sources
* NASA Open Science Data Repository (OSDR) / GeneLab.
* NASA Life Sciences Data Archive (ALSDA).
* Peer-reviewed space biology studies.

## 3. Download Rules & Protocol
* Only download assays directly relevant to pharmacological response, liver metabolism, oxidative stress markers, or validated drug target pathways.
* All downloads must be registered in `data/DOWNLOAD_MANIFEST.csv` before saving.

## 4. Naming Convention
* Standard format: `OSDR-<study_id>_<assay_type>_<original_filename>.<ext>`
* Example: `OSDR-123_transcriptomic_cyp_expression.csv`

## 5. Raw Data Preservation Rules
* **IMMUTABLE:** Files in this directory must **never** be edited or transformed directly.
* Transformations, normalization, and filtering must be performed programmatically via code in `src/` and `notebooks/`.

## 6. Provenance Requirements
* Maintain full accession numbers (e.g., `OSDR-###`), study titles, flight mission metadata, and ground control descriptions in `docs/RESEARCH_DOCUMENT.md`.

## 7. Automated Downloading
* **Status:** ALLOWED ONLY via verified OSDR / GeneLab public REST APIs after study ID verification in Phase 1 Audit.

## 8. Current Status
* `STATUS: PENDING DATASET AUDIT #1`
* No raw datasets downloaded yet.
