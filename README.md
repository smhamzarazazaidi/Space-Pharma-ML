# Interpretable Small-Data ML for Predicting Pharmaceutical Response and Stability Under Long-Duration Spaceflight Conditions

[![Research Status: Phase 1 (Dataset Audit)](https://img.shields.io/badge/Status-Phase%201%20Dataset%20Audit-yellow.svg)](#current-research-status)
[![Single Source of Truth: docs/RESEARCH_DOCUMENT.md](https://img.shields.io/badge/Docs-RESEARCH__DOCUMENT.md-blue.svg)](docs/RESEARCH_DOCUMENT.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Central Research Document & Single Source of Truth

> [!IMPORTANT]
> **This repository is a rigorous scientific research project, not a software product.**  
> All research planning, hypotheses, literature reviews, dataset inventories, data provenance records, data dictionaries, methodology, experimental workflows, results, limitations, and research logs are organized exclusively within:
> 
> 📄 **[`docs/RESEARCH_DOCUMENT.md`](docs/RESEARCH_DOCUMENT.md)**  
> *(The Single Source of Truth for the entire research project)*

---

## 🔬 Research Objective & Concept

Exploration-class human spaceflight missions (such as crewed Mars expeditions and permanent lunar surface habitats) subject pharmaceuticals to multi-stressor environments including microgravity, elevated ionizing radiation (GCR and SPEs), altered atmospheric conditions, and multi-year storage without resupply.

This research aims to:
1. Harmonize empirical spaceflight pharmaceutical stability assays and space environmental dosimetry from verified public repositories (e.g., NASA Open Science Data Repository - OSDR).
2. Integrate domain-specific physicochemical drug descriptors (e.g., molecular weight, TPSA, logP, rotatable bonds, functional groups).
3. Benchmark interpretable, small-data machine learning algorithms and symbolic regression techniques to predict active pharmaceutical ingredient (API) degradation and response variation.
4. Extract explainable feature interactions (via SHAP) and discover closed-form mathematical candidate relationships $S_{\text{space}} = f(\text{radiation}, \text{duration}, \dots)$ to support spaceflight medical operations.

---

## 📁 Repository Structure

```text
space-pharma-ml/
│
├── README.md                      # Project overview, policies, and navigation
├── LICENSE                        # MIT Open Source Research License
├── .gitignore                     # Git ignore rules for small-data ML
├── requirements.txt               # Lightweight research dependencies
│
├── docs/
│   └── RESEARCH_DOCUMENT.md       # SINGLE SOURCE OF TRUTH (All 22 Research Sections)
│
├── data/
│   ├── raw/                       # Original downloaded datasets ONLY (never edited)
│   │   ├── pharmaceutical_stability/
│   │   ├── spaceflight_biological/
│   │   ├── space_radiation/
│   │   └── drug_properties/
│   │
│   ├── interim/                   # Cleaned, standardized intermediate data
│   ├── processed/                 # Final tabular modeling matrices
│   └── external/                  # Reference lookup tables and ontologies
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
│   ├── data/                      # Data loaders and audit scripts
│   ├── features/                  # Feature engineering utilities
│   ├── models/                    # Baseline and ML model wrappers
│   ├── evaluation/                # Grouped cross-validation & SHAP routines
│   └── visualization/             # High-resolution figure generators
│
├── configs/
│   └── experiment_config.yaml     # Experiment parameters and random seeds
│
├── models/                        # Serialized model checkpoints
│
└── results/
    ├── tables/                    # Performance comparison tables
    ├── figures/                   # Scientific figures (1-3 major figures)
    ├── metrics/                   # Quantitative validation metric JSONs
    └── formulas/                  # Discovered symbolic equations
```

---

## 🛡️ Research Integrity & Data Policy

To uphold the highest scientific and open-science standards:
1. **Zero Synthetic / Fake Data:** No artificial datasets or simulated numbers are generated.
2. **Strict Raw Data Immutability:** Raw data files in `data/raw/` are preserved in their exact original form with complete provenance metadata logged in `docs/RESEARCH_DOCUMENT.md`.
3. **No Fabricated Literature or Results:** All papers, DOIs, sample counts, and metrics must be verified. Unperformed experiments are explicitly marked as `NOT YET RUN`.
4. **Distinction of Evidence:** Model-derived mathematical relationships are explicitly characterized as computational hypotheses, not clinically validated physical laws or new therapeutics.

---

## 💻 Compute Constraints & Environment

The computational pipeline is explicitly designed to operate efficiently under realistic academic/field constraints:
* **Hardware:** Standard laptop CPU / 16 GB RAM (or standard Google Colab CPU instance)
* **Stack:** Classical tabular ML (`scikit-learn`, `xgboost`, `lightgbm`, `shap`, `scipy`)
* **Visuals:** Publication-grade output focusing on 1–3 clear, high-impact scientific figures.

---

## 🚦 Current Research Status & Next Steps

* **Current Stage:** `Phase 1: Dataset Audit #1`
* **Immediate Tasks:**
  1. Identify exact spaceflight pharmaceutical stability datasets in NASA OSDR / ALSDA and peer-reviewed literature.
  2. Record candidate entries into Section 7 & 8 of [`docs/RESEARCH_DOCUMENT.md`](docs/RESEARCH_DOCUMENT.md).
  3. Download official unedited raw files to `data/raw/`.
  4. Inspect columns and complete Section 9 (Data Dictionary) prior to running modeling code.

---

## 🚀 How to Start the Research

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd "Space medicne"
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Consult the central document:**
   Read and update [`docs/RESEARCH_DOCUMENT.md`](docs/RESEARCH_DOCUMENT.md) during each phase of dataset curation and modeling.
