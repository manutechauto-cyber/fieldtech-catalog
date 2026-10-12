import base64
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
import zipfile
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_cloud_database import artifacts, ROOT

class CloudDatabaseTests(unittest.TestCase):
    def test_snapshot_integrity_and_source_payloads(self):
        files=artifacts()
        release=json.loads(files['release.json'])
        zipped=base64.b64decode(files['industrial_database.b64'],validate=False)
        self.assertEqual(hashlib.sha256(zipped).hexdigest(),release['bundle']['sha256'])
        with zipfile.ZipFile(io.BytesIO(zipped)) as z:
            raw=z.read('fieldtech-industrial.sqlite')
        self.assertEqual(hashlib.sha256(raw).hexdigest(),release['database']['sha256'])
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'db.sqlite';p.write_bytes(raw)
            with sqlite3.connect(p) as db:
                self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0],'ok')
                rows=db.execute('SELECT source_path,payload_json FROM device_packs').fetchall()
                self.assertEqual(len(rows),len(json.loads((ROOT/'manifest.json').read_text())['packs'])+len(json.loads((ROOT/'industrial/sensors/manifest.json').read_text())['packs']))
                for source,payload in rows:
                    self.assertEqual(json.loads(payload),json.loads((ROOT/source).read_text()))
                self.assertEqual(db.execute('SELECT count(*) FROM sensor_types').fetchone()[0],23)
                self.assertEqual(db.execute("SELECT count(*) FROM device_packs WHERE category='sensors'").fetchone()[0],len(json.loads((ROOT/'industrial/sensors/manifest.json').read_text())['packs']))
                self.assertEqual(db.execute('SELECT count(*) FROM sensor_candidates').fetchone()[0],0)
                self.assertTrue(json.loads(db.execute("SELECT value_json FROM metadata WHERE key='sensorSources'").fetchone()[0]))

    def test_reproducible_distribution(self):
        self.assertEqual(artifacts(),artifacts())
