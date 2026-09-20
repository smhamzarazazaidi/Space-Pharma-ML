import numpy as np

CHEMISTRY = ['tpsa', 'xlogp', 'molecular_weight']

def assess(training, inputs):
    """Only unique training API centroids determine scaling and empirical cutoffs."""
    x = training.groupby('api')[CHEMISTRY].mean().to_numpy(float)
    mean, sd = x.mean(0), x.std(0)
    sd = np.where(sd > 0, sd, 1.)
    z = (x-mean)/sd
    distance = np.sqrt(((z[:,None]-z[None,:])**2).sum(2))
    np.fill_diagonal(distance, np.inf)
    nn = distance.min(1)
    cut1, cut2 = np.median(nn), np.max(nn)
    test = (inputs[CHEMISTRY].to_numpy(float)-mean)/sd
    nearest = np.sqrt(((test[:,None]-z[None,:])**2).sum(2)).min(1)
    status = np.where(nearest <= cut1, 'IN_DOMAIN', np.where(nearest <= cut2, 'NEAR_BOUNDARY', 'OUT_OF_DOMAIN'))
    return nearest, status, {'mean':mean.tolist(),'sd':sd.tolist(),'centroids':z.tolist(), 'in_domain_cutoff':float(cut1),'outer_cutoff':float(cut2)}

