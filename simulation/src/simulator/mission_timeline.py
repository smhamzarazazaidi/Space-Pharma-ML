import pandas as pd

def seconds(value):
    return pd.Timestamp(value, tz='UTC').timestamp() if not isinstance(value, (int,float)) else float(value)

def boundaries(lot):
    return [seconds(lot[k]) for k in ('launch_datetime','docking_datetime','departure_datetime','landing_datetime')]

def phase(lot, time):
    launch, arrival, departure, landing = boundaries(lot)
    if time <= launch: return 'LAUNCH'
    if time < arrival: return 'TRANSIT'
    if time < departure: return 'ISS STORAGE'
    if time < landing: return 'RETURN / TRANSFER UNCERTAIN' if lot['mission']=='NG-11' else 'RETURN'
    return 'LANDING'

def cursor(lot, progress):
    start, _, _, end = boundaries(lot)
    return start + min(1.,max(0.,float(progress)))*(end-start)

