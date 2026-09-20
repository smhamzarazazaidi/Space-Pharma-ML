# Dataset Download & Provenance Policy

**Project:** Interpretable Small-Data ML for Predicting Pharmaceutical Response and Stability Under Long-Duration Spaceflight Conditions  
**Effective Date:** Phase 1 Dataset Audit  

---

## 1. Guiding Philosophy
In open science and biomedical research, dataset reproducibility and traceability are paramount. Every piece of data entering this repository must have an unambiguous provenance trail connecting it directly to an official repository, space agency archive, or peer-reviewed publication.

---

## 2. Manual Downloads Protocol

### When to Use Manual Download:
* The dataset is published as supplementary material attached to a journal article (e.g., journal `.xlsx` or `.pdf` tables).
* The data is embedded within paper figures or text tables requiring human verification.
* The repository does not provide a public, stable REST API.
* The dataset requires manual cross-referencing against flight logs and ground-control protocols prior to inclusion.
* The dataset license, access conditions, or experimental cohort must be verified before retrieval.

### Manual Download Checklist:
1. Identify the dataset and verify its peer-reviewed publication / official repository record.
2. Register the entry in [`data/DOWNLOAD_MANIFEST.csv`](file:///d:/Space%20medicne/data/DOWNLOAD_MANIFEST.csv) with status `READY_TO_DOWNLOAD`.
3. Download the unmodified raw file directly to the appropriate subfolder in `data/raw/`.
4. Update the manifest status to `DOWNLOADED` and record the local file path, file size, and download date.
5. Create a provenance card in `docs/RESEARCH_DOCUMENT.md` using the [`data/DATA_PROVENANCE_TEMPLATE.md`](file:///d:/Space%20medicne/data/DATA_PROVENANCE_TEMPLATE.md).
6. **NEVER edit the raw file directly.**

---

## 3. Automated Downloads Protocol

### When Automation May Be Used:
* The data provider hosts an official, public, and documented API (e.g., NASA OSDR REST API, NASA RadLab API, PubChem PUG-REST API).
* The exact study identifier (e.g., `OSDR-###`, PubChem CID) has already been audited and marked `READY_TO_DOWNLOAD` in `DOWNLOAD_MANIFEST.csv`.
* The download endpoint is permanent, versioned, and publicly accessible without credential abuse.
* The script records HTTP response headers, file checksums, download timestamps, and file sizes automatically.

### Acceptable Automated Sources:
* **NASA Open Science Data Repository (OSDR) API:** For retrieving specific, pre-audited study metadata and assay tables.
* **NASA RadLab API:** For programmatic retrieval of verified radiation dosimetry time-series.
* **PubChem PUG-REST / ChEMBL API:** For programmatic extraction of 2D/3D chemical properties matched to verified active pharmaceutical ingredients.

---

## 4. Strict Ethical & Access Constraints

> [!CAUTION]
> The following actions are strictly prohibited across all research stages:
> * **NO Aggressive Scraping:** Do not deploy scrapers or web crawlers against journal paywalls or un-API'd portals.
> * **NO Authentication Bypassing:** Never attempt to bypass logins, paywalls, or credentialed security barriers.
> * **NO Bulk Repository Dumps:** Never download entire repositories (e.g., downloading all 500+ OSDR studies) without targeted curation.
> * **NO In-Place Raw Editing:** Never modify, re-encode, or overwrite raw data in `data/raw/`.
> * **NO Synthetic / Fake Data:** Never generate placeholder CSV files containing simulated experimental values.

---

## 5. Downloader Software Standards

All download scripts placed in `src/data/downloaders/` must strictly enforce:
1. **Explicit Target Selection:** Only download explicitly specified and verified study IDs.
2. **Raw Preservation:** Default to refusing overwrite if the destination file already exists.
3. **Traceability:** Automatically record download timestamps, source URLs, and file sizes.
4. **Validation:** Use `src/data/validators/file_validator.py` to check file integrity post-download.
5. **Clear Error Reporting:** Log all HTTP status codes, network timeouts, and non-200 responses without crashing silently.
