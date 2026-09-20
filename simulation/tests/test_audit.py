"""Boundary checks for audit calculations; no scientific observations are fabricated."""
import sys
import unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from audit_project import span_metrics

class TemporalSupportTests(unittest.TestCase):
    def test_no_data_means_full_missing_window(self):
        self.assertEqual(span_metrics([], '2020-01-01', '2020-01-02',300),(0,24))
    def test_long_gap_is_not_filled_and_duplicates_do_not_inflate(self):
        start=pd.Timestamp('2020-01-01').value//10**9
        times=[start,start,start+300,start+7200,start+7500]
        hours,gap=span_metrics(times,'2020-01-01','2020-01-01T03:00:00',300)
        self.assertAlmostEqual(hours,600/3600)
        self.assertAlmostEqual(gap,6900/3600)
    def test_boundary_clipping(self):
        start=pd.Timestamp('2020-01-01').value//10**9
        self.assertEqual(span_metrics([start-100,start+100,start+200], '2020-01-01','2020-01-01T00:05:00',300),(200/3600,100/3600))
    def test_nonpositive_window_rejected(self):
        with self.assertRaises(ValueError): span_metrics([], '2020-01-02','2020-01-01',300)

if __name__=='__main__': unittest.main()
