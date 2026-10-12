import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate_catalog.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        manifest = json.loads((ROOT / 'manifest.json').read_text())
        (self.root / 'manifest.json').write_text(json.dumps(manifest))
        for entry in manifest['packs']:
            rel = entry['url'].split('/main/')[1]
            target = self.root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / rel, target)
        shutil.copytree(ROOT / 'requests', self.root / 'requests')
        self.addCleanup(self.tmp.cleanup)

    def mutate(self, path, change):
        p = self.root / path
        data = json.loads(p.read_text())
        change(data)
        p.write_text(json.dumps(data))

    def test_current_catalog(self):
        self.assertEqual(validator.validate(self.root), [])

    def test_empty_published_pack(self):
        self.mutate('schneider/atv340.json', lambda d: d.update(parameters=[]))
        self.assertTrue(any('nonempty' in e for e in validator.validate(self.root)))

    def test_unsubstantiated_candidate(self):
        self.mutate('requests/atv990.json', lambda d: d.update(status='verified-ready'))
        self.assertTrue(any('verified-ready' in e for e in validator.validate(self.root)))

    def test_missing_manual_reference(self):
        self.mutate('schneider/atv340.json', lambda d: d['faults'][0].pop('source'))
        self.assertTrue(any('provenance' in e for e in validator.validate(self.root)))

    def test_version_mismatch(self):
        self.mutate('schneider/atv340.json', lambda d: d.update(version=99))
        self.assertTrue(any('mismatch' in e for e in validator.validate(self.root)))


if __name__ == '__main__':
    unittest.main()
