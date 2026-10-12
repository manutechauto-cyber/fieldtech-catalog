"""Regression checks for cross-family mistakes that matter during field use."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def pack(path):
    return json.loads((ROOT / path).read_text())


def codes(path, group):
    return {entry['code']: entry for entry in pack(path)[group]}


class FieldPackTests(unittest.TestCase):
    def test_pf523_does_not_inherit_pf525_ethernet_faults(self):
        self.assertNotIn('F073', codes('rockwell/pf523.json', 'faults'))
        self.assertIn('F073', codes('rockwell/pf525.json', 'faults'))

    def test_powerflex_frequency_parameter_numbers_are_family_specific(self):
        self.assertEqual(codes('rockwell/pf40.json', 'parameters')['P035']['unit'], 'Hz')
        self.assertEqual(codes('rockwell/pf525.json', 'parameters')['P035']['unit'], '')
        self.assertEqual(codes('rockwell/pf525.json', 'parameters')['P044']['unit'], 'Hz')

    def test_abb_speed_and_frequency_ramps_are_distinguished(self):
        p = codes('abb/acs480.json', 'parameters')
        self.assertEqual(p['23.12']['applicability'], 'Speed control ramp')
        self.assertEqual(p['28.72']['applicability'], 'Frequency control ramp')

    def test_matrix_drive_control_undervoltage_is_not_conventional_dc_bus(self):
        p = codes('yaskawa/u1000.json', 'parameters')
        self.assertIn('E1-22', p)
        self.assertNotIn('E1-01', p)
        self.assertIn('controle', codes('yaskawa/u1000.json', 'faults')['Uv1']['title']['pt'])

    def test_warning_is_not_labeled_as_trip(self):
        self.assertEqual(codes('weg/cfw300.json', 'faults')['A046']['kind'], 'warning')
        self.assertEqual(codes('weg/cfw300.json', 'faults')['F072']['kind'], 'fault')

    def test_specialized_speed_and_ramp_units(self):
        self.assertEqual(codes('invertek/optidrive_coolvert.json', 'parameters')['1-01']['unit'], 'rps')
        self.assertEqual(codes('control_techniques/unidrive_m200.json', 'parameters')['03']['unit'], 's/100 Hz')

    def test_unconfirmed_candidates_are_not_live_or_aliases(self):
        manifest = pack('manifest.json')
        families = ' '.join(p['family'].casefold() for p in manifest['packs'])
        for name in ['atv940', 'atv990']:
            self.assertNotIn(name, families)
            self.assertEqual(pack('requests/' + name + '.json')['status'], 'unconfirmed-model')
            for entry in manifest['packs']:
                p = pack(entry['url'].split('/main/')[1])
                self.assertNotIn(name, [a.casefold() for a in p.get('aliases', [])])

    def test_omron_stage_codes_do_not_inherit_other_vendor_order(self):
        f = codes('omron/jx.json', 'faults')
        self.assertIn('constante', f['E-01']['title']['pt'])
        self.assertIn('aceleração', f['E-03']['title']['pt'])

    def test_published_research_has_manual_provenance(self):
        research = pack('research/enrichment_results.json')
        for result in research['published']:
            p = pack(result['path'])
            self.assertTrue(p['verification']['parametersVerified'])
            self.assertTrue(p['verification']['faultsVerified'])
            for entry in p['parameters'] + p['faults']:
                self.assertTrue(entry['source']['document'])
                self.assertTrue(entry['source']['revision'])
                self.assertTrue(all(n > 0 for n in entry['source']['pages']))


if __name__ == '__main__':
    unittest.main()
