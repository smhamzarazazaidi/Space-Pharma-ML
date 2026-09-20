import json
import numpy as np
from . import DATA
from .exposure_integrator import Stream
from .mission_timeline import boundaries,phase

VARIABLES=['radiation_sensor1','radiation_sensor2','radiation_combined','temperature','relative_humidity','co2']
SOURCES={'radiation':'NASA RadLab / DosTel / Columbus, grade D station proxy','cabin':'NASA EDA ISS fields / RR-7, RR-12, RR-19, grade E (sensor location unresolved)'}

def load_streams():
    return {v:Stream.load(DATA/'environment_streams'/f'{v}.npz') for v in VARIABLES}

def sample(streams,lot,time):
    start,arrival,departure,end=boundaries(lot)
    on_station=arrival<=time<departure
    data={}
    for name,stream in streams.items():
        value,status=stream.sample(time) if on_station else (None,'UNAVAILABLE')
        data[name]={'value':value,'status':status,'spatial_relevance':'D' if name.startswith('radiation') else 'E',
                    'source':SOURCES['radiation' if name.startswith('radiation') else 'cabin']}
    for name in ('pressure','oxygen'):
        data[name]={'value':None,'status':'NO HISTORICAL DATA','spatial_relevance':'E'}
    data['cumulative_radiation_mGy']=streams['radiation_combined'].integral(arrival,min(max(time,arrival),departure))
    data['mission_phase']=phase(lot,time)
    data['timestamp']=time
    return data

