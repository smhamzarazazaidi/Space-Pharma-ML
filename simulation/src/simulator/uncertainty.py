import numpy as np
import pandas as pd
from .stability_engine import fit,predict

def intervals(training, inputs, features, seed=20260920, draws=400):
    """Approximate group-bootstrap predictive distribution, conditional on fixed model.

    Hyperparameters absent. Residual API and row drawn hierarchically; no held-out outcomes.
    Rank-deficient replicates are retained with minimum-norm solutions and counted.
    """
    rng=np.random.default_rng(seed)
    apis=sorted(training.api.unique())
    residuals=[]
    for api in apis:
        tr=training[training.api!=api]; te=training[training.api==api]
        residuals.append(te.delta_api_percent.to_numpy()-predict(fit(tr,features),te))
    samples=[]; deficient=0
    for _ in range(draws):
        boot=pd.concat([training[training.api==a] for a in rng.choice(apis,len(apis),replace=True)])
        m=fit(boot,features)
        deficient+=m['rank'] < len(features)+1
        error=rng.choice(residuals[rng.integers(len(residuals))],len(inputs))
        samples.append(predict(m,inputs)+error)
    low,high=np.percentile(samples,[2.5,97.5],axis=0)
    return low, high, deficient/draws

