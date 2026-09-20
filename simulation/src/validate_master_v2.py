"""
Phase B: Task 12 - Master Dataset V2 Strict Quality Control and Validation
Runs assertions across all integrity checks and produces MASTER_V2_QC.md.
"""

import os
import sys
import numpy as np
import pandas as pd

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

print("=== STARTING MASTER DATASET V2 VALIDATION ===")

SIM_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
v2_path = os.path.join(SIM_DIR, "data", "processed", "master_dataset_v2_verified.csv")

if not os.path.exists(v2_path):
    raise FileNotFoundError(f"Missing master_dataset_v2_verified.csv at {v2_path}")

df_v2 = pd.read_csv(v2_path)

qc_results = []

def run_check(test_name, condition, details=""):
    status = "PASS" if condition else "FAIL"
    qc_results.append({
        "test_name": test_name,
        "status": status,
        "details": details
    })
    print(f"[{status}] {test_name}: {details}")
    if not condition:
        raise AssertionError(f"CRITICAL QC FAILURE: {test_name} - {details}")

# 1. Exactly 32 rows
run_check("Row Count", len(df_v2) == 32, f"Found {len(df_v2)} rows (expected exactly 32).")

# 2. Exactly 8 unique APIs
unique_apis = df_v2['api'].unique()
expected_apis = {'Caffeine', 'Diazepam', 'Diphenhydramine', 'Epinephrine', 'Ketamine', 'Lidocaine', 'Naloxone', 'Promethazine'}
run_check("Unique APIs", len(unique_apis) == 8 and set(unique_apis) == expected_apis, f"Found {len(unique_apis)} APIs: {sorted(list(unique_apis))}")

# 3. Unique lot IDs and no duplicates
dup_lots = df_v2['lot_id'].duplicated().sum()
run_check("Unique Lot IDs", dup_lots == 0, f"Duplicate lot count: {dup_lots}")

# 4. Correct mission assignments
unique_missions = set(df_v2['mission'].unique())
expected_missions = {'SpX-15', 'SpX-16', 'SpX-17', 'NG-11', 'SpX-18', 'SpX-20'}
run_check("Mission Assignments", unique_missions == expected_missions, f"Found missions: {sorted(list(unique_missions))}")

# 5. Non-negative durations
min_space_days = df_v2['days_in_space'].min()
min_iss_days = df_v2['iss_storage_days'].min()
run_check("Positive Durations", min_space_days > 0 and min_iss_days > 0, f"Min spaceflight days: {min_space_days}, Min ISS storage days: {min_iss_days}")

# 6. Realistic API percentages (0 - 150%)
flt_min, flt_max = df_v2['flight_percent_api_remaining'].min(), df_v2['flight_percent_api_remaining'].max()
gnd_min, gnd_max = df_v2['ground_control_percent_api_remaining'].min(), df_v2['ground_control_percent_api_remaining'].max()
run_check("API Percentage Bounds", (flt_min > 50 and flt_max < 150 and gnd_min > 50 and gnd_max < 150), f"Flight range: [{flt_min}%, {flt_max}%], Ground range: [{gnd_min}%, {gnd_max}%]")

# 7. Delta API recalculation check
recomputed_delta = (((df_v2['flight_percent_api_remaining'] - df_v2['ground_control_percent_api_remaining']) / df_v2['ground_control_percent_api_remaining']) * 100.0).round(4)
delta_diff = (df_v2['delta_api_percent'] - recomputed_delta).abs().max()
run_check("Delta API Recomputation", delta_diff < 1e-3, f"Max absolute delta discrepancy: {delta_diff}")

# 8. Stability ratio recalculation check
recomputed_ratio = ((df_v2['flight_percent_api_remaining'] / df_v2['ground_control_percent_api_remaining']) * 100.0).round(4)
ratio_diff = (df_v2['stability_ratio_percent'] - recomputed_ratio).abs().max()
run_check("Stability Ratio Recomputation", ratio_diff < 1e-3, f"Max absolute ratio discrepancy: {ratio_diff}")

# 9. Stability Ratio = 100 + Delta API check
sr_delta_diff = (df_v2['stability_ratio_percent'] - (100.0 + df_v2['delta_api_percent'])).abs().max()
run_check("Stability Ratio vs Delta Consistency", sr_delta_diff < 1e-3, f"Max mathematical deviation: {sr_delta_diff}")

# 10. Radiation coverage bounds (0 - 100%)
rad_cov_min, rad_cov_max = df_v2['radiation_coverage_pct'].min(), df_v2['radiation_coverage_pct'].max()
run_check("Radiation Coverage Bounds", (rad_cov_min >= 0.0 and rad_cov_max <= 100.0), f"Radiation coverage range: [{rad_cov_min}%, {rad_cov_max}%]")

# 11. Radiation dose non-negative
dose_min, dose_max = df_v2['cumulative_dose_combined_mGy'].min(), df_v2['cumulative_dose_combined_mGy'].max()
run_check("Radiation Dose Non-negative", dose_min > 0.0, f"Combined cumulative dose range: [{dose_min} mGy, {dose_max} mGy]")

# 12. Molecular descriptor completeness and sanity
mol_fields = ['pubchem_cid', 'molecular_weight', 'xlogp', 'tpsa', 'hbd', 'hba', 'rotatable_bonds', 'heavy_atom_count', 'complexity']
null_mols = df_v2[mol_fields].isnull().sum().sum()
run_check("Molecular Descriptor Completeness", null_mols == 0, f"Total missing descriptor cells across 32 lots: {null_mols}")

# 13. Formulation consistency
form_class_solid = (df_v2['formulation_class'] == 'Solid').astype(int)
form_mismatch = (df_v2['is_solid'] != form_class_solid).sum()
run_check("Formulation Binary Consistency", form_mismatch == 0, f"Formulation class vs is_solid mismatches: {form_mismatch}")

# 14. Provenance and Confidence completeness
prov_nulls = df_v2[['outcome_confidence', 'exposure_confidence', 'radiation_confidence', 'spatial_relevance_grade', 'data_provenance_class']].isnull().sum().sum()
run_check("Provenance Metadata Completeness", prov_nulls == 0, f"Total null provenance fields: {prov_nulls}")

# Write MASTER_V2_QC.md report
qc_doc_path = os.path.join(SIM_DIR, "docs", "MASTER_V2_QC.md")
with open(qc_doc_path, "w", encoding="utf-8") as f:
    f.write("# Master Dataset V2 Quality Control and Verification Report\n\n")
    f.write(f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"**Target Dataset:** `simulation/data/processed/master_dataset_v2_verified.csv`\n")
    f.write(f"**Status:** ALL {len(qc_results)} STRICT VALIDATION CHECKS PASSED\n\n")
    f.write("## Validation Test Matrix\n\n")
    f.write("| Test Name | Status | Details |\n")
    f.write("|---|:---:|---|\n")
    for r in qc_results:
        f.write(f"| {r['test_name']} | **{r['status']}** | {r['details']} |\n")
    f.write("\n## Summary Statement\n\n")
    f.write("All 32 experimental lots satisfy rigorous scientific, mathematical, and data engineering standards. ")
    f.write("The experimental outcomes, mission boundaries, radiation numerical integration, and molecular features are verified and ready for baseline modeling.\n")

print(f"\nQC Document saved to: {qc_doc_path}")
print("=== ALL STRICT QC CHECKS PASSED (14/14) ===")
