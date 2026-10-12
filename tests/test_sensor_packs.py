import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from validate_sensor_structure import validate_pack,validate
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'industrial/sensors'

class SensorPackTests(unittest.TestCase):
    def setUp(self):
        self.manifest=json.loads((BASE/'manifest.json').read_text())
        self.sources={x['id']:x for x in json.loads((BASE/'sources.json').read_text())['documents']}
        self.type_ids={x['id'] for x in self.manifest['types']}

    def load(self,model):
        entry=next(x for x in self.manifest['packs'] if x['model']==model)
        return entry,json.loads((ROOT/entry['path']).read_text())

    def test_analog_and_io_link_q4x_are_not_interchanged(self):
        _,analog=self.load('Q4XTULAF300-Q8');_,digital=self.load('Q4XTKLAF300-Q8')
        av={x['id']:x['value'] for x in analog['specifications']}
        dv={x['id']:x['value'] for x in digital['specifications']}
        self.assertEqual(av['connector'],'M12, 5-pin')
        self.assertEqual(dv['connector'],'M12, 4-pin')
        self.assertEqual(av['output'],'0...10 V')
        self.assertEqual(dv['ch1'],'IO-Link / push-pull output')

    def test_output_two_pressure_and_temperature_distinction(self):
        _,pn=self.load('PN7094');_,tn=self.load('TN2511')
        self.assertEqual(next(x['value'] for x in pn['specifications'] if x['id']=='out2'),'Switching output, pin 2')
        self.assertIn('Analog function',next(x['name']['en'] for x in tn['parameters'] if x['id']=='ou2'))
        self.assertNotIn('ASP2',{x['id'] for x in pn['parameters']})

    def test_wrong_source_domain_is_rejected(self):
        entry,pack=self.load('O5D100');sources=copy.deepcopy(self.sources)
        sources['o5d100']['url']='https://example.com/manual.pdf'
        with self.assertRaisesRegex(ValueError,'Nonofficial'):
            validate_pack(pack,entry,self.type_ids,sources)

    def test_page_outside_retained_document_is_rejected(self):
        entry,pack=self.load('O5D100');pack['specifications'][0]['source']['pages']=[9999]
        with self.assertRaisesRegex(ValueError,'source page'):
            validate_pack(pack,entry,self.type_ids,self.sources)

    def test_sales_ranking_claim_without_proof_is_rejected(self):
        entry,pack=self.load('O5D100');pack['selection']['salesRankingConfirmed']=True
        with self.assertRaisesRegex(ValueError,'Sales ranking'):
            validate_pack(pack,entry,self.type_ids,self.sources)

    def test_two_dimensional_reader_has_single_canonical_pack(self):
        _,p=self.load('V2D611R-MMSBE4')
        self.assertEqual(set(p['typeIds']),{'barcode-1d','code-reader-2d'})
        self.assertEqual(sum(x['model']==p['model'] for x in self.manifest['packs']),1)
        validate(BASE/'manifest.json')

    def test_reader_licenses_and_camera_exclusion(self):
        _,dpm=self.load('FS40-SR20D4-2C00W')
        _,standard=self.load('FS40-SR20Z4-2C00W')
        self.assertEqual(next(x['value'] for x in dpm['specifications'] if x['id']=='decoder'),'DPM with Fast 2D')
        self.assertEqual(next(x['value'] for x in standard['specifications'] if x['id']=='decoder'),'Standard 2D')
        self.assertFalse(any(x['manufacturer']=='Zebra' and x['model'].startswith('VS') for x in self.manifest['packs']))
        _,omron=self.load('F430-F000N12M-RRA')
        self.assertIn('code reading',omron['software'][0]['value'])

    def test_contrast_io_link_not_inherited_by_npn_variant(self):
        _,npn=self.load('E3S-DCN21');_,io=self.load('E3S-DCP21-IL3')
        self.assertEqual(npn['software'],[])
        self.assertIn('IO-Link',io['software'][0]['value'])

    def test_report_matches_manifest_and_document_registry(self):
        report=json.loads((BASE/'research_results.json').read_text())
        self.assertEqual(report['publishedPacks'],len(self.manifest['packs']))
        self.assertEqual(report['reviewedDocuments'],len(self.sources))
        for row in report['coverageByType']:
            typ=next(t for t in self.manifest['types'] if t['id']==row['typeId'])
            self.assertEqual(row['published'],len(typ['publishedPackIds']))
            self.assertEqual(row['remaining'],max(0,typ['target']-row['published']))
        self.assertEqual(report['remainingSelectionPositions'],sum(r['remaining'] for r in report['coverageByType']))
