# Master Dataset V2 Quality Control and Verification Report

**Generated:** 2026-09-20 02:04:44
**Target Dataset:** `simulation/data/processed/master_dataset_v2_verified.csv`
**Status:** ALL 14 STRICT VALIDATION CHECKS PASSED

## Validation Test Matrix

| Test Name | Status | Details |
|---|:---:|---|
| Row Count | **PASS** | Found 32 rows (expected exactly 32). |
| Unique APIs | **PASS** | Found 8 APIs: ['Caffeine', 'Diazepam', 'Diphenhydramine', 'Epinephrine', 'Ketamine', 'Lidocaine', 'Naloxone', 'Promethazine'] |
| Unique Lot IDs | **PASS** | Duplicate lot count: 0 |
| Mission Assignments | **PASS** | Found missions: ['NG-11', 'SpX-15', 'SpX-16', 'SpX-17', 'SpX-18', 'SpX-20'] |
| Positive Durations | **PASS** | Min spaceflight days: 132, Min ISS storage days: 109.08 |
| API Percentage Bounds | **PASS** | Flight range: [74.2%, 100.8%], Ground range: [78.9%, 103.6%] |
| Delta API Recomputation | **PASS** | Max absolute delta discrepancy: 0.0 |
| Stability Ratio Recomputation | **PASS** | Max absolute ratio discrepancy: 0.0 |
| Stability Ratio vs Delta Consistency | **PASS** | Max mathematical deviation: 0.0 |
| Radiation Coverage Bounds | **PASS** | Radiation coverage range: [76.74%, 100.0%] |
| Radiation Dose Non-negative | **PASS** | Combined cumulative dose range: [37.0078 mGy, 217.0879 mGy] |
| Molecular Descriptor Completeness | **PASS** | Total missing descriptor cells across 32 lots: 0 |
| Formulation Binary Consistency | **PASS** | Formulation class vs is_solid mismatches: 0 |
| Provenance Metadata Completeness | **PASS** | Total null provenance fields: 0 |

## Summary Statement

All 32 experimental lots satisfy rigorous scientific, mathematical, and data engineering standards. The experimental outcomes, mission boundaries, radiation numerical integration, and molecular features are verified and ready for baseline modeling.
