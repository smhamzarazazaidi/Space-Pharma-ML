"""Historical replay and grouped validation. No validated pharmaceutical kinetics."""
import os
import sys
from pathlib import Path

SIM = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SIM / '.deps'))
os.environ.setdefault('MPLCONFIGDIR', str(SIM / '.cache/matplotlib'))
DATA = SIM / 'data/simulator'
TABLES = SIM / 'results/tables'
VERSION = 'phase-d-v0'

