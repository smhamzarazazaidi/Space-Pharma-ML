"""Audit downloaded telemetry availability, preserving raw records and gaps."""
import json
import sys
import os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'.deps'))
os.environ.setdefault('MPLCONFIGDIR',str(Path(__file__).resolve().parents[1]/'.cache/matplotlib'))
import numpy as np
import pandas as pd
if '--no-plot' not in sys.argv:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
from audit_project import BASE, ROOT, save, sha, span_metrics

UNITS={'temperature':'degC','humidity':'%RH','co2':'ppm'}

def main():
    windows=pd.read_csv(BASE/'data/processed/medication_exposure_windows.csv')
    inventory=[]; all_times={k:[] for k in UNITS}; provenance=[]
    for p in sorted((BASE/'data/raw/environment').rglob('*.provenance.json')):
        meta=json.loads(p.read_text()); raw=BASE/meta['path']
        assert sha(raw)==meta['sha256'],f'Archive integrity failure: {raw}'
        provenance.append(meta)
    (BASE/'results/tables/download_manifest.json').write_text(json.dumps(provenance,indent=2),encoding='utf-8')
    for p in sorted((BASE/'data/raw/environment/cabin').glob('*_telemetry.json')):
        mission=p.stem.replace('_telemetry',''); data=pd.DataFrame(json.loads(p.read_text()))
        meta=json.loads(p.with_suffix('.json.provenance.json').read_text())
        for variable,unit in UNITS.items():
            col=variable+'_iss'
            row=dict(dataset=mission,variable=variable,source_organization='NASA OSDR EDA',source_url=meta['url'],raw_file=p.relative_to(BASE).as_posix(),download_utc=meta['retrieved_utc'],sha256=meta['sha256'],unit=unit,sensor='not supplied by API',sensor_location='ISS label; module/hardware not supplied',spatial_relevance_grade='E',quality_flags='not supplied',calibration='not supplied',license='public access; dataset-specific reuse terms unverified',rows=len(data),start_utc='',end_utc='',median_step_seconds='',missing_cells='',unique_observed_times=0,conflicting_timestamps=0,download_status='empty API response' if data.empty else 'downloaded')
            if not data.empty:
                assert col in data and 'time' in data
                values=pd.to_numeric(data[col],errors='coerce')
                times=pd.to_datetime(data.time,utc=True)
                row['missing_cells']=int(values.isna().sum())
                valid=pd.DataFrame({'time':times,'value':values}).dropna()
                conflicts=valid.groupby('time').value.nunique()
                bad=conflicts[conflicts>1].index
                valid=valid[~valid.time.isin(bad)].drop_duplicates('time')
                row['conflicting_timestamps']=len(bad)
                row['duplicate_nonnull_records']=int(values.notna().sum()-data.loc[values.notna(),'time'].nunique())
                if not valid.empty:
                    t=np.sort(valid.time.array.as_unit('ns').asi8//10**9)
                    row.update(start_utc=str(valid.time.min()),end_utc=str(valid.time.max()),unique_observed_times=len(t),median_step_seconds=float(np.median(np.diff(t))) if len(t)>1 else '',min_value=float(valid.value.min()),max_value=float(valid.value.max()))
                    all_times[variable].append(t)
            inventory.append(row)
    streams=pd.DataFrame(inventory); save(streams,'results/tables/environment_source_inventory.csv')
    acquisition=[]
    for name in ['RR-7','RR-8','RR-12','RR-17','RR-19','RR-18','RR-23','RR-10','RR-20']:
        found=streams[streams.dataset==name]
        acquisition.append(dict(dataset=name,status=found.iloc[0].download_status if len(found) else 'no completed response archived; acquisition batch interrupted',payload_archived=bool(len(found)),notes='No missing telemetry values are synthesized'))
    save(pd.DataFrame(acquisition),'results/tables/source_acquisition_status.csv')
    cover=[]
    for w in windows.itertuples():
        hours=(pd.Timestamp(w.candidate_proxy_end_date)-pd.Timestamp(w.candidate_proxy_start_date)).total_seconds()/3600
        for variable in ['temperature','humidity','co2','pressure','oxygen']:
            parts=all_times.get(variable,[])
            t=np.unique(np.concatenate(parts)) if parts else np.array([],dtype=np.int64)
            # Availability union only: never average values or splice into exposure features.
            observed,gap=span_metrics(t,w.candidate_proxy_start_date,w.candidate_proxy_end_date,600)
            cover.append(dict(lot_id=w.lot_id,api=w.api,variable=variable,expected_exposure_hours=hours,observed_support_hours=observed,coverage_percent=100*observed/hours,largest_missing_interval_hours=gap,sensor_count='',confidence='provisional window; sensor identity/location unknown',spatial_relevance_grade='E',gap_limit_seconds=600,status='available timestamps only; not validated exposure' if parts else 'no telemetry acquired; not proof no data exist'))
    rad=pd.read_csv(BASE/'results/tables/radiation_temporal_coverage.csv')
    # Keep sensors separate; the plot uses the better covered single sensor per lot,
    # rather than pretending sensor measurements can be pooled as a dosimeter.
    rad=rad[rad.gap_limit_seconds==300]
    for lot,g in rad.groupby('lot_id'):
        best=g.loc[g.coverage_percent.idxmax()]
        cover.append(dict(lot_id=lot,api=best.api,variable='radiation',expected_exposure_hours=best.expected_hours,observed_support_hours=best.observed_support_hours,coverage_percent=best.coverage_percent,largest_missing_interval_hours=best.largest_missing_interval_hours,sensor_count=len(g),confidence='best-covered single sensor; duplicate timestamps unresolved',spatial_relevance_grade='D',gap_limit_seconds=300,status='provisional window; source UTC assumption'))
    coverage=pd.DataFrame(cover)
    assert len(coverage)==192 and not coverage.duplicated(['lot_id','variable']).any()
    assert coverage.coverage_percent.between(0,100.000001).all()
    assert (coverage.largest_missing_interval_hours<=coverage.expected_exposure_hours+1e-9).all()
    save(coverage,'results/tables/lot_variable_availability.csv')
    mat=coverage.pivot(index='lot_id',columns='variable',values='coverage_percent').reindex(columns=['radiation','temperature','humidity','co2','pressure','oxygen'])
    if '--no-plot' not in sys.argv:
        plot_coverage(mat,windows)
    official=pd.read_csv(BASE/'data/raw/environment/radiation/radlab_verification_20180601.csv')
    local=pd.read_csv(ROOT/'data/raw/space_radiation/RAD_ISS_Columbus_DosTel_2018_2022.csv',nrows=1000)
    local=local[local.timestamp<'2018-06-01T01:00:00']
    joined=official.merge(local,on=['timestamp','instrument_id'],how='outer',suffixes=('_official','_archive'),indicator=True)
    result=dict(official_rows=len(official),archive_rows=len(local),matched_keys=int((joined._merge=='both').sum()),all_keys_match=bool((joined._merge=='both').all()),all_rates_match=bool(np.allclose(joined.absorbed_dose_rate_official,joined.absorbed_dose_rate_archive)),scope='First hour only; does not certify entire multi-year archive')
    (BASE/'results/tables/radiation_live_verification.json').write_text(json.dumps(result,indent=2))
    print(streams[['dataset','variable','rows','start_utc','end_utc','unique_observed_times','conflicting_timestamps']].to_string(index=False))
    print(json.dumps(result))
    print(coverage.groupby('variable').coverage_percent.agg(['min','max']).to_string())

def plot_coverage(mat,windows):
    fig,ax=plt.subplots(figsize=(10,12))
    image=ax.imshow(mat.values,aspect='auto',vmin=0,vmax=100,cmap='Blues')
    ax.set_xticks(range(len(mat.columns)),['Radiation','Temperature','Humidity','CO2','Pressure','Oxygen'])
    labels=windows.set_index('lot_id').api
    ax.set_yticks(range(len(mat)),[f'{x}  {labels[x]}' for x in mat.index],fontsize=8)
    for i in range(len(mat)):
        for j in range(len(mat.columns)):
            value=mat.iloc[i,j]
            ax.text(j,i,f'{value:.1f}%',ha='center',va='center',fontsize=8,color='white' if value>55 else '#142c40')
    ax.set_title('Telemetry availability within provisional lot windows',loc='left',fontsize=15,pad=18)
    fig.colorbar(image,ax=ax,label='Temporal support (%)',shrink=.65)
    fig.text(.06,.025,'Not exact medication exposure. Radiation: best single sensor, 5-minute gap limit.\nCabin variables: timestamp union, 10-minute gap limit; conflicting values excluded.\n0% means no supported interval in acquired data. Pressure/oxygen were not acquired.',fontsize=9)
    fig.tight_layout(rect=(0,.08,1,1)); fig.savefig(BASE/'results/figures/environment_availability.png',dpi=160); plt.close(fig)

if __name__=='__main__': main()
