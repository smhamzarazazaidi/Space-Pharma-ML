"""Reproducible Phase A audit. Parent project is read-only; no model fitting."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import ast
import argparse
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parent
PAPER = 'https://doi.org/10.1177/10806032261466966'
LAUNCH = {'SpX-15':'2018-06-29','SpX-16':'2018-12-05','NG-11':'2019-04-17',
          'SpX-17':'2019-05-04','SpX-18':'2019-07-25','SpX-20':'2020-03-07'}
ARRIVAL = {'SpX-15':'2018-07-02','SpX-16':'2018-12-08','NG-11':'2019-04-19',
           'SpX-17':'2019-05-06','SpX-18':'2019-07-27','SpX-20':'2020-03-09'}
ARRIVAL_SOURCE = {
 'SpX-15':'https://www.nasa.gov/blogs/spacestation/2018/07/page/2/',
 'SpX-16':'https://www.nasa.gov/blogs/stationreport/2018/12/08/iss-daily-summary-report-12-08-2018/',
 'SpX-17':'https://www.nasa.gov/blogs/spacestation/2019/05/06/spacex-cargo-craft-attached-to-station/',
 'SpX-18':'https://www.nasa.gov/blogs/spacestation/2019/07/27/dragon-installed-to-stations-harmony-module-for-cargo-operations/',
 'SpX-20':'https://www.nasa.gov/blogs/spacestation/2020/03/09/robotic-arm-captures-dragon-packed-with-science/',
 'NG-11':'https://www.nasa.gov/blogs/spacestation/2019/04/19/astronaut-commands-robotic-arm-to-capture-cygnus-cargo-craft-2/'}
BERTHING = {'SpX-15':'2018-07-02T13:52:00Z','SpX-16':'2018-12-08T15:36:00Z',
            'SpX-17':'2019-05-06T13:32:00Z'}

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''): h.update(block)
    return h.hexdigest()

def save(df, name):
    path=BASE/name
    path.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(path,index=False)

def span_metrics(timestamps, start, end, max_gap_seconds):
    """Union of adjacent observations within a declared gap limit, clipped to window.

    This estimates temporal support, not integration or completeness of drug dosimetry.
    Gaps longer than the limit, including boundaries, are not filled.
    """
    t=np.unique(np.asarray(timestamps,dtype=np.int64))
    a,b=pd.Timestamp(start).value//10**9,pd.Timestamp(end).value//10**9
    if b<=a: raise ValueError('Nonpositive exposure window')
    if len(t)<2: return 0.,(b-a)/3600
    left=np.maximum(t[:-1],a); right=np.minimum(t[1:],b)
    good=((t[1:]-t[:-1])<=max_gap_seconds)&(right>left)
    left,right=left[good],right[good]
    covered=float((right-left).sum())
    missing=np.concatenate(([left[0]-a],left[1:]-right[:-1],[b-right[-1]])) if len(left) else np.array([b-a])
    return covered/3600,float(missing.max())/3600

def audit():
    folders=['data/processed','data/interim/environment','results/tables','results/figures','docs']
    for f in folders: (BASE/f).mkdir(parents=True,exist_ok=True)
    files=[]
    for folder in ['data','docs','results','src','references','configs','notebooks']:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file(): files.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha(p)))
    save(pd.DataFrame(files),'results/tables/parent_file_inventory.csv')
    master=pd.read_csv(ROOT/'data/processed/master_dataset_v1.csv')
    assert len(master)==32 and master.sample_id.is_unique
    assert master.drug_name.nunique()==8 and master.mission.nunique()==6
    mapping=pd.read_csv(ROOT/'results/tables/nowadly_outcome_mapping_qc.csv')
    comparison=master.merge(mapping[['sample_id','source_identifier','flight_api_percent','ground_control_api_percent']],on='sample_id',validate='one_to_one')
    comparison['mapping_disagrees']=(comparison.flight_percent_api_remaining!=comparison.flight_api_percent)|(comparison.ground_control_percent_api_remaining!=comparison.ground_control_api_percent)
    comparison['recomputed_relative_delta']=100*(comparison.flight_percent_api_remaining/comparison.ground_control_percent_api_remaining-1)
    comparison['derived_stability_ratio']=100*comparison.flight_percent_api_remaining/comparison.ground_control_percent_api_remaining
    comparison['delta_arithmetic_ok']=abs(comparison.recomputed_relative_delta-comparison.relative_percent_diff_vs_control)<=0.0051
    comparison['use_for_modeling']=False
    save(comparison[['sample_id','drug_name','formulation','mission','flight_percent_api_remaining','ground_control_percent_api_remaining','flight_api_percent','ground_control_api_percent','source_identifier','mapping_disagrees','relative_percent_diff_vs_control','recomputed_relative_delta','derived_stability_ratio','delta_arithmetic_ok','use_for_modeling']],'results/tables/outcome_linkage_audit.csv')
    # Inspect literal values without executing the legacy script (which overwrites datasets).
    tree=ast.parse((ROOT/'scratch/digitize_all_lots.py').read_text(encoding='utf-8-sig'))
    outcomes=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='outcomes_list' for t in n.targets))
    positional_match=bool(np.allclose(master.flight_percent_api_remaining,[r['flight_api'] for r in outcomes]))
    expected={'Caffeine|Tablet':'2A','Diphenhydramine|Capsule':'2B','Promethazine|Tablet':'2C','Diazepam|Solution':'3A','Diphenhydramine|Solution':'3B','Epinephrine|Autoinjector':'3C','Ketamine|Solution':'3D','Lidocaine|Solution':'3E','Naloxone|Solution':'3F','Promethazine|Solution':'3G'}
    comparison['expected_panel']=[expected[r.drug_name+'|'+r.formulation] for r in comparison.itertuples()]
    wrong_panel=~comparison.source_identifier.str[-2:].eq(comparison.expected_panel)
    save(comparison.loc[wrong_panel,['sample_id','drug_name','formulation','source_identifier','expected_panel']],'results/tables/figure_mapping_conflicts.csv')
    windows=[]
    for r in master.itertuples():
        nominal=pd.Timestamp(LAUNCH[r.mission])+pd.Timedelta(days=r.days_in_space)
        windows.append(dict(lot_id=r.sample_id,api=r.drug_name,mission=r.mission,
          formulation=r.formulation,launch_date=LAUNCH[r.mission],
          launch_datetime='2020-03-07T04:50:00Z' if r.mission=='SpX-20' else ('2019-07-25T22:01:00Z' if r.mission=='SpX-18' else ''),
          arrival_date=ARRIVAL[r.mission],docking_datetime=BERTHING.get(r.mission,''),
          arrival_event='robotic berthing; exact medication transfer time unknown',
          departure_datetime='',landing_datetime='',iss_exposure_hours='',
          reported_days_launch_to_landing=r.days_in_space,total_spaceflight_hours=r.days_in_space*24,
          total_hours_precision='derived from published integer days; not exact timestamp duration',
          reconstructed_landing_date=nominal.date().isoformat(),
          reconstruction_status='launch date + reported integer days; NOT a verified landing',
          candidate_proxy_start_date=ARRIVAL[r.mission],candidate_proxy_end_date=nominal.date().isoformat(),
          candidate_window_status='screening envelope only; includes unknown return transit and transfer periods',
          legacy_start_date=r.start_date,legacy_end_date=r.end_date,
          legacy_end_shift_days=(pd.Timestamp(r.end_date)-nominal).days,
          days_expired_at_analysis=r.days_expired,expiration_at_launch='within label expiration (paper)',
          expiration_at_analysis='expired (paper)',storage_location='ISS HMS kit; exact module/hardware unknown',
          spatial_relevance_grade='D',source='Nowadly 2026 Table 1; NASA mission record',
          source_url_or_identifier=PAPER,arrival_source=ARRIVAL_SOURCE[r.mission],
          confidence='provisional; return vehicle and lot manifest unverified',
          notes='Do not equate arrival vehicle departure with medication departure. SpX-16 berthing time approximate; SpX-18 NASA reports disagree on minute.'))
    windows=pd.DataFrame(windows)
    save(windows,'data/processed/medication_exposure_windows.csv')
    print('Auditing radiation archive...',flush=True)
    radpath=ROOT/'data/raw/space_radiation/RAD_ISS_Columbus_DosTel_2018_2022.csv'
    rad=pd.read_csv(radpath)
    dates=pd.to_datetime(rad.timestamp,utc=True,errors='raise')
    rad['epoch']=dates.array.as_unit('ns').asi8//10**9
    sensors=[]; groups={}
    for sensor,g in rad.groupby('instrument_id'):
        t=np.sort(g.epoch.unique()); groups[sensor]=t; dt=np.diff(t)
        sensors.append(dict(sensor=sensor,rows=len(g),start=pd.Timestamp(t[0],unit='s',tz='UTC').isoformat(),end=pd.Timestamp(t[-1],unit='s',tz='UTC').isoformat(),median_step_seconds=float(np.median(dt)),p95_step_seconds=float(np.quantile(dt,.95)),largest_gap_hours=float(dt.max()/3600),gaps_gt_1h=int((dt>3600).sum()),gaps_gt_24h=int((dt>86400).sum()),mean_rate_as_stored=float(g.absorbed_dose_rate.mean()),module='Columbus',unit='uGy/h (RadLab API documentation)',spatial_relevance_grade='D'))
    save(pd.DataFrame(sensors),'results/tables/radiation_sensor_audit.csv')
    coverage=[]
    for w in windows.itertuples():
        for sensor,t in groups.items():
            for maxgap in (300,3600):
                h,gap=span_metrics(t,w.candidate_proxy_start_date,w.candidate_proxy_end_date,maxgap)
                expected_h=(pd.Timestamp(w.candidate_proxy_end_date)-pd.Timestamp(w.candidate_proxy_start_date)).total_seconds()/3600
                coverage.append(dict(lot_id=w.lot_id,api=w.api,variable='radiation',sensor=sensor,window_status='provisional screening envelope',start=w.candidate_proxy_start_date,end=w.candidate_proxy_end_date,expected_hours=expected_h,observed_support_hours=h,coverage_percent=100*h/expected_h,largest_missing_interval_hours=gap,gap_limit_seconds=maxgap,spatial_relevance_grade='D',timezone_status='naive source timestamps interpreted as UTC for audit; confirm with provider'))
    save(pd.DataFrame(coverage),'results/tables/radiation_temporal_coverage.csv')
    duplicates=rad[rad.duplicated(['timestamp','instrument_id'],keep=False)]
    duplicate_conflicts=int((duplicates.groupby(['timestamp','instrument_id']).absorbed_dose_rate.nunique()>1).sum())
    summary=dict(generated_utc=datetime.now(timezone.utc).isoformat(),lots=len(master),apis=master.drug_name.nunique(),missions=master.mission.nunique(),outcome_mapping_disagreements=int(comparison.mapping_disagrees.sum()),figure_mapping_conflicts=int(wrong_panel.sum()),legacy_positional_assignment_reproduced=positional_match,relative_delta_arithmetic_failures=int((~comparison.delta_arithmetic_ok).sum()),radiation_rows=len(rad),radiation_missing_cells=int(rad.isna().sum().sum()),radiation_duplicate_sensor_timestamps=int(rad.duplicated(['timestamp','instrument_id']).sum()),radiation_exact_duplicate_rows=int(rad.duplicated().sum()),radiation_conflicting_timestamp_groups=duplicate_conflicts,radiation_negative_values=int((rad.absorbed_dose_rate<0).sum()),radiation_first_timestamp=str(dates.min()),radiation_last_timestamp=str(dates.max()),radiation_sha256=sha(radpath),master_sha256=sha(ROOT/'data/processed/master_dataset_v1.csv'),all_exact_iss_windows_unresolved=True,models_run=False)
    # Re-hash parent files after analysis to enforce the read-only boundary.
    changed=[f['path'] for f in files if sha(ROOT/f['path'])!=f['sha256']]
    summary['parent_files_changed']=changed
    assert not changed, changed
    (BASE/'results/tables/audit_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__': audit()
