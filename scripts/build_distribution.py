"""Build a reproducible ZIP/base64 snapshot of exactly the live manifest packs."""
import base64
import io
import json
from pathlib import Path
import zipfile
from validate_catalog import validate

ROOT = Path(__file__).resolve().parents[1]


def build(root=ROOT):
    errors = validate(root)
    if errors:
        raise ValueError('\n'.join(errors))
    manifest = json.loads((root / 'manifest.json').read_text())
    paths = ['manifest.json'] + [item['url'].split('/main/', 1)[1] for item in manifest['packs']]
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            info = zipfile.ZipInfo(path, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (root / path).read_bytes())
    encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
    (root / 'catalog_bundle.b64').write_text(encoded + '\n')
    parts = root / 'bundle_parts'
    parts.mkdir(exist_ok=True)
    for path in parts.glob('part*.b64'):
        path.unlink()
    for n, start in enumerate(range(0, len(encoded), 9000)):
        (parts / f'part{n:02}.b64').write_text(encoded[start:start + 9000])
    verify(root)
    return len(paths)


def verify(root=ROOT):
    manifest = json.loads((root / 'manifest.json').read_text())
    paths = ['manifest.json'] + [item['url'].split('/main/', 1)[1] for item in manifest['packs']]
    encoded = (root / 'catalog_bundle.b64').read_text().strip()
    chunks = ''.join(p.read_text() for p in sorted((root / 'bundle_parts').glob('part*.b64')))
    if chunks != encoded:
        raise ValueError('Bundle chunks do not match the complete bundle')
    with zipfile.ZipFile(io.BytesIO(base64.b64decode(encoded, validate=True))) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(paths):
            raise ValueError('Invalid ZIP entries')
        for path in paths:
            if archive.read(path) != (root / path).read_bytes():
                raise ValueError(f'Stale bundle content: {path}')


if __name__ == '__main__':
    import sys
    if '--check' in sys.argv:
        verify()
        print('Distribution matches live catalog')
    else:
        print(f'Built and verified {build()} distribution files')
