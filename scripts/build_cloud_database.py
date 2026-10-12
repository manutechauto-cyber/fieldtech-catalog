"""Build/check the downloadable industrial database using Python's stdlib only."""
import base64
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import tempfile
import zipfile
from validate_catalog import validate as validate_drives
from validate_sensor_structure import validate as validate_sensors
ROOT = Path(__file__).resolve().parents[1]

def collect(root):
    errors = validate_drives(root)
    if errors:
        raise ValueError('\n'.join(errors))
    sensors = validate_sensors(root / 'industrial/sensors/manifest.json')
    manifest = json.loads((root / 'manifest.json').read_text())
    records = []
    for item in manifest['packs']:
        path = item['url'].split('/main/', 1)[1]
        payload = json.loads((root / path).read_text())
        records.append({'id': item['packId'], 'category': 'drives', 'manufacturer': item['manufacturer'], 'model': item['family'], 'version': item['version'], 'path': path, 'payload': payload})
    for item in sensors['packs']:
        payload=json.loads((root/item['path']).read_text())
        records.append({'id':item['packId'],'category':'sensors','manufacturer':item['manufacturer'],'model':item['model'],'version':item['version'],'path':item['path'],'payload':payload})
    if len({x['id'] for x in records})!=len(records):
        raise ValueError('Duplicate cross-category pack IDs')
    sensors['sourceDocuments']=json.loads((root/'industrial/sensors/sources.json').read_text())['documents']
    return manifest, sensors, sorted(records, key=lambda x: x['id'])

def write_database(path, manifest, sensors, records):
    with sqlite3.connect(path) as db:
        db.executescript('''
        PRAGMA user_version=1;
        CREATE TABLE metadata(key TEXT PRIMARY KEY, value_json TEXT NOT NULL);
        CREATE TABLE device_packs(id TEXT PRIMARY KEY, category TEXT NOT NULL, manufacturer TEXT NOT NULL, model TEXT NOT NULL, version INTEGER NOT NULL CHECK(version>0), source_path TEXT NOT NULL UNIQUE, payload_json TEXT NOT NULL);
        CREATE INDEX device_lookup ON device_packs(category,manufacturer,model);
        CREATE TABLE sensor_types(id TEXT PRIMARY KEY, priority INTEGER NOT NULL, target INTEGER NOT NULL, payload_json TEXT NOT NULL);
        CREATE TABLE sensor_candidates(type_id TEXT NOT NULL REFERENCES sensor_types(id), model TEXT NOT NULL, status TEXT NOT NULL, payload_json TEXT NOT NULL, PRIMARY KEY(type_id,model));
        ''')
        metadata = {'databaseSchemaVersion': 1, 'drivesCatalogVersion': manifest['catalogVersion'], 'sensorManifest': sensors, 'sensorSources': sensors.get('sourceDocuments', []), 'hardwareTested': False}
        db.executemany('INSERT INTO metadata VALUES (?,?)', [(k,json.dumps(v,ensure_ascii=False,sort_keys=True)) for k,v in sorted(metadata.items())])
        db.executemany('INSERT INTO device_packs VALUES (?,?,?,?,?,?,?)', [(x['id'],x['category'],x['manufacturer'],x['model'],x['version'],x['path'],json.dumps(x['payload'],ensure_ascii=False,sort_keys=True)) for x in records])
        for item in sensors['types']:
            db.execute('INSERT INTO sensor_types VALUES (?,?,?,?)',(item['id'],item['priority'],item['target'],json.dumps(item,ensure_ascii=False,sort_keys=True)))
            for candidate in item['candidates']:
                db.execute('INSERT INTO sensor_candidates VALUES (?,?,?,?)',(item['id'],candidate['model'],candidate['status'],json.dumps(candidate,ensure_ascii=False,sort_keys=True)))
        if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise ValueError('Database integrity check failed')

def artifacts(root=ROOT):
    manifest,sensors,records=collect(root)
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/'fieldtech-industrial.sqlite'
        write_database(path,manifest,sensors,records)
        raw=path.read_bytes()
    index={'schemaVersion':1,'distributionVersion':1,'drivesCatalogVersion':manifest['catalogVersion'],'counts':{'publishedDrives':sum(x['category']=='drives' for x in records),'publishedSensors':sum(x['category']=='sensors' for x in records),'sensorTypes':len(sensors['types']),'sensorCandidates':sum(len(x['candidates']) for x in sensors['types'])},'packs':[{k:v for k,v in x.items() if k!='payload'} for x in records],'sensorTypes':sensors['types']}
    index_bytes=(json.dumps(index,ensure_ascii=False,indent=2)+'\n').encode()
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as z:
        for name,content in [('fieldtech-industrial.sqlite',raw),('index.json',index_bytes)]:
            info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,content)
    bundle=buf.getvalue()
    release={'schemaVersion':1,'databaseSchemaVersion':1,'drivesCatalogVersion':manifest['catalogVersion'],'counts':index['counts'],'bundle':{'url':'https://raw.githubusercontent.com/manutechauto-cyber/fieldtech-catalog/main/cloud/industrial_database.b64','encoding':'base64-zip','sha256':hashlib.sha256(bundle).hexdigest(),'bytes':len(bundle)},'database':{'filename':'fieldtech-industrial.sqlite','sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)},'indexUrl':'https://raw.githubusercontent.com/manutechauto-cyber/fieldtech-catalog/main/cloud/index.json','scope':'Downloadable read-only catalog; no live Supabase deployment is asserted'}
    return {'index.json':index_bytes,'release.json':(json.dumps(release,ensure_ascii=False,indent=2)+'\n').encode(),'industrial_database.b64':(base64.b64encode(bundle).decode()+'\n').encode()}

def verify(root=ROOT):
    expected=artifacts(root)
    cloud=root/'cloud'
    if (cloud/'index.json').read_bytes()!=expected['index.json']:
        raise ValueError('Cloud index stale')
    release=json.loads((cloud/'release.json').read_text())
    expected_release=json.loads(expected['release.json'])
    for key in ('schemaVersion','databaseSchemaVersion','drivesCatalogVersion','counts','indexUrl','scope'):
        if release[key]!=expected_release[key]:
            raise ValueError(f'Cloud release stale: {key}')
    zipped=base64.b64decode((cloud/'industrial_database.b64').read_text().strip(),validate=True)
    if hashlib.sha256(zipped).hexdigest()!=release['bundle']['sha256'] or len(zipped)!=release['bundle']['bytes']:
        raise ValueError('Bundle checksum/size mismatch')
    if release['bundle']['url']!=expected_release['bundle']['url'] or release['bundle']['encoding']!='base64-zip':
        raise ValueError('Unexpected bundle endpoint/encoding')
    with zipfile.ZipFile(io.BytesIO(zipped)) as z:
        if z.testzip() or set(z.namelist())!={'fieldtech-industrial.sqlite','index.json'}:
            raise ValueError('Invalid database archive')
        raw=z.read('fieldtech-industrial.sqlite')
        if z.read('index.json')!=expected['index.json']:
            raise ValueError('Bundled index stale')
    if hashlib.sha256(raw).hexdigest()!=release['database']['sha256'] or len(raw)!=release['database']['bytes']:
        raise ValueError('Database checksum/size mismatch')
    with tempfile.TemporaryDirectory() as temp:
        actual=Path(temp)/'actual.sqlite';actual.write_bytes(raw)
        baseline=Path(temp)/'expected.sqlite'
        manifest,sensors,records=collect(root)
        write_database(baseline,manifest,sensors,records)
        with sqlite3.connect(actual) as db, sqlite3.connect(baseline) as reference:
            if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok' or db.execute('PRAGMA user_version').fetchone()[0]!=1:
                raise ValueError('Invalid SQLite integrity/schema version')
            if list(db.iterdump())!=list(reference.iterdump()):
                raise ValueError('Cloud database contents/schema stale')
    print('Cloud database validated')


def run(root=ROOT,check=False):
    if check:
        verify(root)
        return
    expected=artifacts(root)
    for name,data in expected.items():
        path=root/'cloud'/name
        if check:
            if not path.exists() or path.read_bytes()!=data:
                raise ValueError(f'Cloud database stale: {name}; run scripts/build_cloud_database.py')
        else:
            path.parent.mkdir(exist_ok=True);path.write_bytes(data)
    print('Cloud database validated' if check else 'Cloud database built and validated')

if __name__=='__main__':
    import sys
    run(check='--check' in sys.argv)
