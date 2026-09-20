"""Local-only simulator service. python simulation/src/serve_phase_d.py --port 8765"""
import argparse,json,uuid,threading,mimetypes
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime,timezone
from simulator import DATA,SIM,VERSION
import pandas as pd
import numpy as np
from simulator.environment_loader import load_streams,sample
from simulator.mission_timeline import cursor
from simulator.simulation_logger import save
from simulator.stability_engine import predict,FEATURES,fit,contributions
from simulator.domain_checker import assess
from simulator.uncertainty import intervals


class ResearchService:
    def __init__(self,log_dir=None):
        self.catalog=json.loads((DATA/'catalog.json').read_text())
        self.lots={r['lot_id']:r for r in self.catalog['lots']}
        self.results=json.loads((DATA/'private/validation.json').read_text())
        self.registry=json.loads((SIM/'models/phase_d_v0/registry.json').read_text())['models']
        self.streams=load_streams();self.runs={};self.lock=threading.RLock()
        self.log_dir=log_dir or SIM/'results/simulation_runs'

    def create(self,body):
        held=sorted(set(body.get('held_out_apis',[])));lot_ids=body.get('lot_ids',[])
        if len(held) not in (1,2) or not set(held)<=set(self.catalog['apis']):raise ValueError('Select one or two distinct held-out APIs')
        if len(lot_ids)!=len(held) or any(l not in self.lots for l in lot_ids):raise ValueError('Select one flown lot per held-out API')
        if {self.lots[l]['api'] for l in lot_ids}!=set(held):raise ValueError('Lot selections must match held-out APIs')
        keys=[f'{len(held)}:{" + ".join(held)}:{e}' for e in ('A','B')]
        run={'simulation_id':str(uuid.uuid4()),'created_utc':datetime.now(timezone.utc).isoformat(),'mode':'HISTORICAL_REPLAY',
            'lot_ids':lot_ids,'apis':held,'missions':[self.lots[l]['mission'] for l in lot_ids],
            'environment_data_version':VERSION,'model_version':'D-v0','validation_type':'LODO' if len(held)==1 else 'LTDO',
            'held_out_apis':held,'training_api_count':8-len(held),'fold_keys':keys,'progress':0.,'revealed':False,
            'coverage_metrics':{l:self.lots[l]['coverage'] for l in lot_ids},'prediction':None,'published_result':None}
        self.runs[run['simulation_id']]=run;save(self.log_dir,run)
        return run

    def advance(self,run,progress):
        progress=float(progress)
        if not np.isfinite(progress) or not 0<=progress<=1:raise ValueError('Progress must be between 0 and 1')
        run['progress']=progress
        samples={l:sample(self.streams,self.lots[l],cursor(self.lots[l],progress)) for l in run['lot_ids']}
        result={'progress':progress,'samples':samples,'prediction':None,'published_result':None}
        if progress==1:
            predictions=[]
            for r in self.results:
                if r['fold_key'] in run['fold_keys'] and r['lot_id'] in run['lot_ids']:
                    predictions.append({k:v for k,v in r.items() if k not in ('actual_delta_api','absolute_error','signed_error')})
            run['prediction']=predictions;result['prediction']=predictions
            save(self.log_dir,run)
        if run['revealed'] and progress==1:result['published_result']=run['published_result']
        save(self.log_dir,run)
        return result

    def reveal(self,run):
        if run['progress']!=1 or run['prediction'] is None:raise ValueError('Complete replay before revealing published results')
        rows=[r for r in self.results if r['fold_key'] in run['fold_keys'] and r['lot_id'] in run['lot_ids']]
        run['published_result']=rows;run['revealed']=True;save(self.log_dir,run)
        return {'published_result':rows}

    def hypothetical(self,body):
        values={f:float(body[f]) for f in FEATURES['A']}
        if not all(np.isfinite(v) for v in values.values()) or values['molecular_weight']<=0 or values['tpsa']<0:raise ValueError('Enter finite, physically admissible descriptors')
        training=pd.read_csv(SIM/'data/processed/master_dataset_v2_verified.csv')
        inputs=pd.DataFrame([values]);m=fit(training,FEATURES['A'])
        distance,status,_=assess(training,inputs);p=float(predict(m,inputs)[0]);low,high,deficient=intervals(training,inputs,FEATURES['A'])
        run={'simulation_id':str(uuid.uuid4()),'mode':'HYPOTHETICAL_LAB','api':str(body.get('api','Hypothetical'))[:120],
            'model_version':'D-v0-A','environment_data_version':None,'validation_type':'NONE_NOT_EXTERNAL_VALIDATION','held_out_apis':[],
            'inputs':values,'prediction':p,'uncertainty_lower':float(low[0]),'uncertainty_upper':float(high[0]),'domain_status':str(status[0]),
            'domain_distance':float(distance[0]),'published_result':None,'error':None,'coverage_metrics':None,
            'warning':'SIMULATED MODEL PREDICTION - NOT EXPERIMENTAL DATA. No environmental or kinetic response.',
            'bootstrap_rank_deficient_fraction':deficient}
        save(self.log_dir,run);return run


def handler(service):
    class Handler(BaseHTTPRequestHandler):
        def send(self,code,data,kind='application/json'):
            payload=json.dumps(data,allow_nan=False).encode() if kind=='application/json' else data
            self.send_response(code);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(payload)))
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(payload)

        def do_GET(self):
            path=urlparse(self.path).path
            try:
                if path=='/api/catalog':return self.send(200,service.catalog)
                if path=='/api/validation':return self.send(200,service.results)
                if path.startswith('/api/mission/'):
                    name=path.split('/')[-1]
                    if name not in {r['mission'] for r in service.catalog['lots']}:raise ValueError('Unknown mission')
                    return self.send(200,json.loads((DATA/'missions'/f'{name}.json').read_text()))
                root=(SIM/'app').resolve();file=(root/('index.html' if path=='/' else path.lstrip('/'))).resolve()
                if not file.is_relative_to(root) or not file.is_file():return self.send(404,{'error':'Not found'})
                kind='text/javascript' if file.suffix=='.js' else (mimetypes.guess_type(file.name)[0] or 'application/octet-stream')
                self.send(200,file.read_bytes(),kind)
            except ValueError as e:self.send(400,{'error':str(e)})

        def do_POST(self):
            # Local research service: reject cross-origin browser writes and oversized requests.
            origin=self.headers.get('Origin')
            if origin and origin not in (f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'):
                return self.send(403,{'error':'Origin not allowed'})
            try:
                length=int(self.headers.get('Content-Length',0))
                if length>10000:raise ValueError('Request too large')
                body=json.loads(self.rfile.read(length));path=urlparse(self.path).path
                with service.lock:
                    if path=='/api/run':return self.send(200,service.create(body))
                    if path=='/api/hypothetical':return self.send(200,service.hypothetical(body))
                    parts=path.strip('/').split('/')
                    if len(parts)!=4 or parts[:2]!=['api','run'] or parts[2] not in service.runs:raise ValueError('Unknown run')
                    run=service.runs[parts[2]]
                    if parts[3]=='advance':return self.send(200,service.advance(run,body['progress']))
                    if parts[3]=='reveal':return self.send(200,service.reveal(run))
                    raise ValueError('Unknown action')
            except (ValueError,KeyError,TypeError) as e:self.send(400,{'error':str(e)})

        def log_message(self,*args):pass
    return Handler

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);args=parser.parse_args()
    service=ResearchService();server=ThreadingHTTPServer(('127.0.0.1',args.port),handler(service))
    print(f'Spaceflight pharmaceutical simulator: http://127.0.0.1:{args.port}',flush=True)
    server.serve_forever()
