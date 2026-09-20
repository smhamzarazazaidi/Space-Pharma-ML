"""Archive explicitly specified public NASA URLs without overwriting raw bytes."""
import argparse
import hashlib
import json
import urllib.request
import concurrent.futures
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parents[1]

def collect(url, relative):
    if urlparse(url).scheme != 'https' or urlparse(url).hostname != 'visualization.osdr.nasa.gov':
        raise ValueError('Only public NASA OSDR visualization URLs are allowed')
    target = (BASE / 'data/raw/environment' / relative).resolve()
    target.relative_to((BASE / 'data/raw/environment').resolve())
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        print('Preserved existing archive:', target)
        return
    request = urllib.request.Request(url, headers={'User-Agent': 'ISS-Pharmaceutical-Exposure-Audit/1.0'})
    with urllib.request.urlopen(request, timeout=45) as response:
        payload = response.read()
        metadata = dict(url=url, resolved_url=response.url, status=response.status,
                        content_type=response.headers.get('Content-Type'),
                        retrieved_utc=datetime.now(timezone.utc).isoformat(),
                        bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest(),
                        path=str(target.relative_to(BASE)),
                        license='Publicly accessible; dataset-specific reuse terms require review')
    with target.open('xb') as stream:
        stream.write(payload)
    target.with_suffix(target.suffix + '.provenance.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    print(json.dumps(metadata))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url', nargs='?')
    parser.add_argument('relative_path', nargs='?')
    parser.add_argument('--overlapping-missions', action='store_true')
    args = parser.parse_args()
    if args.overlapping_missions:
        # Selected from the archived catalog. Date filters prevent unrelated eras.
        names=['RR-12','RR-17','RR-19','RR-23','RR-18','RR-10','RR-20']
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            jobs={pool.submit(collect,f'https://visualization.osdr.nasa.gov/eda/api/missions/{n}/telemetry_data/?start=2018-06-29T00:00:00Z&end=2022-11-07T00:00:00Z',f'cabin/{n}_telemetry.json'):n for n in names}
            for job in concurrent.futures.as_completed(jobs):
                try: job.result()
                except Exception as error: print(json.dumps({'mission':jobs[job],'error':str(error)}))
    else:
        collect(args.url, args.relative_path)
