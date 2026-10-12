"""Validate downloadable packs without claiming legacy vendor verification."""
import json
from pathlib import Path
from urllib.parse import urlparse


def validate(root):
    manifest = json.loads((root / 'manifest.json').read_text())
    errors = []
    seen = set()
    for item in manifest['packs']:
        ident = item['packId']
        if ident in seen:
            errors.append(f'duplicate packId: {ident}')
        seen.add(ident)
        prefix = 'https://raw.githubusercontent.com/manutechauto-cyber/fieldtech-catalog/main/'
        if not item['url'].startswith(prefix):
            errors.append(f'{ident}: invalid pack URL')
            continue
        rel = item['url'][len(prefix):]
        path = Path(rel)
        if path.is_absolute() or '..' in path.parts:
            errors.append(f'{ident}: unsafe pack path')
            continue
        try:
            pack = json.loads((root / path).read_text())
        except (OSError, ValueError) as exc:
            errors.append(f'{ident}: {exc}')
            continue
        if (pack.get('packId'), pack.get('version')) != (ident, item['version']):
            errors.append(f'{rel}: manifest identity/version mismatch')
        for key, label in [('parameters', 'name'), ('faults', 'title')]:
            entries = pack.get(key)
            if not isinstance(entries, list) or not entries:
                errors.append(f'{rel}: {key} must be a nonempty list')
                continue
            codes = set()
            for entry in entries:
                code = entry.get('code')
                if not isinstance(code, str) or not code.strip() or code.casefold() in codes:
                    errors.append(f'{rel}: missing/duplicate {key} code {code!r}')
                if isinstance(code, str):
                    codes.add(code.casefold())
                names = entry.get(label)
                if not isinstance(names, dict) or not all(names.get(lang) for lang in ['en', 'pt']):
                    errors.append(f'{rel}: {code}: missing English/Portuguese {label}')
                if pack.get('verification', {}).get(key + 'Verified'):
                    source = entry.get('source', {})
                    host = urlparse(source.get('url', '')).hostname or ''
                    vendor_host = urlparse(pack.get('sourceUrl', '')).hostname or ''
                    if not (host and host == vendor_host and source.get('document') and source.get('revision') and source.get('pages')):
                        errors.append(f'{rel}: {code}: verified item requires vendor manual provenance')
    for path in (root / 'requests').glob('*.json'):
        request = json.loads(path.read_text())
        if request.get('status') == 'verified-ready':
            v = request.get('verification', {})
            if not all(v.get(k) for k in ['sourceVerified', 'parametersVerified', 'faultsVerified']):
                errors.append(f'{path.name}: verified-ready without full verification')
            if not any(e.get('official') for e in request.get('evidence', [])):
                errors.append(f'{path.name}: verified-ready without retained official evidence')
    return errors


if __name__ == '__main__':
    import sys
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print('Catalog validation passed')
