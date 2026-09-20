"""Numerical, split-isolation, masking and persistence contract tests."""
import sys,json,unittest,tempfile,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from simulator import SIM,DATA
import numpy as np
import pandas as pd
from simulator.exposure_integrator import Stream,combine
from simulator.mission_timeline import boundaries,phase,cursor
from simulator.stability_engine import fit,predict,FEATURES
from simulator.domain_checker import assess
from simulator.uncertainty import intervals
from serve_phase_d import ResearchService

class IntegrationTests(unittest.TestCase):
    def test_units_constant(self):
        s=Stream([0,3600],[100,100],3600)
        self.assertAlmostEqual(s.integral(0,3600),.1)
    def test_clipped_linear(self):
        s=Stream([0,3600],[0,200],3600)
        self.assertAlmostEqual(s.integral(900,2700),.05)
    def test_long_gap_not_filled(self):
        s=Stream([0,100,10000,10100],[100]*4,300)
        self.assertIsNone(s.sample(5000)[0]);self.assertAlmostEqual(s.coverage(0,10100),200/101)
    def test_overlap_not_summed(self):
        a=Stream([0,100],[100,100]);b=Stream([0,100],[200,200])
        self.assertAlmostEqual(combine([a,b]).integral(0,100),150*100/3600000)
    def test_single_sensor_supported(self):
        a=Stream([0,100],[100,100]);b=Stream([200,300],[200,200]);s=combine([a,b])
        self.assertIsNone(s.sample(150)[0]);self.assertEqual(s.sample(50)[0],100)
    def test_status_distinction(self):
        s=Stream([0,100],[10,20]);self.assertEqual(s.sample(0)[1],'MEASURED');self.assertEqual(s.sample(50)[1],'SHORT_GAP_INTERPOLATED')
    def test_prefix_at_final_boundary(self):
        s=Stream([0,100],[100,100]);self.assertEqual(s.prefix(100),s.prefix(200));self.assertEqual(s.prefix(-100),0)

class ArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frame=pd.read_csv(SIM/'data/processed/master_dataset_v2_verified.csv')
        cls.registry=json.loads((SIM/'models/phase_d_v0/registry.json').read_text())
        cls.results=pd.read_csv(SIM/'results/tables/ltdo_validation.csv')
    def test_v2_immutable(self):
        actual=hashlib.sha256((SIM/'data/processed/master_dataset_v2_verified.csv').read_bytes()).hexdigest()
        self.assertEqual(actual,self.registry['dataset_sha256'])
    def test_all_pairs_and_lots(self):
        self.assertEqual(self.results.held_out_pair.nunique(),28);self.assertEqual(len(self.results),448)
        self.assertTrue((self.results.groupby(['model','lot_id']).size()==7).all())
    def test_fold_isolation(self):
        for m in self.registry['models'].values():
            self.assertFalse(set(m['training_apis'])&set(m['held_out_apis']))
            self.assertEqual(len(m['training_apis'])+len(m['held_out_apis']),8)
    def test_baseline_reproduction(self):
        c=pd.read_csv(SIM/'results/tables/model_environment_comparison.csv');a=c[(c.validation=='LODO')&(c.model=='A')].iloc[0]
        self.assertAlmostEqual(a.mae,2.770845,places=5);self.assertAlmostEqual(a.rmse,3.607573,places=5)
    def test_holdout_target_mutation_cannot_change_fit_or_interval(self):
        df=self.frame;held=['Caffeine','Diazepam'];tr=df[~df.api.isin(held)].copy();te=df[df.api.isin(held)][FEATURES['A']]
        changed=df.copy();changed.loc[changed.api.isin(held),'delta_api_percent']=100000
        tr2=changed[~changed.api.isin(held)].copy()
        np.testing.assert_allclose(predict(fit(tr,FEATURES['A']),te),predict(fit(tr2,FEATURES['A']),te))
        a=intervals(tr,te,FEATURES['A'],draws=15);b=intervals(tr2,te,FEATURES['A'],draws=15)
        np.testing.assert_allclose(a[0],b[0]);np.testing.assert_allclose(a[1],b[1])
    def test_domain_uses_unique_apis(self):
        tr=self.frame;te=tr.iloc[:1];a=assess(tr,te);b=assess(pd.concat([tr,tr[tr.api=='Caffeine']]*2),te)
        np.testing.assert_allclose(a[0],b[0]);self.assertEqual(a[1][0],b[1][0])
    def test_mission_boundaries_and_cursor(self):
        for _,r in self.frame.iterrows():
            t=boundaries(r);self.assertEqual(t,sorted(t));self.assertEqual(cursor(r,0),t[0]);self.assertEqual(cursor(r,1),t[-1]);self.assertEqual(phase(r,t[-1]),'LANDING')
    def test_missing_pressure_oxygen_and_coverage(self):
        c=pd.read_csv(SIM/'results/tables/environment_coverage_by_lot.csv')
        self.assertTrue((c.pressure_coverage_pct==0).all());self.assertTrue((c.oxygen_coverage_pct==0).all())
        self.assertTrue(c.filter(like='_coverage_pct').apply(lambda s:s.between(0,100).all()).all())
    def test_full_archive_loaded(self):
        m=json.loads((DATA/'manifest.json').read_text());self.assertGreater(sum(m['numeric_streams'][s]['samples'] for s in ['radiation_sensor1','radiation_sensor2']),2000000)
    def test_intervals_finite_and_ordered(self):
        self.assertTrue(np.isfinite(self.results[['uncertainty_lower','uncertainty_upper']]).all().all())
        self.assertTrue((self.results.uncertainty_lower<=self.results.uncertainty_upper).all())
    def test_descriptor_constants(self):
        self.assertTrue((self.frame.groupby('api')[FEATURES['A']].nunique()==1).all().all())

class ReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.service=ResearchService(Path(cls.temp.name))
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def new_run(self,pair=False):
        return self.service.create({'held_out_apis':['Caffeine','Diazepam'] if pair else ['Caffeine'], 'lot_ids':['DS01_01','DS01_16'] if pair else ['DS01_01']})
    def test_masking_and_reveal_gate(self):
        r=self.new_run();self.assertIsNone(r['prediction']);self.assertIsNone(r['published_result'])
        with self.assertRaises(ValueError):self.service.reveal(r)
        halfway=self.service.advance(r,.5);self.assertIsNone(halfway['prediction'])
        final=self.service.advance(r,1);self.assertEqual(len(final['prediction']),2)
        self.assertNotIn('actual_delta_api',json.dumps(final));self.assertNotIn('absolute_error',json.dumps(final))
        self.assertEqual(len(self.service.reveal(r)['published_result']),2)
    def test_pair_run_predictions_and_log(self):
        r=self.new_run(True);p=self.service.advance(r,1);self.assertEqual(len(p['prediction']),4);self.service.reveal(r)
        saved=json.loads((Path(self.temp.name)/(r['simulation_id']+'.json')).read_text())
        self.assertEqual(saved['training_api_count'],6);self.assertTrue(saved['revealed'])
    def test_speed_and_scrub_invariance(self):
        r=self.new_run();a=self.service.advance(r,1)['samples']['DS01_01']['cumulative_radiation_mGy']
        for p in [.1,.4,.8]:self.service.advance(r,p)
        b=self.service.advance(r,1)['samples']['DS01_01']['cumulative_radiation_mGy'];self.assertEqual(a,b)
    def test_public_catalog_no_outcomes(self):
        for l in self.service.catalog['lots']:
            self.assertNotIn('delta_api_percent',l);self.assertNotIn('flight_percent_api_remaining',l)
    def test_unknown_or_mismatched_lots_rejected(self):
        with self.assertRaises(ValueError):self.service.create({'held_out_apis':['Caffeine'],'lot_ids':['DS01_16']})
    def test_transit_unavailable(self):
        r=self.new_run();s=self.service.advance(r,0)['samples']['DS01_01'];self.assertIsNone(s['radiation_combined']['value']);self.assertIsNone(s['temperature']['value'])
    def test_hypothetical_ood_no_published_outcome(self):
        r=self.service.hypothetical({'api':'OOD test vector','tpsa':300,'xlogp':20,'molecular_weight':1000})
        self.assertEqual(r['domain_status'],'OUT_OF_DOMAIN');self.assertIsNone(r['published_result'])
        self.assertLessEqual(r['uncertainty_lower'],r['uncertainty_upper'])

if __name__=='__main__':unittest.main(verbosity=2)
