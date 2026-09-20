from itertools import combinations
import numpy as np
import pandas as pd
from .stability_engine import FEATURES,fit,predict,contributions
from .uncertainty import intervals
from .domain_checker import assess

def run(frame, held_count, draws=400):
    rows=[]; registry={}
    for number,held in enumerate(combinations(sorted(frame.api.unique()),held_count)):
        training=frame[~frame.api.isin(held)].copy()
        inputs=frame[frame.api.isin(held)].drop(columns=['delta_api_percent','flight_percent_api_remaining','ground_control_percent_api_remaining','stability_ratio_percent'])
        assert not set(training.api)&set(inputs.api)
        distance,status,domain=assess(training,inputs)
        pair=' + '.join(held)
        for engine,features in FEATURES.items():
            model=fit(training,features)
            predictions=predict(model,inputs)
            low,high,deficient=intervals(training,inputs,features,seed=20260920+number,draws=draws)
            key=f'{held_count}:{pair}:{engine}'
            registry[key]={**model,'training_apis':sorted(training.api.unique()),'held_out_apis':list(held),'domain':domain,'model_id':f'D-v0-{engine}','uncertainty_method':'Approximate 95% group-bootstrap predictive interval; uncalibrated', 'bootstrap_rank_deficient_fraction':deficient}
            # Outcomes are joined only after all prediction, scaling, interval and domain work.
            actual=frame.set_index('lot_id').loc[inputs.lot_id,'delta_api_percent'].to_numpy()
            for i,(_,r) in enumerate(inputs.iterrows()):
                rows.append({'fold_key':key,'held_out_pair':pair,'test_api':r.api,'lot_id':r.lot_id,'mission':r.mission,
                    'predicted_delta_api':predictions[i],'actual_delta_api':actual[i],'absolute_error':abs(predictions[i]-actual[i]),
                    'signed_error':predictions[i]-actual[i],'uncertainty_lower':low[i],'uncertainty_upper':high[i],
                    'domain_status':status[i],'domain_distance':distance[i],'model':engine,'training_api_count':len(training.api.unique()),
                    'validation_type':'LODO' if held_count==1 else 'LTDO','contributions':contributions(model,r),
                    'bootstrap_rank_deficient_fraction':deficient})
        print(f'Validated {held_count}-drug holdout: {pair}',flush=True)
    return pd.DataFrame(rows),registry

def metrics(frame):
    e=frame.predicted_delta_api-frame.actual_delta_api
    return {'r2':float(1-(e**2).sum()/((frame.actual_delta_api-frame.actual_delta_api.mean())**2).sum()),
            'rmse':float(np.sqrt((e**2).mean())),'mae':float(e.abs().mean()),'median_ae':float(e.abs().median()),
            'max_ae':float(e.abs().max()),'worst_pair_mae':float(frame.groupby('held_out_pair').absolute_error.mean().max()),
            'empirical_interval_coverage':float(((frame.actual_delta_api>=frame.uncertainty_lower)&(frame.actual_delta_api<=frame.uncertainty_upper)).mean()),
            'mean_interval_width':float((frame.uncertainty_upper-frame.uncertainty_lower).mean())}

