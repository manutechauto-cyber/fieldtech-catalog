"""Validate the sensor research queue; does not certify device specifications."""
import json
from pathlib import Path


def validate(path):
    data = json.loads(path.read_text())
    assert data['schemaVersion'] == 1
    assert data['domain'] == 'industrial' and data['category'] == 'sensors'
    assert data['targetModelsPerType'] == 20
    assert data['selectionPolicy']['salesRankingConfirmed'] is False
    ids = [entry['id'] for entry in data['types']]
    assert len(ids) == len(set(ids)) == 23
    for entry in data['types']:
        assert entry['target'] == 20 and entry['priority'] in (1, 2, 3)
        assert entry['name']['pt']
        assert isinstance(entry['candidates'], list)
        assert isinstance(entry['publishedPackIds'], list)
        if entry['id'].startswith('laser-'):
            assert entry['lightSource'] == 'laser'
    assert {'contrast', 'color', 'barcode-1d', 'code-reader-2d'} <= set(ids)
    contract = data['configurationResearchContract']
    assert contract['publicationEnabled'] is False
    assert {'softwareVersionCompatibility', 'firmwareCompatibility', 'backupProcedure', 'restoreProcedure', 'persistentSaveProcedure'} <= set(contract['fields'])
    assert 'unknown' in contract['capabilityStates']
    # Publishing requires a separate specification validator and bundle implementation.
    assert data['packs'] == [], 'Sensor publication is not enabled by this structure validator'
    assert all(not entry['publishedPackIds'] for entry in data['types'])
    return data


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    result = validate(root / 'industrial/sensors/manifest.json')
    print(f"Sensor structure valid: {len(result['types'])} types; no published packs")
