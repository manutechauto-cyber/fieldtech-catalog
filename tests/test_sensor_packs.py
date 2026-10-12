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

    def test_lmt_switch_on_delay_model_exclusions(self):
        for model in ('LMT100','LMT110','LMT121'):
            _,p=self.load(model)
            self.assertNotIn('manual_dS1',{x['id'] for x in p['parameters']})
        _,p=self.load('LMT102')
        self.assertIn('manual_dS1',{x['id'] for x in p['parameters']})
        event=next(x for x in p['diagnostics'] if x['id']=='manual_0x7710')
        self.assertEqual(event['severity'],'error')

    def test_sa_dual_analogue_and_switching_variants_differ(self):
        _,analog=self.load('SA4114');_,switching=self.load('SA4110')
        ap={x['id']:x for x in analog['parameters']}
        sp={x['id']:x for x in switching['parameters']}
        self.assertIn('OUT1 temperature',ap['manual_ASP1']['description']['en'])
        self.assertIn('OUT2 flow',ap['manual_ASP2']['description']['en'])
        self.assertNotIn('manual_ASP1',sp)
        self.assertNotIn('manual_ou2',{x['id'] for x in analog['parameters']})

    def test_zebra_backup_interrupt_and_restore_reboot(self):
        _,p=self.load('FS40-SR20D4-2C00W')
        procedures={x['id']:x for x in p['procedures']}
        self.assertIn('interrupts',procedures['depth_backup']['description']['en'])
        self.assertIn('reboots',procedures['depth_restore']['description']['en'])
        self.assertNotIn('backupProcedure',p['configurationUnknowns'])
        self.assertIn('firmwareCompatibility',p['configurationUnknowns'])

    def test_pressure_new_variants_have_switching_output_two(self):
        for model in ('PN7012','PN7014'):
            _,p=self.load(model)
            ids={x['id'] for x in p['parameters']}
            self.assertIn('SP2',ids)
            self.assertNotIn('ASP2',ids)
            self.assertIn('mode 2/3',p['coverage']['limitations']['en'])

    def test_omron_fiber_bank_and_io_link_limits(self):
        _,standard=self.load('E3NX-FA11 2M');_,advanced=self.load('E3NX-FA21 2M');_,io=self.load('E3NX-FA51-IL3 2M')
        self.assertNotIn('ops4_bank',{x['id'] for x in standard['parameters']})
        self.assertIn('ops4_bank',{x['id'] for x in advanced['parameters']})
        self.assertNotIn('ops4_user_save',{x['id'] for x in io['procedures']})
        self.assertEqual(next(x['value'] for x in io['parameters'] if x['id']=='ops4_SHS'),50)
        self.assertFalse(any(x['source']['documentId']=='ops4_e3nxil' for x in standard['parameters']))

    def test_datalogic_delay_is_variant_specific(self):
        _,basic=self.load('TL46-W-815');_,enhanced=self.load('TL46-WLF-815')
        self.assertEqual(next(x['value'] for x in basic['parameters'] if x['id']=='ops4_delay'),20)
        self.assertEqual(next(x['value'] for x in enhanced['parameters'] if x['id']=='ops4_dLOn'),{'min':0,'max':100,'step':1})
        self.assertNotIn('ops4_dLOn',{x['id'] for x in basic['parameters']})
        _,knob=self.load('TL46-A-415')
        self.assertIn('ops4_sensitivity',{x['id'] for x in knob['parameters']})
        self.assertNotIn('ops4_mark_background',{x['id'] for x in knob['procedures']})

    def test_installation_supplement_is_distinct_from_operating_manual(self):
        entry,p=self.load('IFS204')
        self.assertEqual(p['coverage']['scope'],'installation-field-subset')
        self.assertFalse(p['coverage']['fullManualTranscribed'])
        sources=copy.deepcopy(self.sources)
        for x in p['procedures']:
            sources[x['source']['documentId']].pop('kind',None)
        with self.assertRaisesRegex(ValueError,'Installation provenance'):
            validate_pack(p,entry,self.type_ids,sources)

    def test_fixed_cylinder_variants_do_not_inherit_io_link(self):
        for model in ('MK5100','MK5103','MK5110','MK5114','MK5140','MK5156','MK5351'):
            _,p=self.load(model)
            self.assertFalse(any(x['id'].startswith('close5_') for x in p['software']))
            self.assertIn('close5_alignment',{x['id'] for x in p['procedures']})
        _,p=self.load('KI6000')
        self.assertIn('close5_io_link',{x['id'] for x in p['software']})

    def test_f430_run_and_camera_save_are_separate(self):
        _,p=self.load('F430-F000N12M-RRA')
        rows={x['id']:x for x in p['procedures']}
        self.assertIn('automatically downloads',rows['close5_run_job']['description']['en'])
        self.assertIn('separate steps',rows['close5_save_job']['description']['en'])
        self.assertIn('firmwareCompatibility',p['configurationUnknowns'])

    def test_w9_opaque_teach_knob_and_output_polarities(self):
        for model in ('WL9L-3P2432','WL9L-3N2432'):
            _,p=self.load(model)
            rows={x['id']:x for x in p['parameters']}
            self.assertEqual(rows['retry6_opaque_teach']['value'],'> 2')
            self.assertEqual(rows['retry6_standard_reserve']['value'],4)
            self.assertIn('LG',rows['retry6_opaque_teach']['source']['applicability'])
            self.assertFalse(any('8 seconds' in x['description']['en'] for x in p['procedures']))
            state=next(x['description']['en'] for x in p['diagnostics'] if x['id']=='retry6_output_state')
            self.assertIn('light path free',state)
            self.assertIn('HIGH' if '-3P' in model else 'LOW',state)
        for model in ('WTB9L-3P2461','WTB9L-3N2461'):
            _,p=self.load(model)
            self.assertIn('retry6_distance_knob',{x['id'] for x in p['parameters']})
            self.assertNotIn('retry6_opaque_teach',{x['id'] for x in p['parameters']})
            state=next(x['description']['en'] for x in p['diagnostics'] if x['id']=='retry6_output_state')
            self.assertIn('object detected',state)
            self.assertIn('HIGH' if '-3P' in model else 'LOW',state)
