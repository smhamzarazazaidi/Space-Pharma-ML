import numpy as np

FEATURES = {'A':['tpsa','xlogp','molecular_weight'], 'B':['tpsa','xlogp','molecular_weight','replay_dose_mGy']}
LABELS = {'A':'CHEMISTRY CORE OLS - PROVISIONAL RESEARCH MODEL', 'B':'CHEMISTRY + OBSERVED STATION DOSE OLS - EXPERIMENTAL'}

def fit(training, features):
    x = training[features].to_numpy(float)
    y = training.delta_api_percent.to_numpy(float)
    mean, sd = x.mean(0), x.std(0)
    sd = np.where(sd > 1e-12, sd, 1.)
    design = np.c_[np.ones(len(x)), (x-mean)/sd]
    beta = np.linalg.lstsq(design,y,rcond=None)[0]
    raw = beta[1:]/sd
    return {'features':features,'intercept':float(beta[0]-raw@mean),'coefficients':raw.tolist(),
            'scaler_mean':mean.tolist(),'scaler_sd':sd.tolist(),'rank':int(np.linalg.matrix_rank(design))}

def predict(model, inputs):
    return model['intercept']+inputs[model['features']].to_numpy(float)@np.array(model['coefficients'])

def contributions(model, row):
    return {'Intercept':model['intercept'], **{f:float(row[f]*b) for f,b in zip(model['features'],model['coefficients'])}}

