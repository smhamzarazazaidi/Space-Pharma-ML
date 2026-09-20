# Master Project Structure & Repository Map

# Interpretable Small-Data ML for Predicting Pharmaceutical Response and Stability Under Long-Duration Spaceflight Conditions

---

## 1. Project Overview

### Research Initiative
**Title:** Interpretable Small-Data ML for Predicting Pharmaceutical Response and Stability Under Long-Duration Spaceflight Conditions  
**Domain:** Space Medicine, Aerospace Pharmacology, Microgravity Biophysics, Small-Data Statistical Learning, Explainable AI (XAI), Symbolic Regression  

### Scientific Context
Long-duration spaceflight (such as multi-year crewed missions to Mars, lunar Artemis basecamp stays, and deep-space transit) subjects astronauts and medical inventories to extreme multi-stressor conditions. These include microgravity ($\mu g$), chronic low-dose-rate ionizing cosmic radiation (Galactic Cosmic Rays [GCR] and Solar Particle Events [SPE]), altered spacecraft atmospheric composition (elevated $CO_2$, fluctuating humidity), and prolonged storage without terrestrial resupply.

Terrestrial shelf-lives and pharmacopeial standards (e.g., USP/ICH guidelines) assume controlled $1g$ ambient conditions with regular restock cycles. In exploration spaceflight, premature chemical degradation of active pharmaceutical ingredients (APIs), excipient breakdown, toxic degradation product formation, or microgravity-induced pharmacodynamic shifts could jeopardize astronaut health and mission safety.

### AI & Small-Data Philosophy
Because spaceflight experiments are inherently scarce, costly, and resource-constrained, space pharmacology datasets are characteristically small ($n < 1000$), multi-batch, and heterogeneous. This project prioritizes:
1. **Small-Data Statistical Learning:** Regularized linear models, ensemble trees, and kernel methods suited for low-sample tabular domains without over-parameterization.
2. **Explainable AI (XAI):** Rigorous feature attribution via SHAP (SHapley Additive exPlanations) and permutation importance.
3. **Symbolic Regression:** Closed-form mathematical discovery of candidate degradation equations $S_{\text{space}} = f(\text{radiation}, \text{duration}, \text{descriptors})$.
4. **Data Leakage Prevention:** Grouped validation (Leave-One-Drug-Out, Leave-One-Study-Out) with non-parametric bootstrap uncertainty quantification.

> [!IMPORTANT]
> **Scientific Integrity Notice:** The exact final research target (e.g., active ingredient potency retention, chemical degradation rate constant $k$, or biological response variation) will be established **strictly following the Phase 1 Dataset Audit** after inspecting actual empirical files from NASA Open Science Data Repository (OSDR) and peer-reviewed literature. No synthetic data, fake results, or premature physical claims are permitted.

---

## 2. Complete Repository Tree

```text
space-pharma-ml/
│
├── README.md                      # Project overview, policies, setup, and navigation
├── LICENSE                        # MIT Open Source License
├── .gitignore                     # Git version control ignore rules
├── requirements.txt               # Lightweight research Python dependencies
│
├── references/                    # Scientific literature and supplementary documents
│   ├── papers/                    # Downloaded research papers and NASA technical reports (.gitkeep)
│   └── supplementary/             # Supplementary files, extended tables, and appendices (.gitkeep)
│
├── docs/
│   ├── PROJECT_STRUCTURE.md       # Master map and architecture guide (this document)
│   ├── RESEARCH_DOCUMENT.md       # Central consolidated research document (Single Source of Truth)
│   ├── 00_RESEARCH_OVERVIEW.md    # High-level research summary and motivation
│   ├── 01_RESEARCH_QUESTION.md    # Formal research questions (RQ1–RQ5)
│   ├── 02_LITERATURE_REVIEW.md    # Systematic peer-reviewed literature notes
│   ├── 03_RESEARCH_GAP.md         # Documented empirical and computational gaps
│   ├── 04_DATASET_INVENTORY.md    # Verified candidate dataset registry
│   ├── 05_DATA_DICTIONARY.md      # Audited empirical variables and definitions
│   ├── 06_METHODOLOGY.md          # Statistical learning and modeling methodology
│   ├── 07_EXPERIMENT_PLAN.md      # Step-by-step 17-stage experimental protocol
│   ├── 08_RESULTS.md              # Experimental results and benchmark tracking (NOT YET RUN)
│   ├── 09_LIMITATIONS.md          # Explicit scientific, data, and clinical limitations
│   ├── 10_RESEARCH_LOG.md         # Chronological dated decision and discovery log
│   ├── 11_REFERENCES.md           # Verified bibliography and DOI registry
│   │
│   └── paper/
│       ├── manuscript.md          # Scientific paper draft
│       ├── figures.md             # Publication figures and captions plan
│       └── tables.md              # Publication tables plan
│
├── data/
│   ├── DOWNLOAD_MANIFEST.csv      # Registry tracking download status, licenses, and hashes
│   ├── DATA_PROVENANCE_TEMPLATE.md# Standardized metadata card template for downloaded datasets
│   ├── DOWNLOAD_POLICY.md         # Protocol governing manual vs. automated data retrieval
│   │
│   ├── raw/                       # Original unedited downloaded data files
│   │   ├── pharmaceutical_stability/
│   │   │   └── README.md          # Rules & provenance for stability assay data
│   │   ├── spaceflight_biological/
│   │   │   └── README.md          # Rules & provenance for OSDR/ALSDA biological data
│   │   ├── space_radiation/
│   │   │   └── README.md          # Rules & provenance for dosimetry data
│   │   └── drug_properties/
│   │       └── README.md          # Rules & provenance for chemical descriptors
│   │
│   ├── interim/                   # Cleaned, standardized intermediate data
│   ├── processed/                 # Final modeling matrices (sample × feature)
│   └── external/                  # Reference lookup tables, ontologies, SMILES
│
├── notebooks/
│   ├── 01_dataset_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_statistical_analysis.ipynb
│   ├── 05_baseline_models.ipynb
│   ├── 06_ml_models.ipynb
│   ├── 07_feature_selection.ipynb
│   ├── 08_interpretability.ipynb
│   ├── 09_symbolic_regression.ipynb
│   └── 10_validation.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data/                      # Loaders, provenance checks, audit scripts
│   │   ├── downloaders/           # Safe automated download utilities
│   │   │   ├── __init__.py
│   │   │   ├── osdr_downloader.py # NASA OSDR API downloader
│   │   │   └── radlab_downloader.py # NASA RadLab API downloader
│   │   └── validators/            # Data file integrity and checksum validators
│   │       ├── __init__.py
│   │       └── file_validator.py  # File non-emptiness & SHA-256 calculator
│   │
│   ├── features/                  # Domain feature calculators & descriptors
│   ├── models/                    # Model wrappers and symbolic regression interfaces
│   ├── evaluation/                # Grouped cross-validation & SHAP routines
│   └── visualization/             # Publication-grade plotting utilities
│
├── configs/
│   └── experiment_config.yaml     # Global hyperparameters, seeds, and path registry
│
├── models/                        # Serialized model checkpoints (.gitkeep)
│
└── results/
    ├── tables/                    # Performance spreadsheets and metric CSVs
    ├── figures/                   # Rendered high-resolution scientific plots
    ├── metrics/                   # JSON evaluation summaries and bootstrap CIs
    └── formulas/                  # Discovered symbolic closed-form equations
```

---

## 3. File-by-File Detailed Specification

### Root Configuration & Reference Files

#### File: `README.md`
* **Purpose:** Public portal, repository orientation, setup instructions, and research integrity statement.
* **Contains:** Project summary, compute constraints, reproducibility policy, folder map, and pointer to `docs/RESEARCH_DOCUMENT.md`.
* **Does NOT contain:** Raw datasets, scratch experiment logs, or speculative findings.
* **Updated when:** Project milestones or setup prerequisites change.
* **Depends on:** `docs/PROJECT_STRUCTURE.md`, `docs/RESEARCH_DOCUMENT.md`.

#### File: `LICENSE`
* **Purpose:** Legal licensing and distribution rights.
* **Contains:** MIT License terms for open-source academic research.
* **Does NOT contain:** Proprietary restrictions or scientific data.
* **Updated when:** Repository initialization.
* **Depends on:** N/A.

#### File: `.gitignore`
* **Purpose:** Specify files excluded from git version tracking.
* **Contains:** Rules for `__pycache__`, virtual environments, checkpoints, temporary artifacts, and large raw data files, while preserving directory `.gitkeep` files.
* **Does NOT contain:** Source code or documentation tracking rules.
* **Updated when:** New tools, environments, or artifact formats are introduced.
* **Depends on:** Repository directory layout.

#### File: `requirements.txt`
* **Purpose:** Python package dependency declarations for standard lightweight compute environments.
* **Contains:** Pinned packages (`numpy`, `pandas`, `scipy`, `scikit-learn`, `matplotlib`, `seaborn`, `xgboost`, `lightgbm`, `shap`, `openpyxl`, `jupyter`, `notebook`, `pyyaml`).
* **Does NOT contain:** Bloated deep-learning GPU stacks unnecessary for small-data tabular ML.
* **Updated when:** New lightweight libraries (e.g., symbolic regression engine) are confirmed viable post-audit.
* **Depends on:** Python 3.10+ virtual environment.

#### Directory: `references/` (`references/papers/`, `references/supplementary/`)
* **Purpose:** Permanent repository for downloaded full-text research papers, NASA technical reports, and supplementary tables.
* **Contains:** PDFs, supplementary spreadsheets, and document archives.
* **Does NOT contain:** Cleaned ML modeling data.
* **Updated when:** Papers are audited and verified during Phase 1 & 2.
* **Depends on:** Peer-reviewed literature discovery.

#### File: `configs/experiment_config.yaml`
* **Purpose:** Centralized configuration parameters for data paths, random seeds, and model hyperparameters.
* **Contains:** Directory mappings, random seed (42), grouped CV parameters, baseline and ML model registries.
* **Does NOT contain:** Hardcoded dataset values or raw data contents.
* **Updated when:** Dataset audit confirms the exact target column, groupings, and validation folds.
* **Depends on:** Audited dataset schema in `docs/05_DATA_DICTIONARY.md`.

---

### Data Management & Provenance Files (`data/`)

#### File: `data/DOWNLOAD_MANIFEST.csv`
* **Purpose:** Master registry tracking all candidate and downloaded datasets.
* **Contains:** Dataset ID, category, source, URL, paper citation, DOI, download method, local filename, file size, license, and status (`IDENTIFIED`, `TO_VERIFY`, `VERIFIED`, `READY_TO_DOWNLOAD`, `DOWNLOADED`, `INSPECTED`, `REJECTED`).
* **Does NOT contain:** Actual raw data rows.
* **Updated when:** Datasets are discovered, audited, downloaded, or rejected.
* **Depends on:** External scientific sources.

#### File: `data/DATA_PROVENANCE_TEMPLATE.md`
* **Purpose:** Standardized template for creating provenance metadata cards.
* **Contains:** Schema fields (Source, Study ID, DOI, Date, Filename, License, Experimental Conditions, Ground Controls, Limitations).
* **Does NOT contain:** Specific dataset instances.
* **Updated when:** Provenance logging requirements evolve.
* **Depends on:** Open science standards.

#### File: `data/DOWNLOAD_POLICY.md`
* **Purpose:** Governance protocol defining permissible manual and automated data acquisition rules.
* **Contains:** Manual download criteria, acceptable automated endpoints (NASA OSDR, RadLab, PubChem), and ethical access boundaries.
* **Does NOT contain:** Executable download code.
* **Updated when:** New repository APIs are approved.
* **Depends on:** Academic open access policies.

#### Files: `data/raw/*/README.md`
* **Purpose:** Folder-specific documentation and preservation rules for raw datasets.
* **Contains:** Data classification, sources, naming conventions, immutability rules, and provenance requirements for `pharmaceutical_stability/`, `spaceflight_biological/`, `space_radiation/`, and `drug_properties/`.
* **Does NOT contain:** Modified data.
* **Updated when:** Folder-level data scope changes.
* **Depends on:** Raw data folder hierarchy.

---

### Documentation Files (`docs/`)

#### File: `docs/PROJECT_STRUCTURE.md`
* **Purpose:** Master structural blueprint and repository navigation guide (this document).
* **Contains:** Comprehensive directory breakdown, file-by-file specification, data flow diagrams, research lifecycle phases, and version control guidelines.
* **Does NOT contain:** Raw assay data or unperformed experimental metrics.
* **Updated when:** Structural repository changes or major phase transitions occur.
* **Depends on:** Entire repository layout.

#### File: `docs/RESEARCH_DOCUMENT.md`
* **Purpose:** Central consolidated research document and primary Single Source of Truth.
* **Contains:** All 22 comprehensive research sections (Overview, Objectives, RQs, Hypotheses, Literature Review, Dataset Inventory, Provenance, Data Dictionary, Architecture, Methodology, Validation, Formulas, Experiments, Results, Figures, Limitations, Interpretation, Log, References, Open Questions, Next Steps).
* **Does NOT contain:** Fabricated data, synthetic numbers, or unverified claims.
* **Updated when:** Continuously across every research phase and after every major decision.
* **Depends on:** Verified empirical datasets, literature citations, and execution outputs.

#### File: `docs/00_RESEARCH_OVERVIEW.md`
* **Purpose:** Dedicated high-level modular overview of project motivation, spaceflight stressor domains, and computational philosophy.
* **Contains:** Working title, research domain, project summary, exploration context, and phase tracking.
* **Does NOT contain:** Raw data tables or low-level implementation code.
* **Updated when:** High-level project scope or phase status is updated.
* **Depends on:** `docs/RESEARCH_DOCUMENT.md` (Section 1).

#### File: `docs/01_RESEARCH_QUESTION.md`
* **Purpose:** Formal itemization and breakdown of research questions and preliminary working hypotheses.
* **Contains:** Detailed statements for RQ1 (Harmonization), RQ2 (Algorithm Benchmarks), RQ3 (Feature Attribution), RQ4 (Formula Discovery), RQ5 (Extrapolation Validation), and hypothesis statements.
* **Does NOT contain:** Speculative answers prior to data analysis.
* **Updated when:** Dataset audit refines the operational target variable.
* **Depends on:** `docs/RESEARCH_DOCUMENT.md` (Sections 2, 3, 4).

#### File: `docs/02_LITERATURE_REVIEW.md`
* **Purpose:** Systematic record of peer-reviewed space pharmacology, stability, and space biology literature.
* **Contains:** Author, Year, Title, Journal, DOI, URL, Dataset used, Methods, Findings, Limitations, Relevance, and Differentiators for each audited paper.
* **Does NOT contain:** Non-existent papers, AI-hallucinated citations, or unverified DOIs.
* **Updated when:** Literature search and citation verification are conducted.
* **Depends on:** Peer-reviewed publications and PubMed/NASA technical reports.

#### File: `docs/03_RESEARCH_GAP.md`
* **Purpose:** Detailed articulation of the specific empirical and methodological research gaps.
* **Contains:** Synthesis of prior work limitations, lack of cross-compound ML models, absence of closed-form degradation equations, and grouped leakage vulnerabilities.
* **Does NOT contain:** Sweeping unsubstantiated claims dismissive of existing space medicine research.
* **Updated when:** Literature review is completed.
* **Depends on:** `docs/02_LITERATURE_REVIEW.md`.

#### File: `docs/04_DATASET_INVENTORY.md`
* **Purpose:** Complete tabular registry of all candidate spaceflight and reference datasets.
* **Contains:** Dataset ID, Name, Source (NASA OSDR, ALSDA, etc.), DOI, URL, Type, Samples ($n$), Variables, Target, Missingness, License, and Audit Status.
* **Does NOT contain:** Actual raw data rows or synthetic records.
* **Updated when:** Datasets are identified, downloaded, and audited.
* **Depends on:** NASA OSDR / ALSDA repository metadata and published tables.

#### File: `docs/05_DATA_DICTIONARY.md`
* **Purpose:** Definitive schema and metadata for all empirical and engineered variables.
* **Contains:** Variable name, Description, Measurement Unit, Data Type, Source, Missing Values, Biological/Chemical Meaning, and ML Role (Feature, Target, Group Identifier).
* **Does NOT contain:** Imagined variables before raw file audit.
* **Updated when:** Raw files are inspected in `notebooks/01_dataset_exploration.ipynb`.
* **Depends on:** `data/raw/` and `notebooks/01_dataset_exploration.ipynb`.

#### File: `docs/06_METHODOLOGY.md`
* **Purpose:** Comprehensive technical documentation of data preparation, modeling, interpretability, and validation algorithms.
* **Contains:** Mathematical formulations for linear baselines, tree ensembles, SVR, SHAP attributions, symbolic regression Pareto optimization, and bootstrap CI estimation.
* **Does NOT contain:** Results or execution logs.
* **Updated when:** Methodological decisions or algorithm selections are finalized.
* **Depends on:** `docs/RESEARCH_DOCUMENT.md` (Sections 11, 12, 13).

#### File: `docs/07_EXPERIMENT_PLAN.md`
* **Purpose:** Step-by-step procedural guide for conducting the 17-stage research workflow.
* **Contains:** Sequential checklist from Dataset Audit to Paper Preparation, detailing required inputs, execution scripts/notebooks, and validation checkpoints.
* **Does NOT contain:** Experimental results.
* **Updated when:** Workflow stages progress or protocols are refined.
* **Depends on:** `docs/RESEARCH_DOCUMENT.md` (Section 14).

#### File: `docs/08_RESULTS.md`
* **Purpose:** Tracking document for all empirical evaluation metrics, model comparisons, and discovered formulas.
* **Contains:** Baseline scores, classical ML benchmark tables, SHAP feature rankings, and symbolic regression candidates—all marked `NOT YET RUN` until executed.
* **Does NOT contain:** Fabricated metrics, placeholder estimates, or simulated curves.
* **Updated when:** Notebooks `05_baseline_models.ipynb` through `10_validation.ipynb` are executed on real data.
* **Depends on:** `results/metrics/`, `results/tables/`, `results/formulas/`.

#### File: `docs/09_LIMITATIONS.md`
* **Purpose:** Transparent documentation of scientific, experimental, computational, and clinical boundaries.
* **Contains:** Discussion of small sample sizes ($n$), heterogeneous flight stowage temperatures, lack of human in-flight PK/PD data, LEO vs. deep-space GCR differences, and model-derived boundaries.
* **Does NOT contain:** Defensive omissions of research constraints.
* **Updated when:** Dataset audit and validation reveal domain boundaries.
* **Depends on:** `docs/RESEARCH_DOCUMENT.md` (Section 17).

#### File: `docs/10_RESEARCH_LOG.md`
* **Purpose:** Chronological, dated laboratory notebook capturing decisions, discoveries, and pivots.
* **Contains:** Timestamped entries (Date, Action, Dataset/Paper, Discovery, Decision, Reason, Next Step).
* **Does NOT contain:** Retrospective fabrications of research history.
* **Updated when:** After every research session, decision, or audit phase.
* **Depends on:** Ongoing research activity.

#### File: `docs/11_REFERENCES.md`
* **Purpose:** Fully formatted scientific bibliography and DOI library.
* **Contains:** Verified citations in APA/Vancouver format with direct persistent URLs and verified DOIs.
* **Does NOT contain:** Hallucinated citations or unverified URLs.
* **Updated when:** New verified papers are integrated into the research.
* **Depends on:** `docs/02_LITERATURE_REVIEW.md`.

#### Files: `docs/paper/manuscript.md`, `figures.md`, `tables.md`
* **Purpose:** Scientific manuscript drafting workspace for academic journal submission.
* **Contains:** Introduction, Related Work, Methods, Results (populated from real data), Discussion, Conclusion, figure captions, and publication tables.
* **Does NOT contain:** Fictional results.
* **Updated when:** Experimental phases 8–13 are validated and ready for synthesis.
* **Depends on:** `docs/08_RESULTS.md`, `results/figures/`, `results/tables/`.

---

### Jupyter Notebooks (`notebooks/`)

#### File: `notebooks/01_dataset_exploration.ipynb`
* **Purpose:** Initial audit, column inspection, missing value profiling, and study distribution analysis of raw files.
* **Contains:** Data inspection routines, missingness matrices, and summary statistics.
* **Does NOT contain:** In-place mutations of raw files or model training.
* **Updated when:** New raw dataset files are placed in `data/raw/`.
* **Depends on:** `data/raw/`, `src/data/`.

#### File: `notebooks/02_data_cleaning.ipynb`
* **Purpose:** Unit harmonization (time in orbit, radiation mGy/mSv), missing value imputation, and chemical nomenclature standardization.
* **Contains:** Cleaning pipelines exporting intermediate tables to `data/interim/`.
* **Does NOT contain:** Loss of original raw data files.
* **Updated when:** Cleaning rules are defined following exploration.
* **Depends on:** `data/raw/`, `notebooks/01_dataset_exploration.ipynb`.

#### File: `notebooks/03_feature_engineering.ipynb`
* **Purpose:** Calculate domain-specific interaction features (radiation × duration) and physicochemical descriptors (MW, logP, TPSA, rotatable bonds).
* **Contains:** Feature transformation scripts outputting model-ready matrices to `data/processed/`.
* **Does NOT contain:** Final model training.
* **Updated when:** Processed feature set is refined.
* **Depends on:** `data/interim/`, `src/features/`.

#### File: `notebooks/04_statistical_analysis.ipynb`
* **Purpose:** Conduct rigorous non-parametric hypothesis testing (Mann-Whitney U, Kruskal-Wallis) and rank correlation analyses.
* **Contains:** Statistical test executions comparing flight vs. ground-matched controls and bivariate correlation heatmaps.
* **Does NOT contain:** Machine learning model training.
* **Updated when:** Processed data matrix is stabilized.
* **Depends on:** `data/processed/`.

#### File: `notebooks/05_baseline_models.ipynb`
* **Purpose:** Benchmark trivial non-learning baselines (Mean, Median) and regularized linear regressors (OLS, Ridge, Lasso).
* **Contains:** Benchmark training and baseline performance logging using grouped CV.
* **Does NOT contain:** Complex non-linear ML models.
* **Updated when:** Baselines are trained on processed data.
* **Depends on:** `data/processed/`, `src/models/`, `configs/experiment_config.yaml`.

#### File: `notebooks/06_ml_models.ipynb`
* **Purpose:** Train and evaluate classical machine learning models (Random Forest, XGBoost, LightGBM, SVR, k-NN) suited for small tabular datasets.
* **Contains:** Hyperparameter tuning, cross-validation metrics, and model artifact serialization.
* **Does NOT contain:** Data leakage across drug/study batches.
* **Updated when:** ML experiments are executed.
* **Depends on:** `data/processed/`, `src/models/`, `src/evaluation/`.

#### File: `notebooks/07_feature_selection.ipynb`
* **Purpose:** Identify minimal, robust predictive feature subsets to prevent overfitting in small-sample regimes.
* **Contains:** L1 penalty paths, Recursive Feature Elimination (RFE), and permutation importance rankings.
* **Does NOT contain:** Unjustified feature pruning without cross-validation stability checks.
* **Updated when:** Feature reduction is performed.
* **Depends on:** `notebooks/06_ml_models.ipynb`.

#### File: `notebooks/08_interpretability.ipynb`
* **Purpose:** Compute TreeSHAP and KernelSHAP values to explain model predictions globally and locally.
* **Contains:** SHAP summary beeswarm plots, feature dependence plots, and interaction attributions saved to `results/figures/`.
* **Does NOT contain:** Unexplained black-box model outputs.
* **Updated when:** Best-performing models are finalized.
* **Depends on:** `models/`, `notebooks/06_ml_models.ipynb`, `src/evaluation/`.

#### File: `notebooks/09_symbolic_regression.ipynb`
* **Purpose:** Discover closed-form mathematical equations $S_{\text{space}} = f(\dots)$ balancing accuracy and complexity along the Pareto frontier.
* **Contains:** Genetic programming / symbolic regression fits, equation exports to `results/formulas/`.
* **Does NOT contain:** Manually invented equations disguised as empirical discoveries.
* **Updated when:** Symbolic regression is executed post-ML benchmarking.
* **Depends on:** `data/processed/`, `notebooks/07_feature_selection.ipynb`.

#### File: `notebooks/10_validation.ipynb`
* **Purpose:** Execute out-of-distribution grouped validation (Leave-One-Drug-Out, Leave-One-Study-Out), 95% bootstrap CIs, and perturbation sensitivity testing.
* **Contains:** Final validation suite, residual analysis, sensitivity simulations, and metric export to `results/metrics/`.
* **Does NOT contain:** Optimistic random train/test splits.
* **Updated when:** Final model validation is performed.
* **Depends on:** `notebooks/06_ml_models.ipynb`, `notebooks/09_symbolic_regression.ipynb`.

---

### Python Source Modules (`src/`)

* **`src/__init__.py`:** Package initialization and version declaration (`0.1.0`).
* **`src/data/__init__.py`:** Data loaders, validation helpers, and acquisition interfaces.
* **`src/data/downloaders/`:**
  * `__init__.py`: Downloader exports.
  * `osdr_downloader.py`: Verified NASA OSDR REST API metadata and assay retriever.
  * `radlab_downloader.py`: NASA RadLab radiation dosimetry retriever.
* **`src/data/validators/`:**
  * `__init__.py`: Validator exports.
  * `file_validator.py`: Non-emptiness check, format parsing, and SHA-256 cryptographic provenance hasher.
* **`src/features/__init__.py`:** Physicochemical descriptor extractors (RDKit / PubChem wrappers) and environmental stressor interaction functions.
* **`src/models/__init__.py`:** Standardized sklearn-compatible wrappers for baseline regressors, tree ensembles, and symbolic regression interfaces.
* **`src/evaluation/__init__.py`:** Custom cross-validators (`LeaveOneDrugOut`, `GroupKFoldCV`), bootstrap confidence interval estimators, and SHAP explainers.
* **`src/visualization/__init__.py`:** Publication-grade figure generators adhering to clear scientific typography, high DPI, and consistent color palettes.

---

## 4. Folder-by-Folder Specification

| Directory | Primary Purpose | What Belong There | What Does NOT Belong There |
| :--- | :--- | :--- | :--- |
| `references/` | Literature repository | Full-text PDFs (`papers/`) and supplementary tables (`supplementary/`) | Cleaned ML datasets |
| `docs/` | Comprehensive scientific documentation | Central research document, modular docs, master map, paper drafts | Raw data, binary checkpoints, executable code |
| `data/raw/` | Permanent archive of downloaded datasets | Original, unedited CSV, Excel, TXT, or JSON files from verified repositories | Modified files, cleaned data, generated columns |
| `data/interim/` | Intermediate standardized datasets | Harmonized tables, unit-converted data, imputed working files | Raw untouched downloads, final ML matrices |
| `data/processed/` | Final model-ready tabular matrices | Standardized $X, y, G$ arrays ready for direct ML consumption | Raw data, unverified intermediate drafts |
| `data/external/` | Auxiliary reference datasets | PubChem chemical properties, SMILES lookups, GCR radiation tables | Primary experimental target data |
| `notebooks/` | Sequential research execution environment | Interactive Jupyter notebooks (01 to 10) with code and visualizations | Production backend code, heavy ETL pipelines |
| `src/` | Modular, testable Python package | Reusable functions, classes, custom CV splitters, plotting helpers | Ad-hoc one-off experiment scripts, raw data |
| `src/data/downloaders/`| Safe data acquisition scripts | Controlled OSDR / RadLab API retrieval utilities | Aggressive web scrapers |
| `src/data/validators/` | File integrity checkers | Cryptographic hashers and structure verifiers | Destructive in-place file mutators |
| `configs/` | Centralized experiment configuration | YAML files defining seeds, paths, hyperparameter grids | Hardcoded data samples, secret credentials |
| `models/` | Trained model artifact storage | Serialized `.pkl`, `.joblib`, or `.json` model checkpoints | Raw data, un-versioned scratch checkpoints |
| `results/tables/` | Tabular scientific results | Performance comparison spreadsheets, summary CSVs | Raw datasets, intermediate logs |
| `results/figures/` | High-resolution publication figures | Vector/raster figures (PNG, PDF, SVG at 300+ DPI) | Low-res exploratory scratch plots |
| `results/metrics/` | Evaluation metrics and logs | JSON/YAML files containing RMSE, MAE, $R^2$, bootstrap CIs | Intermediate unvalidated debug logs |
| `results/formulas/` | Discovered mathematical equations | Markdown/LaTeX text files of symbolic regression equations | Arbitrary unverified text |

---

## 5. End-to-End Data Flow

```text
       ┌─────────────────────────────────────────────────────────┐
       │     External Scientific Sources (NASA OSDR, ALSDA,     │
       │          Peer-Reviewed Pharmaceutical Studies)          │
       └────────────────────────────┬────────────────────────────┘
                                    │ (Download unedited raw files)
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │             data/raw/ (Permanent Immature Data)          │
       │   pharmaceutical_stability/ | spaceflight_biological/   │
       │         space_radiation/    | drug_properties/          │
       └────────────────────────────┬────────────────────────────┘
                                    │ (Audit in notebooks/01)
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │                   Phase 1: Dataset Audit                │
       │          (Document provenance, inspect variables)       │
       └────────────────────────────┬────────────────────────────┘
                                    │ (Harmonize & clean in notebooks/02)
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │             data/interim/ (Standardized Units)          │
       └────────────────────────────┬────────────────────────────┘
                                    │ (Feature engineering in notebooks/03)
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │             data/processed/ (Final ML Matrix)           │
       │       Features (X) + Target (y) + Group IDs (G)         │
       └────────────────────────────┬────────────────────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
┌─────────────────────────────┐                   ┌─────────────────────────────┐
│ 04_statistical_analysis.ipynb│                  │  05_baseline_models.ipynb   │
│ (Hypothesis tests, $\rho$)  │                  │  (Mean, Median, OLS, Ridge) │
└──────────┬──────────────────┘                   └──────────────┬──────────────┘
           │                                                     │
           └────────────────────────┬────────────────────────────┘
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │                 06_ml_models.ipynb                      │
       │ (Random Forest, XGBoost, LightGBM, SVR, k-NN)           │
       └────────────────────────────┬────────────────────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
┌─────────────────────────────┐                   ┌─────────────────────────────┐
│ 07_feature_selection.ipynb  │                   │ 09_symbolic_regression.ipynb│
│ (RFE, L1, Permutation Imp.) │                   │ (Discovered Equations)      │
└──────────┬──────────────────┘                   └──────────────┬──────────────┘
           │                                                     │
           ▼                                                     │
┌─────────────────────────────┐                                  │
│  08_interpretability.ipynb  │                                  │
│   (TreeSHAP, Beeswarm plots)│                                  │
└──────────┬──────────────────┘                                  │
           │                                                     │
           └────────────────────────┬────────────────────────────┘
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │                 10_validation.ipynb                     │
       │   (Leave-One-Drug-Out, Leave-One-Study-Out,             │
       │    95% Bootstrap CIs, Perturbation Sensitivity)         │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │                        results/                         │
       │   tables/  |  figures/  |  metrics/  |  formulas/       │
       └────────────────────────────┬────────────────────────────┘
                                    │
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │           docs/paper/ & docs/RESEARCH_DOCUMENT.md       │
       │          (Synthesized Manuscript & Findings)            │
       └─────────────────────────────────────────────────────────┘
```

---

## 6. Research Lifecycle & Phase Breakdown

```text
PHASE 1: Research Question & Scope Definition
   ↓
PHASE 2: Literature Review & Gap Analysis
   ↓
PHASE 3: Dataset Audit & Provenance Verification
   ↓
PHASE 4: Data Preparation & Standardization
   ↓
PHASE 5: Exploratory Data Analysis (EDA)
   ↓
PHASE 6: Statistical Analysis & Hypothesis Testing
   ↓
PHASE 7: Baseline Modeling
   ↓
PHASE 8: Classical Machine Learning Benchmarking
   ↓
PHASE 9: Regularized Feature Selection
   ↓
PHASE 10: Explainable AI & SHAP Interpretability
   ↓
PHASE 11: Symbolic Regression & Equation Discovery
   ↓
PHASE 12: Robust Out-of-Distribution Validation
   ↓
PHASE 13: Scientific Interpretation & Limitations
   ↓
PHASE 14: Manuscript & Publication Preparation
```

### Detailed Phase Specifications:

* **PHASE 1: Research Question & Scope**
  * *Objective:* Establish research boundary conditions and preliminary hypotheses.
  * *Input:* Domain challenges in space medicine and long-duration mission planning.
  * *Files Used:* `docs/01_RESEARCH_QUESTION.md`, `docs/RESEARCH_DOCUMENT.md`.
  * *Expected Output:* Explicit RQs (RQ1–RQ5) and testable working hypotheses.
  * *Where Saved:* `docs/01_RESEARCH_QUESTION.md`.

* **PHASE 2: Literature Review & Gap Analysis**
  * *Objective:* Systematically document verified spaceflight pharmaceutical literature without hallucination.
  * *Input:* Peer-reviewed publications from NASA, ESA, JAXA, and pharmacology journals.
  * *Files Used:* `docs/02_LITERATURE_REVIEW.md`, `docs/03_RESEARCH_GAP.md`, `docs/11_REFERENCES.md`.
  * *Expected Output:* Verified citation cards with documented findings and limitations.
  * *Where Saved:* `docs/02_LITERATURE_REVIEW.md`, `docs/11_REFERENCES.md`.

* **PHASE 3: Dataset Audit & Provenance Verification (CURRENT)**
  * *Objective:* Discover, download, and catalog candidate spaceflight datasets; verify real target variables.
  * *Input:* NASA OSDR, ALSDA, space radiation repositories.
  * *Files Used:* `notebooks/01_dataset_exploration.ipynb`, `docs/04_DATASET_INVENTORY.md`, `docs/05_DATA_DICTIONARY.md`.
  * *Expected Output:* Unmodified raw files in `data/raw/` and populated data dictionaries.
  * *Where Saved:* `data/raw/`, `docs/04_DATASET_INVENTORY.md`, `docs/05_DATA_DICTIONARY.md`.

* **PHASE 4: Data Preparation & Harmonization**
  * *Objective:* Clean and harmonize multi-study tables without overwriting raw files.
  * *Input:* Raw datasets in `data/raw/`.
  * *Files Used:* `notebooks/02_data_cleaning.ipynb`, `notebooks/03_feature_engineering.ipynb`, `src/data/`, `src/features/`.
  * *Expected Output:* Cleaned tables in `data/interim/` and final matrices in `data/processed/`.
  * *Where Saved:* `data/interim/`, `data/processed/`.

* **PHASE 5: Exploratory Data Analysis (EDA)**
  * *Objective:* Profile sample distributions, missingness, and flight duration spans.
  * *Input:* `data/processed/`.
  * *Files Used:* `notebooks/01_dataset_exploration.ipynb`, `src/visualization/`.
  * *Expected Output:* Univariate distributions and bivariate exploratory plots.
  * *Where Saved:* `results/figures/`.

* **PHASE 6: Statistical Analysis & Hypothesis Testing**
  * *Objective:* Test statistical significance between flight samples and ground controls.
  * *Input:* `data/processed/`.
  * *Files Used:* `notebooks/04_statistical_analysis.ipynb`.
  * *Expected Output:* Non-parametric p-values, rank correlation matrices, and effect sizes.
  * *Where Saved:* `results/tables/`, `docs/08_RESULTS.md`.

* **PHASE 7: Baseline Modeling**
  * *Objective:* Establish non-learning and linear baselines.
  * *Input:* `data/processed/`, `configs/experiment_config.yaml`.
  * *Files Used:* `notebooks/05_baseline_models.ipynb`, `src/models/`.
  * *Expected Output:* Benchmark RMSE, MAE, and $R^2$ scores.
  * *Where Saved:* `results/metrics/`, `docs/08_RESULTS.md`.

* **PHASE 8: Classical Machine Learning Benchmarking**
  * *Objective:* Train small-data ML models (Random Forest, XGBoost, LightGBM, SVR, k-NN).
  * *Input:* `data/processed/`, `configs/experiment_config.yaml`.
  * *Files Used:* `notebooks/06_ml_models.ipynb`, `src/models/`, `src/evaluation/`.
  * *Expected Output:* Comparative model leaderboard with grouped CV scores.
  * *Where Saved:* `results/metrics/`, `models/`, `docs/08_RESULTS.md`.

* **PHASE 9: Regularized Feature Selection**
  * *Objective:* Identify the most parsimonious predictive subset to prevent overfitting.
  * *Input:* Trained models and feature matrices.
  * *Files Used:* `notebooks/07_feature_selection.ipynb`.
  * *Expected Output:* Ranked feature lists and reduced feature matrices.
  * *Where Saved:* `results/tables/`.

* **PHASE 10: Explainable AI & Interpretability**
  * *Objective:* Calculate SHAP attributions for transparent scientific explanation.
  * *Input:* Best-performing ML models and processed test folds.
  * *Files Used:* `notebooks/08_interpretability.ipynb`, `src/evaluation/`.
  * *Expected Output:* SHAP beeswarm and feature interaction plots.
  * *Where Saved:* `results/figures/`.

* **PHASE 11: Symbolic Regression & Equation Discovery**
  * *Objective:* Discover candidate mathematical formulations $S_{\text{space}} = f(\dots)$.
  * *Input:* Selected feature subsets and empirical targets.
  * *Files Used:* `notebooks/09_symbolic_regression.ipynb`.
  * *Expected Output:* Parsimonious mathematical formulas and Pareto frontier curves.
  * *Where Saved:* `results/formulas/`, `results/figures/`.

* **PHASE 12: Robust Out-of-Distribution Validation**
  * *Objective:* Validate models via Leave-One-Drug-Out and bootstrap confidence intervals.
  * *Input:* Final models, discovered equations, and grouped datasets.
  * *Files Used:* `notebooks/10_validation.ipynb`, `src/evaluation/`.
  * *Expected Output:* 95% bootstrap CIs and perturbation sensitivity envelopes.
  * *Where Saved:* `results/metrics/`, `results/tables/`.

* **PHASE 13: Scientific Interpretation & Limitations**
  * *Objective:* Synthesize findings across the 6 evidence tiers and document limitations.
  * *Input:* Validation outputs, SHAP explanations, and domain context.
  * *Files Used:* `docs/09_LIMITATIONS.md`, `docs/RESEARCH_DOCUMENT.md`.
  * *Expected Output:* Structured scientific interpretation distinguishing prediction from clinical validation.
  * *Where Saved:* `docs/RESEARCH_DOCUMENT.md` (Sections 17, 18).

* **PHASE 14: Manuscript & Publication Preparation**
  * *Objective:* Draft the complete scientific manuscript with figures and tables.
  * *Input:* All validated results, figures, and documentation.
  * *Files Used:* `docs/paper/manuscript.md`, `docs/paper/figures.md`, `docs/paper/tables.md`.
  * *Expected Output:* Submission-ready manuscript.
  * *Where Saved:* `docs/paper/`.

---

## 7. Documentation Architecture & Relationships

The documentation structure is designed around a dual-layer hierarchy:

```text
                             docs/PROJECT_STRUCTURE.md
                           (Master Map of Entire Project)
                                        │
                                        ▼
                            docs/RESEARCH_DOCUMENT.md
                      (Central Single Source of Truth - 22 Sections)
                                        │
             ┌──────────────────────────┼──────────────────────────┐
             ▼                          ▼                          ▼
   Modular Foundation Docs     Methodology & Results Docs     Manuscript Drafts
   ├── 00_RESEARCH_OVERVIEW    ├── 06_METHODOLOGY             └── paper/
   ├── 01_RESEARCH_QUESTION    ├── 07_EXPERIMENT_PLAN             ├── manuscript.md
   ├── 02_LITERATURE_REVIEW    ├── 08_RESULTS                     ├── figures.md
   ├── 03_RESEARCH_GAP         ├── 09_LIMITATIONS                 └── tables.md
   ├── 04_DATASET_INVENTORY    ├── 10_RESEARCH_LOG
   └── 05_DATA_DICTIONARY      └── 11_REFERENCES
```

* **`PROJECT_STRUCTURE.md`** explains *how the repository is organized and how work is done*.
* **`RESEARCH_DOCUMENT.md`** is the *canonical master reference for all research content*.
* **`00_*.md` through `11_*.md`** provide *modular, focused documentation files* corresponding to individual research domains for targeted editing and inspection.

---

## 8. Dataset Storage & Immutability Map

| Data Type | Directory Location | Example File Types | Can Modify in Place? | Role in Research |
| :--- | :--- | :--- | :--- | :--- |
| **Original Spaceflight Data** | `data/raw/pharmaceutical_stability/` | `.csv`, `.xlsx`, `.tsv` | ❌ **NEVER** | Immutable ground-truth experimental assay tables |
| **Original Biological Data** | `data/raw/spaceflight_biological/` | `.csv`, `.txt`, `.json` | ❌ **NEVER** | Unmodified OSDR / ALSDA biological assay files |
| **Original Radiation Data** | `data/raw/space_radiation/` | `.csv`, `.dat`, `.txt` | ❌ **NEVER** | Mission dosimetry logs and GCR/SPE measurements |
| **Original Drug Properties** | `data/raw/drug_properties/` | `.sdf`, `.csv`, `.json` | ❌ **NEVER** | Raw chemical property records and SMILES strings |
| **Cleaned Intermediate Data**| `data/interim/` | `.parquet`, `.csv` | ⚠️ Yes (via script) | Harmonized units, standardized nomenclature |
| **Final Modeling Matrix** | `data/processed/` | `.parquet`, `.csv` | ⚠️ Yes (via script) | Model-ready $X, y, G$ tabular arrays |
| **External Reference Lookups**| `data/external/` | `.csv`, `.json` | ⚠️ Read-Only | Fixed chemical ontologies, standard molecular weights |
| **Serialized Models** | `models/` | `.joblib`, `.pkl` | 🔄 Generated | Saved model checkpoints for reproducible inference |
| **Metric Summaries** | `results/metrics/` | `.json`, `.yaml` | 🔄 Generated | Evaluation scores and bootstrap confidence intervals |
| **Scientific Figures** | `results/figures/` | `.png`, `.pdf`, `.svg` | 🔄 Generated | Publication-grade plots and SHAP visualizations |
| **Discovered Formulas** | `results/formulas/` | `.md`, `.tex`, `.json` | 🔄 Generated | Mathematical symbolic regression candidate equations |

---

## 9. Research Integrity & Open Science Protocols

To guarantee scientific rigor, peer-review defensibility, and open reproducibility:

1. **Zero Data Fabrication:** No artificial datasets, simulated rows, or synthetic variables are ever generated.
2. **Zero Result Fabrication:** No metrics, $R^2$ values, or tables are invented. Unrun experiments remain strictly labeled `NOT YET RUN`.
3. **No Fictional Literature:** Every paper, author, DOI, and journal reference must be physically verified against indexed academic databases.
4. **Preservation of Raw Provenance:** Raw files remain untouched. All cleaning and transformations are fully reproducible via code in `src/` and `notebooks/`.
5. **Epistemological Clarity:** Model-derived mathematical relationships are explicitly characterized as computational hypotheses rather than clinically certified pharmacological formulations.
6. **No Unsupported Clinical Claims:** The project does not claim to invent new medicines or validate therapies without real experimental/clinical confirmation.

---

## 10. Version Control & Git Strategy

### Files to Commit to Git:
* All documentation files (`docs/`, `docs/paper/`, `README.md`, `LICENSE`).
* All configuration files (`configs/experiment_config.yaml`).
* All source code modules (`src/`).
* All Jupyter notebooks (`notebooks/`).
* Small reference lookup tables in `data/external/`.
* Generated final metrics, summary tables, and discovered formulas in `results/`.
* High-resolution publication figures in `results/figures/`.
* Directory placeholder files (`.gitkeep`).

### Files Excluded from Git (`.gitignore`):
* Large raw dataset downloads exceeding standard git quotas.
* Temporary cache files (`__pycache__/`, `.ipynb_checkpoints/`).
* Local virtual environments (`.venv/`, `env/`).
* Large binary model checkpoints (`*.pkl`, `*.joblib` $> 50\text{ MB}$).
* Scratch files and temporary operating system logs.

---

## 11. Current Project Status & Immediate Action

```text
CURRENT STATUS:
├── Phase: PHASE 1 — DATASET AUDIT #1
├── State: Repository structure, master map, and single-source-of-truth established
├── Data: PENDING AUDIT (No datasets downloaded yet; no synthetic data created)
└── ML: NOT YET RUN (No models trained; no fabricated metrics)

COMPLETED:
✅ Complete repository folder hierarchy created
✅ docs/RESEARCH_DOCUMENT.md established as Single Source of Truth
✅ docs/PROJECT_STRUCTURE.md master map created
✅ All 10 research notebooks initialized with research integrity structure
✅ Python src/ modules created with clear separation of concerns
✅ Lightweight requirements.txt and experiment_config.yaml configured

IMMEDIATE NEXT ACTION:
👉 DATASET AUDIT #1:
   1. Search NASA Open Science Data Repository (OSDR) and ALSDA for spaceflight pharmaceutical stability and environmental datasets.
   2. Audit candidate literature for quantitative assay data, sample sizes, and ground-matched controls.
   3. Record verified candidates in docs/04_DATASET_INVENTORY.md and docs/RESEARCH_DOCUMENT.md.
   4. Download official unmodified files into data/raw/ and populate docs/05_DATA_DICTIONARY.md.
```
