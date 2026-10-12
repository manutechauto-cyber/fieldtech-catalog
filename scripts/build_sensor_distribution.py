"""Build/check sensor-only manifest/source/pack download, independent of legacy drives."""
import base64
import hashlib
import io
import json
from pathlib import Path
import zipfile
from validate_sensor_structure import validate
ROOT=Path(__file__).resolve().parents[1]
BASE='industrial/sensors/'

def paths(root):
    manifest=validate(root/BASE/'manifest.json')
    return [BASE+'manifest.json',BASE+'sources.json']+[x['path'] for x in manifest['packs']]

def build(root=ROOT):
    entries=paths(root);buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as archive:
        for path in entries:
            info=zipfile.ZipInfo(path,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,(root/path).read_bytes())
    raw=buf.getvalue();target=root/BASE
    (target/'catalog_bundle.b64').write_text(base64.b64encode(raw).decode()+'\n')
    manifest=json.loads((target/'manifest.json').read_text())
    release={'schemaVersion':1,'sensorCatalogVersion':manifest['sensorCatalogVersion'],'publishedPacks':len(manifest['packs']),'bundleUrl':'https://raw.githubusercontent.com/manutechauto-cyber/fieldtech-catalog/main/'+BASE+'catalog_bundle.b64','encoding':'base64-zip','sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'fileCount':len(entries)}
    (target/'release.json').write_text(json.dumps(release,indent=2)+'\n');verify(root)

def verify(root=ROOT):
    entries=paths(root);target=root/BASE;release=json.loads((target/'release.json').read_text());raw=base64.b64decode((target/'catalog_bundle.b64').read_text().strip(),validate=True)
    if hashlib.sha256(raw).hexdigest()!=release['sha256'] or len(raw)!=release['bytes']:
        raise ValueError('Sensor bundle checksum mismatch')
    manifest=json.loads((target/'manifest.json').read_text())
    if release['publishedPacks']!=len(manifest['packs']) or release['sensorCatalogVersion']!=manifest['sensorCatalogVersion'] or release['fileCount']!=len(entries):
        raise ValueError('Stale sensor release metadata')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if archive.testzip() or len(archive.namelist())!=len(entries) or set(archive.namelist())!=set(entries):
            raise ValueError('Invalid sensor archive')
        for path in entries:
            if archive.read(path)!=(root/path).read_bytes():
                raise ValueError(f'Stale sensor archive entry: {path}')
    print('Sensor distribution valid')

if __name__=='__main__':
    import sys
    verify() if '--check' in sys.argv else build()
