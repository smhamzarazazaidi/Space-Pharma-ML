"""Build Phase D artifacts. Run once before serve_phase_d.py. Preserves V2 bytes."""
import sys,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
from simulator import SIM,DATA,TABLES,VERSION
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from simulator.exposure_integrator import Stream,combine
from simulator.environment_loader import VARIABLES,SOURCES
from simulator.mission_timeline import seconds,boundaries
from simulator.validation_engine import run,metrics
from simulator.stability_engine import fit,FEATURES
from simulator.domain_checker import assess
from simulator.uncertainty import intervals

FIG=SIM/'results/figures/phase_d'
def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def write_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,allow_nan=False,separators=(',',':')),encoding='utf-8')

def plot(name,title,xlabel,ylabel,series):
    fig,ax=plt.subplots(figsize=(9,4.5))
    for x,y,label in series:ax.plot(x,y,label=label,lw=1)
    ax.set(title=title,xlabel=xlabel,ylabel=ylabel)
    if len(series)>1:ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(FIG/(name+'.png'),dpi=240);plt.close(fig)

def build():
    for path in [DATA/'environment_streams',DATA/'missions',DATA/'private',FIG,SIM/'models/phase_d_v0']:
        path.mkdir(parents=True,exist_ok=True)
    source=SIM/'data/processed/master_dataset_v2_verified.csv'
    original=digest(source)
    frame=pd.read_csv(source)
    print('Loading cleaned DosTel archive',flush=True)
    rad=pd.read_csv(SIM/'data/interim/radiation_cleaned.csv.gz',usecols=['timestamp','instrument_id','absorbed_dose_rate'])
    assert len(rad)>2000000, 'Full archive required; uncompressed CSV is only a 50,000-row preview'
    rad['seconds']=pd.to_datetime(rad.timestamp,utc=True).astype('int64')/1e9
    # pandas 3 may retain non-nanosecond datetime resolution; explicit conversion below.
    rad['seconds']=pd.DatetimeIndex(pd.to_datetime(rad.timestamp,utc=True)).as_unit('ns').asi8/1e9
    streams={}; sensitivity={}
    for n,sensor in enumerate(['DosTel1','DosTel2'],1):
        r=rad[rad.instrument_id==sensor].groupby('seconds').absorbed_dose_rate.mean().sort_index()
        streams[f'radiation_sensor{n}']=Stream(r.index,r.to_numpy(),300)
        sensitivity[sensor]=Stream(r.index,r.to_numpy(),3600)
    streams['radiation_combined']=combine([streams['radiation_sensor1'],streams['radiation_sensor2']])
    rad_sensitivity=combine(list(sensitivity.values()))
    cabin=[]
    for path in sorted((SIM/'data/raw/environment/cabin').glob('*_telemetry.json')):
        values=json.loads(path.read_text(encoding='utf-8'))
        if values:
            c=pd.DataFrame(values);c['source_file']=path.name;cabin.append(c)
    cabin=pd.concat(cabin,ignore_index=True)
    cabin['seconds']=pd.DatetimeIndex(pd.to_datetime(cabin.time,utc=True)).as_unit('ns').asi8/1e9
    for key,field in [('temperature','temperature_iss'),('relative_humidity','humidity_iss'),('co2','co2_iss')]:
        values=cabin.groupby('seconds')[field].mean().dropna().sort_index()
        streams[key]=Stream(values.index,values.to_numpy(),600)
    for key,s in streams.items():s.save(DATA/'environment_streams'/f'{key}.npz')
    print('Computing clipped dose, coverage and shared mission streams',flush=True)
    coverage=[]; timelines=[]; compare=[]; lots=[]; mission_series={}
    descriptors=pd.read_csv(SIM.parent/'data/raw/drug_properties/ds03_pubchem_drug_descriptors_8compounds.csv').set_index('drug_name')
    excluded=['delta_api_percent','stability_ratio_percent','flight_percent_api_remaining','ground_control_percent_api_remaining','sd_flight','sd_ground','anova_p_value','figure_source']
    for _,lot in frame.iterrows():
        start,arrival,departure,end=boundaries(lot)
        row={'lot_id':lot.lot_id,'api':lot.api,'mission':lot.mission}
        for key,s in streams.items():
            row[key+'_coverage_pct']=(s.prefix(departure,True)-s.prefix(arrival,True))/(end-start)*100
        row.update(pressure_coverage_pct=0.,oxygen_coverage_pct=0.)
        dose=streams['radiation_combined'].integral(arrival,departure)
        frame.loc[frame.lot_id==lot.lot_id,'replay_dose_mGy']=dose
        coverage.append(row)
        compare.append({'lot_id':lot.lot_id,'v2_dose_mGy':lot.cumulative_dose_combined_mGy,'phase_d_storage_observed_dose_mGy':dose,
            'one_hour_gap_sensitivity_mGy':rad_sensitivity.integral(arrival,departure),'v2_cabin_coverage_method':'row count x 5 min; may double count',
            'boundary_issue':'NG-11 departure is delivery Cygnus departure; pharmaceutical transfer/return unresolved' if lot.mission=='NG-11' else 'Inherited V2 timestamps; lot-specific manifest not independently verified in D'})
        timelines.append({**{k:lot[k] for k in ['lot_id','api','mission','launch_datetime','docking_datetime','departure_datetime','landing_datetime','days_in_space']},
            'boundary_provenance':'Inherited V2; capture labeled docking; exact package transfer unverified', 'date_status':'PROVISIONAL_BOUNDARY',
            'departure_issue':lot.mission=='NG-11'})
        public={k:v for k,v in lot.to_dict().items() if k not in excluded}
        public.update(coverage=row,replay_dose_mGy=dose,times=[start,arrival,departure,end],
            molecular_formula=descriptors.loc[lot.api,'molecular_formula'],
            timeline_note=compare[-1]['boundary_issue'])
        lots.append(public)
    cov=pd.DataFrame(coverage)
    cov.to_csv(TABLES/'environment_coverage_by_lot.csv',index=False)
    pd.DataFrame(compare).to_csv(TABLES/'phase_d_exposure_reconciliation.csv',index=False)
    pd.DataFrame(timelines).to_csv(DATA/'historical_mission_timelines.csv',index=False)
    mission_cov=[]
    for mission,group in frame.groupby('mission'):
        start=seconds(group.launch_datetime.min());end=seconds(group.landing_datetime.max())
        arrival=seconds(group.docking_datetime.min());departure=seconds(group.departure_datetime.max())
        # 12-hour visualization bins only; full-resolution integrals remain in NPZ on the server.
        edges=np.r_[np.arange(start,end,43200.),end]
        pack={'mission':mission,'timestamp':((edges[:-1]+edges[1:])/2).tolist(),'bin_start':edges[:-1].tolist(),'bin_end':edges[1:].tolist(),'series':{}}
        mrow={'mission':mission,'window':'launch to latest lot landing','start':start,'end':end}
        for key,s in streams.items():
            a=np.maximum(edges[:-1],arrival);b=np.minimum(edges[1:],departure)
            valid=b>a
            support=np.where(valid,s.prefix(b,True)-s.prefix(a,True),0.)
            area=np.where(valid,s.prefix(b)-s.prefix(a),0.)
            values=np.divide(area,support/3600,out=np.full(len(a),np.nan),where=support>0)
            pack['series'][key]={'value':[None if not np.isfinite(v) else float(v) for v in values],
                'coverage':(support/(edges[1:]-edges[:-1])*100).round(3).tolist(),
                'status':['MEASURED_AGGREGATE' if v else 'UNAVAILABLE' for v in support],
                'source':SOURCES['radiation' if key.startswith('radiation') else 'cabin']}
            mrow[key+'_coverage_pct']=s.coverage(arrival,departure)*(departure-arrival)/(end-start)
        pack['cumulative_mGy']=(streams['radiation_combined'].prefix(np.clip(edges[1:],arrival,departure))-streams['radiation_combined'].prefix(arrival)).__truediv__(1000).tolist()
        # Event threshold based on actual per-sensor samples inside the mission storage envelope.
        v=rad[(rad.seconds>=arrival)&(rad.seconds<=departure)].absorbed_dose_rate
        pack['radiation_p95_uGy_h']=float(v.quantile(.95))
        mrow.update(pressure_coverage_pct=0.,oxygen_coverage_pct=0.)
        mission_cov.append(mrow);mission_series[mission]=pack
        write_json(DATA/'missions'/f'{mission}.json',pack)
    pd.DataFrame(mission_cov).to_csv(TABLES/'environment_coverage_by_mission.csv',index=False)
    # Declare candidate specifications before accessing evaluation outcomes.
    write_json(DATA/'protocol.json',{'version':VERSION,'engines':FEATURES,'candidate_selection':'Fixed before Phase D holdout runs; no target-adaptive revision',
        'demonstration_pair':['Caffeine','Diazepam'],'rationale':'Contrast polar methylxanthine solid with lipophilic benzodiazepine solution; chosen from chemistry not errors',
        'radiation_max_gap_seconds':300,'cabin_max_gap_seconds':600,'bootstrap_draws':400,'seed':20260920,
        'caveat':'Retrospective masked replay; Phase B/C outcomes already informed the chemistry baseline. Not prospectively blinded external validation.'})
    registry={};evaluations=[]
    for held_count,filename in [(1,'historical_replay_validation.csv'),(2,'ltdo_validation.csv')]:
        result,models=run(frame,held_count)
        registry.update(models);evaluations.append(result)
        result.drop(columns='contributions').to_csv(TABLES/filename,index=False)
    evaluation=pd.concat(evaluations,ignore_index=True)
    summary=pd.DataFrame([{'validation':v,'model':m,**metrics(g)} for (v,m),g in evaluation.groupby(['validation_type','model'])])
    summary.to_csv(TABLES/'model_environment_comparison.csv',index=False)
    pd.DataFrame([{'validation_type':v,'model':m,'held_out_pair':pair,**metrics(g)} for (v,m,pair),g in evaluation.groupby(['validation_type','model','held_out_pair'])]).to_csv(TABLES/'phase_d_fold_metrics.csv',index=False)
    evaluation.groupby(['validation_type','model','test_api']).absolute_error.agg(['count','mean','median','max']).to_csv(TABLES/'phase_d_per_api_error.csv')
    # Preserve candidate version and exact split models as transparent JSON coefficients.
    write_json(SIM/'models/phase_d_v0/registry.json',{'version':VERSION,'target':'100*(flight-ground)/ground','dataset_sha256':original,'software':{'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__},'models':registry})
    full=fit(frame,FEATURES['A']);_,_,domain=assess(frame,frame)
    full['domain']=domain
    write_json(DATA/'private/full_research_model.json',full)
    write_json(DATA/'private/validation.json',evaluation.to_dict('records'))
    write_json(DATA/'catalog.json',{'version':VERSION,'lots':lots,'apis':sorted(frame.api.unique()),'summary':summary.to_dict('records'),
        'disclosures':['Retrospective masked validation; published results were available in prior phases.',
        'Orbit and Earth geometry are schematic; solar lighting is not a model input.',
        'Station sensors are proxies. Package location and transfer times remain uncertain.',
        'Coverage uses supported unique intervals. No pressure or oxygen telemetry exists locally.']})
    manifest={'version':VERSION,'created_utc':datetime.now(timezone.utc).isoformat(),'v2_sha256':original,
        'sources':[{'path':str(p.relative_to(SIM.parent)),'sha256':digest(p)} for p in [source,SIM/'data/interim/radiation_cleaned.csv.gz',*sorted((SIM/'data/raw/environment/cabin').glob('*_telemetry.json'))]],
        'numeric_streams':{k:{'samples':len(s.t),'supported_segments':len(s.left)} for k,s in streams.items()},
        'browser_bins_hours':12,'radiation_gap_seconds':300,'cabin_gap_seconds':600}
    write_json(DATA/'manifest.json',manifest)
    figures(frame,evaluation,summary,cov,mission_series)
    docs(frame,evaluation,summary,cov,compare)
    assert digest(source)==original,'Authoritative V2 changed'
    print(summary.to_string(index=False),flush=True)

def figures(frame,ev,summary,cov,missions):
    radiation=[];cumulative=[]
    for name,p in missions.items():
        t=(np.array(p['timestamp'])-p['bin_start'][0])/86400
        radiation.append((t,np.array(p['series']['radiation_combined']['value'],dtype=float),name))
        cumulative.append((t,p['cumulative_mGy'],name))
    plot('historical_radiation','Station radiation: 12-hour supported means','Days since delivery launch','Dose rate (uGy/hour)',radiation)
    plot('cumulative_radiation','Observed station proxy dose; gaps not filled','Days since delivery launch','Cumulative dose (mGy)',cumulative)
    keys=['radiation_combined','temperature','relative_humidity','co2','pressure','oxygen']
    fig,ax=plt.subplots(figsize=(9,9));im=ax.imshow(cov[[k+'_coverage_pct' for k in keys]],vmin=0,vmax=100,cmap='viridis',aspect='auto')
    ax.set_xticks(range(6),['Radiation','Temperature','RH','CO2','Pressure','Oxygen']);ax.set_yticks(range(32),cov.lot_id,fontsize=7)
    fig.colorbar(im,label='Supported time / launch-to-landing window (%)');fig.tight_layout();fig.savefig(FIG/'environmental_coverage_matrix.png',dpi=240);plt.close(fig)
    for validation in ['LODO','LTDO']:
        fig,ax=plt.subplots(figsize=(7,6))
        for engine in ['A','B']:
            g=ev[(ev.validation_type==validation)&(ev.model==engine)];ax.scatter(g.actual_delta_api,g.predicted_delta_api,s=20,alpha=.65,label='Engine '+engine)
        low,high=ax.get_ylim();ax.plot([low,high],[low,high],'k--',lw=.7)
        ax.set(xlabel='Published delta API (%)',ylabel='Held-out predicted delta API (%)',title=validation+' grouped validation');ax.legend();fig.tight_layout();fig.savefig(FIG/f'predicted_vs_measured_{validation.lower()}.png',dpi=240);plt.close(fig)
    per=ev.groupby(['test_api','validation_type','model']).absolute_error.mean().unstack([1,2])
    ax=per.plot.bar(figsize=(11,5),rot=25);ax.set(ylabel='Mean absolute error (percentage points)',title='API errors, including repeated LTDO predictions');plt.tight_layout();plt.savefig(FIG/'per_api_error.png',dpi=240);plt.close()
    ax=summary.pivot(index='validation',columns='model',values='mae').plot.bar(rot=0,figsize=(7,5));ax.set(ylabel='MAE (percentage points)',title='Chemistry-only A versus environment-aware B');plt.tight_layout();plt.savefig(FIG/'chemistry_vs_environment.png',dpi=240);plt.close()
    g=ev[(ev.validation_type=='LODO')&(ev.model=='A')].reset_index(drop=True)
    fig,ax=plt.subplots(figsize=(12,5));ax.vlines(np.arange(len(g)),g.uncertainty_lower,g.uncertainty_upper,color='#477baf',alpha=.6);ax.scatter(np.arange(len(g)),g.predicted_delta_api,label='Prediction');ax.scatter(np.arange(len(g)),g.actual_delta_api,marker='x',label='Published')
    ax.set_xticks(np.arange(len(g)),g.lot_id,rotation=90,fontsize=7);ax.set(ylabel='Delta API (%)',title='Approximate 95% group-bootstrap predictive intervals; uncalibrated');ax.legend();fig.tight_layout();fig.savefig(FIG/'prediction_intervals.png',dpi=240);plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,5));ax.scatter(frame.days_in_space,frame.replay_dose_mGy);ax.set(xlabel='Published duration (days)',ylabel='Observed station proxy dose (mGy)',title='Duration versus reconstructed exposure');fig.tight_layout();fig.savefig(FIG/'duration_vs_radiation.png',dpi=240);plt.close(fig)
    fig,axes=plt.subplots(len(missions),1,figsize=(11,10))
    for ax,(mission,p) in zip(axes,missions.items()):
        mat=np.array([p['series'][k]['coverage'] for k in keys[:4]])
        ax.imshow(mat,aspect='auto',vmin=0,vmax=100,extent=[0,(p['bin_end'][-1]-p['bin_start'][0])/86400,4,0],cmap='viridis');ax.set_yticks(np.arange(4)+.5,['Rad','Temp','RH','CO2'],fontsize=7);ax.set_title(mission,fontsize=9)
    axes[-1].set_xlabel('Days since launch; dark bins show missingness');fig.tight_layout();fig.savefig(FIG/'telemetry_availability_timeline.png',dpi=240);plt.close(fig)

def docs(frame,ev,summary,cov,compare):
    def score(v,m):return summary[(summary.validation==v)&(summary.model==m)].iloc[0]
    a,b=score('LODO','A'),score('LODO','B');ta,tb=score('LTDO','A'),score('LTDO','B')
    caffeine=ev[(ev.validation_type=='LODO')&(ev.model=='A')&(ev.test_api=='Caffeine')]
    worst=ev[(ev.validation_type=='LTDO')&(ev.model=='A')].groupby('held_out_pair').absolute_error.mean().sort_values(ascending=False)
    per=ev[(ev.validation_type=='LODO')&(ev.model=='A')].groupby('test_api').absolute_error.mean().sort_values(ascending=False)
    paired=ev[(ev.validation_type=='LTDO')&(ev.model=='A')&(ev.held_out_pair=='Caffeine + Diazepam')]
    merged=ev.merge(cov,on=['lot_id','mission']).query("model == 'A' and validation_type == 'LODO'")
    correlations={k:float(merged.absolute_error.corr(merged[k],method='spearman')) for k in ['domain_distance','radiation_combined_coverage_pct']}
    method='''# Historical simulator method

The archive contains 32 lots representing eight APIs. V2 is immutable; SHA-256 and source hashes are recorded in data/simulator/manifest.json. Mission timestamps are inherited from V2, not newly established package-level facts. The earlier reports overstate certainty: the source builder assigns NG-11 departure to Cygnus although samples supposedly return on Dragon. Phase D flags that interval as uncertain and makes no claim of a verified three-week sample return transit. Other exact downmass links also need source review. Postflight storage and assay delays remain potential confounders.

## Historical exposure

Full-resolution cleaned DosTel1/2 data remain distinct. Within each instrument, consecutive valid readings at most 300 seconds apart define a supported piecewise-linear segment. This reflects the archive cadence and conservatively avoids long outages. On overlapping segments, the combined estimate is the equal sensor mean; elsewhere it uses the single supported sensor. It is a station proxy, not absorbed dose inside a drug package. Never sum detector doses. Exact clipped trapezoids convert uGy/hour times seconds / 3600 / 1000 to mGy. Prefix integrals make replay independent of playback speed. Integration is limited to inherited arrival/departure bounds. Launch/return exposure is unavailable. One-hour gap sensitivity and legacy V2 dose comparisons are saved separately.

Cabin records are deduplicated per timestamp/field, ignoring null duplicates and retaining means if non-null records conflict. Source JSONs remain immutable. Interpolation spans at most ten minutes; no long gap is filled. Unique supported seconds define coverage, divided by the whole lot flight duration. This corrects Phase B row-count coverage inflation. Radiation spatial relevance is D (Columbus proxy), cabin is E because sensor identity/locality was not established. Pressure and oxygen remain null.

NPZ streams store original time/value arrays plus supported intervals once for all lots. Six mission JSON streams contain 12-hour supported means and support percentages; empty bins are null. Bins are for visualization only. Live values and cumulative dose use full-resolution server arrays. Displayed event threshold is the 95th percentile of raw sensor samples in the mission storage envelope; it denotes an elevated observation, not a biological threshold. Downsampling may hide peaks on the chart, so event status uses the live stream.

## Validation and uncertainty

A fixed OLS chemistry baseline (TPSA, XLogP, MW) and fixed OLS chemistry plus replay dose candidate are refitted for every fold. No Phase D feature or parameter tuning follows held-out errors. Scaling, coefficients, chemical-domain cutoffs, bootstrap refits and residuals use only training APIs. Outcomes are joined for scoring after predictions are frozen. All 28 LTDO pairs run; each lot appears in seven pairs. Pooled LTDO rows are dependent, not 224 independent observations. This is retrospective masking with known historical outcomes, not prospective blinded external validation; earlier baseline selection used this dataset.

Uncertainty uses 400 training-API bootstrap draws and hierarchical draws from inner leave-API-out residuals. The 2.5/97.5 percentiles form approximate, uncalibrated predictive intervals conditional on the fixed model. Rank-deficient bootstrap refits are counted and retained as minimum-norm solutions; this and the small number of chemistries limit interval trust. Negative relative potency below -100% is mathematically unphysical; such interval endpoints are shown as a model limitation, not clipped to imply calibration. Interval coverage is measured only after generation.

Domain distances use only unique training-API chemistry centroids and their scaler. Median leave-centroid-out nearest-neighbor distance defines IN_DOMAIN, up to the largest training nearest-neighbor distance is NEAR_BOUNDARY, beyond is OUT_OF_DOMAIN. These empirical heuristic thresholds are not a statistical guarantee. Mahalanobis distance is avoided with six to eight molecular entities.

The UI receives no outcome in its catalog or replay payload. Completion records endpoint predictions, then a separate server reveal action joins assay outcomes. The explicit Validation Lab exposes outcomes for analysis. This is masking against accidental viewing, not an adversarial security protocol. Runs persist locally as JSON. Scientific contributions are intercept and coefficient times feature in delta-API percentage points, never causal factor percentages. No dynamic potency curve is generated.

## Sources and implementation

[NASA RadLab](https://visualization.osdr.nasa.gov/radlab/gui/overview/), [EDA](https://visualization.osdr.nasa.gov/eda/), [grouped validation documentation](https://scikit-learn.org/stable/modules/cross_validation.html), local Phase A/B/C artifacts and original study DOI 10.1177/10806032261466966. The Three.js 0.170.0 renderer is locally vendored with its MIT license. Procedural continents, orbit, station geometry, sunlight and star field are schematic visual elements; no ephemeris is claimed. Only radiation particle intensity responds to observed dose rate. Reduced-motion settings suppress decorative animation.
'''
    (SIM/'docs/HISTORICAL_SIMULATOR_METHOD.md').write_text(method,encoding='utf-8')
    ltdo=f'''# Leave-two-drugs-out validation

All 28 API pairs were evaluated on both fixed engines, fitting six APIs per fold. There are 224 repeated lot predictions per engine. No test API enters scaling, fitting, bootstrap draws or residual estimation. See phase_d_fold_metrics.csv and ltdo_validation.csv.

| Engine | Pooled R2 | RMSE | MAE | Median AE | Worst pair MAE |
|---|---:|---:|---:|---:|---:|
| A chemistry | {ta.r2:.4f} | {ta.rmse:.4f} | {ta.mae:.4f} | {ta.median_ae:.4f} | {ta.worst_pair_mae:.4f} |
| B chemistry + dose | {tb.r2:.4f} | {tb.rmse:.4f} | {tb.mae:.4f} | {tb.median_ae:.4f} | {tb.worst_pair_mae:.4f} |

Worst A pair: {worst.index[0]}, MAE {worst.iloc[0]:.3f} percentage points. Caffeine + Diazepam demonstration MAE {paired.absolute_error.mean():.3f}. That pair was chosen for chemistry/formulation contrast before examining pair errors. A pooled interval coverage {ta.empirical_interval_coverage:.1%}, mean width {ta.mean_interval_width:.2f}; these intervals are approximate and uncalibrated. Repeated pair predictions are dependent; no independent-row significance test is used. This is a harder stress test with less training diversity, not an external validation cohort.
'''
    (SIM/'docs/LTDO_VALIDATION.md').write_text(ltdo,encoding='utf-8')
    improves=b.mae<a.mae and b.rmse<a.rmse
    answers=[
        'All 32 inherited mission windows have replay infrastructure, but complete actual local environments are NOT reconstructed. Telemetry gaps, package location and return-manifest uncertainty remain.',
        'DosTel radiation and intermittent EDA temperature, RH and CO2 are measured station data. Between readings, short interpolation and integrated dose are derived.',
        f'Cabin support is sparse: mean temperature {cov.temperature_coverage_pct.mean():.1f}%, RH {cov.relative_humidity_coverage_pct.mean():.1f}%, CO2 {cov.co2_coverage_pct.mean():.1f}%. Pressure and oxygen have zero historical coverage.',
        'Live values have measured/interpolated/unavailable status; dose is derived; final delta API is predicted; the Earth/orbit/station/sun are decorative schematic geometry.',
        f'Engine A LODO R2 {a.r2:.4f}, RMSE {a.rmse:.4f}, MAE {a.mae:.4f} percentage points; it reproduces the M4 benchmark.',
        f'Engine B LODO R2 {b.r2:.4f}, RMSE {b.rmse:.4f}, MAE {b.mae:.4f}. Improvement on both errors: {"YES" if improves else "NO"}.',
        f'LTDO A R2 {ta.r2:.4f}, RMSE {ta.rmse:.4f}, MAE {ta.mae:.4f}; B MAE {tb.mae:.4f}. See the separate pair report.',
        f'Caffeine LODO MAE {caffeine.absolute_error.mean():.4f}, mean prediction {caffeine.predicted_delta_api.mean():.4f}, published mean {caffeine.actual_delta_api.mean():.4f}. All four caffeine lots are absent from its fit.',
        f'Caffeine + Diazepam LTDO MAE {paired.absolute_error.mean():.4f}; worst of all pairs is {worst.index[0]} ({worst.iloc[0]:.4f}).',
        f'Largest Engine A LODO API errors: {per.index[0]} ({per.iloc[0]:.3f}) and {per.index[1]} ({per.iloc[1]:.3f}) percentage points.',
        f'Exploratory LODO A Spearman error/domain-distance association {correlations["domain_distance"]:.3f}; repeated lots and eight APIs preclude strong inferential claims.',
        f'Exploratory LODO A error/radiation-coverage association {correlations["radiation_combined_coverage_pct"]:.3f}; this is not proof that missingness causes errors.',
        f'For the fixed additive radiation test, improvement in both pooled LODO errors: {"YES" if improves else "NO"}. No radiation causal effect is established.',
        'No additional cabin factor is supported for primary prediction at this coverage. No invented environmental weights are fitted.',
        'No causal contribution percentages. Linear terms can be decomposed additively in delta-API percentage points, dependent on units and correlated inputs.',
        'Suitable for retrospective research exploration with explicit missingness, provenance and uncertainty; not a clinical tool or validated potency simulator.',
        'Descriptor-based research-only endpoint estimates are supported with intervals and prominent domain warnings. There is no validated hypothetical environmental response or molecular SMILES parser.',
        'Highest priorities: additional unseen APIs, matched controlled radiation experiments, repeated potency timepoints, package-level telemetry, exact downmass/storage/assay linkage and independently audited digitization.'
    ]
    text='# Phase D historical pharmaceutical simulator\n\n'+'\n\n'.join(f'## Q{i+1}\n\n{a}' for i,a in enumerate(answers))
    text+='\n\n## Readiness\n\n3D HISTORICAL SPACE ENVIRONMENT: COMPLETE as schematic visualization, not historical ephemeris.\n\nMISSION TELEMETRY REPLAY: COMPLETE for acquired streams; historical coverage remains incomplete.\n\nCAFFEINE BLINDED REPLAY: COMPLETE as retrospective outcome-masked replay.\n\n8-API LODO REPLAY: COMPLETE.\n\nTWO-DRUG LTDO: COMPLETE (28 pairs).\n\nSCIENTIFIC SIMULATOR UI: COMPLETE; see test evidence.\n\nENVIRONMENT-AWARE MODEL IMPROVES BASELINE: '+('YES in this fixed exploratory comparison' if improves else 'NO')+'.\n\nREADY FOR RESEARCH-ONLY NEW DRUG SIMULATION: YES for endpoint descriptor dry runs; no validated kinetics.\n\nREADY FOR FINAL MODEL FREEZE: NO.\n\nREADY FOR VULNERABILITY RANKING: NO.\n\nSTOP FOR REVIEW.\n'
    (SIM/'docs/PHASE_D_SIMULATOR_REPORT.md').write_text(text,encoding='utf-8')

if __name__=='__main__':build()
