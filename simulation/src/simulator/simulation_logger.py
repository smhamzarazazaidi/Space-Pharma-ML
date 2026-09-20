import json
import os
from pathlib import Path

def save(directory, run):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    path=directory/(run['simulation_id']+'.json')
    temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(run,indent=2,allow_nan=False),encoding='utf-8')
    os.replace(temporary,path)
