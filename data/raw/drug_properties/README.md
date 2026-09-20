# Raw Drug Physicochemical Properties — DS-03

## 1. Data Classification
* **Category:** In Silico Drug Descriptors (Physicochemical)
* **Dataset ID:** DS-03
* **Source:** PubChem (NCBI/NIH) — publicly available, open access REST API

## 2. Extracted File

| Field | Value |
| :--- | :--- |
| **Filename** | `ds03_pubchem_drug_descriptors_8compounds.csv` |
| **Rows** | 8 compounds (one row per drug) |
| **Columns** | 14 |
| **File size** | 1,560 bytes |
| **SHA256** | `3D61B14B95C95C52CD75E1C25BB938A87FB2470025BFFA1F8A3E96F368471865` |
| **Extraction date** | 2026-09-17 |
| **Extraction method** | PubChem REST API (`/rest/pug/compound/name/<name>/property/.../JSON`) |
| **License** | Public Domain (PubChem open data) |

## 3. Compound Coverage

| Drug | PubChem CID | Molecular Formula | MW (g/mol) |
| :--- | :--- | :--- | :--- |
| Caffeine | 2519 | C8H10N4O2 | 194.19 |
| Diazepam | 3016 | C16H13ClN2O | 284.74 |
| Diphenhydramine | 3100 | C17H21NO | 255.35 |
| Epinephrine | 5816 | C9H13NO3 | 183.20 |
| Ketamine | 3821 | C13H16ClNO | 237.72 |
| Lidocaine | 3676 | C14H22N2O | 234.34 |
| Naloxone | 5284596 | C19H21NO4 | 327.40 |
| Promethazine | 4927 | C17H20N2S | 284.40 |

## 4. Column Definitions

| Column | Unit / Format | Description |
| :--- | :--- | :--- |
| `drug_name` | String | Common drug name (matches DS-01 medication column) |
| `pubchem_cid` | Integer | PubChem Compound ID |
| `molecular_formula` | String | Molecular formula (Hill notation) |
| `molecular_weight_gmol` | g/mol | Molecular weight |
| `xlogp` | Unitless | Octanol-water partition coefficient (logP) — hydrophilicity proxy |
| `tpsa_angstrom2` | Å² | Topological Polar Surface Area — membrane permeability proxy |
| `rotatable_bonds` | Integer | Count of rotatable bonds — molecular flexibility |
| `hbond_donors` | Integer | Hydrogen bond donor count |
| `hbond_acceptors` | Integer | Hydrogen bond acceptor count |
| `heavy_atom_count` | Integer | Number of non-hydrogen atoms — molecular size proxy |
| `complexity` | Unitless | Molecular complexity score (Bertz/Morgan-based) |
| `inchikey` | String (27 chars) | Hashed InChI identifier — globally unique compound key |
| `iupac_name` | String | IUPAC systematic name |
| `isomeric_smiles` | String | Isomeric SMILES notation (includes stereochemistry) |

## 5. Intended Use
- **Primary purpose:** Feature vectors for ML models in this research project
- **Key ML features:** `xlogp`, `tpsa_angstrom2`, `molecular_weight_gmol`, `rotatable_bonds`, `hbond_donors`, `hbond_acceptors`
- **Join key:** `drug_name` → matches `medication` column in DS-01 (case-insensitive)

## 6. Raw Data Preservation Rules
* This file is read-only. Do not edit values in-place.
* Additional descriptors (e.g., from RDKit, ChEMBL, DrugBank) should be added in `data/interim/` as separate augmented files.
* If descriptors need re-extraction (e.g., from a different stereoisomer), document in `docs/RESEARCH_DOCUMENT.md` Research Log.

## 7. Reference
Kim S, Chen J, Cheng T, et al. PubChem 2023 update. *Nucleic Acids Research*. 2023;51(D1):D1373-D1380. DOI: 10.1093/nar/gkac956
