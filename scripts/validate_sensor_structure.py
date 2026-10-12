"""Validate sensor research, published packs and retained provenance."""
import json
from pathlib import Path
from urllib.parse import urlparse

VENDOR_DOMAINS={'SICK':('sick.com',),'Banner Engineering':('bannerengineering.com',),'Omron':('omron.eu','omron.com.au','ia.omron.com','omron-ap.com'),'ifm':('ifm.com',)}
SECTIONS=('specifications','parameters','diagnostics','procedures','software')

def require(condition,message):
    if not condition:
        raise ValueError(message)

def bilingual(value,label):
    require(isinstance(value,dict) and all(isinstance(value.get(k),str) and value[k].strip() for k in ('en','pt')),label+' needs en/pt')

def validate_pack(pack,entry,type_ids,registry):
    require(pack['schemaVersion']==1 and pack['category']=='sensors','Invalid sensor pack schema')
    for key in ('packId','manufacturer','model','version','path'):
        require(pack[key]==entry[key],f'Sensor identity mismatch: {key}')
    require(isinstance(pack['version'],int) and pack['version']>0,'Invalid pack version')
    require(pack['typeIds'] and set(pack['typeIds'])<=type_ids,'Unknown sensor type')
    require(pack['verification']['status']=='curated-field-subset-verified-v1','Unverified sensor pack')
    require(pack['verification']['factsVerified'] is True,'Unverified sensor facts')
    require(pack['verification']['hardwareTested'] is False,'Hardware verification not implemented')
    require(pack['selection']['salesRankingConfirmed'] is False,'Sales ranking not established')
    require(pack['modelEvidence'],'Model evidence required')
    require(pack['specifications'],'A published sensor pack needs specifications')
    domains=VENDOR_DOMAINS.get(pack['manufacturer'],())
    require(domains,'Manufacturer source allowlist missing')
    for section in ('modelEvidence',)+SECTIONS:
        items=pack[section]
        require(isinstance(items,list),'Section must be a list')
        codes=[x['id'] for x in items]
        require(len(codes)==len(set(codes)),f'Duplicate item in {section}')
        for item in items:
            bilingual(item['name'],item['id'])
            bilingual(item['description'],item['id'])
            src=item['source'];doc=registry.get(src['documentId'])
            require(doc is not None,'Unregistered source document')
            host=urlparse(doc['url']).hostname or ''
            require(doc['url'].startswith('https://') and any(host==d or host.endswith('.'+d) for d in domains),'Nonofficial vendor source')
            require(src['pages'] and all(isinstance(n,int) and not isinstance(n,bool) and 1<=n<=doc['pageCount'] for n in src['pages']),'Invalid source page')
            require(src['applicability'] and src['section'],'Source scope/section missing')
    require(pack['coverage']['scope'] in ('manual-field-subset','datasheet-field-subset'),'Missing scope')
    require(pack['coverage']['fullManualTranscribed'] is False,'Full manual not imported')
    require(pack['configurationUnknowns'] is not None,'Unknowns must be explicit')

def validate(path):
    data=json.loads(path.read_text());root=path.parents[2]
    require(data['schemaVersion']==1 and data['domain']=='industrial' and data['category']=='sensors','Invalid sensor manifest')
    require(data['targetModelsPerType']==20,'Invalid selection target')
    require(data['selectionPolicy']['salesRankingConfirmed'] is False,'Unsubstantiated ranking')
    ids=[x['id'] for x in data['types']]
    require(len(ids)==len(set(ids))==23,'Sensor taxonomy requires 23 unique types')
    registry_path=path.parent/'sources.json'
    registry=json.loads(registry_path.read_text())['documents'] if registry_path.exists() else []
    require(len({x['id'] for x in registry})==len(registry),'Duplicate source document IDs')
    for doc in registry:
        require(doc['official'] is True and doc['title'] and doc['revision'],'Missing document provenance')
        require(len(doc['sha256'])==64 and all(c in '0123456789abcdef' for c in doc['sha256']),'Invalid PDF checksum')
        require(isinstance(doc['pageCount'],int) and doc['pageCount']>0,'Invalid PDF page count')
    registry={x['id']:x for x in registry}
    pack_ids=[x['packId'] for x in data['packs']]
    require(len(pack_ids)==len(set(pack_ids)),'Duplicate sensor pack ID')
    paths=set()
    mappings={ident:[] for ident in ids}
    for entry in data['packs']:
        rel=Path(entry['path'])
        require(not rel.is_absolute() and '..' not in rel.parts and str(rel).startswith('industrial/sensors/packs/'),'Invalid pack path')
        require(str(rel) not in paths,'Duplicate sensor path');paths.add(str(rel))
        pack=json.loads((root/rel).read_text())
        validate_pack(pack,entry,set(ids),registry)
        for ident in pack['typeIds']:mappings[ident].append(pack['packId'])
    actual={str(x.relative_to(root)) for x in (path.parent/'packs').rglob('*.json')} if (path.parent/'packs').exists() else set()
    require(actual==paths,'Sensor manifest/file mismatch')
    for entry in data['types']:
        require(entry['target']==20 and entry['priority'] in (1,2,3),'Invalid type target/priority')
        require(entry['name']['pt'],'Missing type label')
        require(sorted(entry['publishedPackIds'])==sorted(mappings[entry['id']]),'Type/pack mapping mismatch')
        models=[x['model'] for x in entry['candidates']]
        require(len(models)==len(set(models)),'Duplicate research model')
        for candidate in entry['candidates']:
            require(candidate['manufacturer'] and candidate['published'] is False,'Candidate cannot be a published pack')
            require(candidate['status'] in ('pending-research','model-confirmed','manual-verified'),'Invalid candidate status')
            require(candidate['salesRankingConfirmed'] is False,'Candidate ranking unsupported')
            require(candidate['evidence'] and all(x['url'].startswith('https://') and x['scope'] for x in candidate['evidence']),'Candidate evidence missing')
        if entry['id'].startswith('laser-'):
            require(entry['lightSource']=='laser','Incorrect laser taxonomy')
    contract=data['configurationResearchContract']
    require({'contrast','color','barcode-1d','code-reader-2d'}<=set(ids),'Taxonomy missing readers/color')
    require({'softwareVersionCompatibility','firmwareCompatibility','backupProcedure','restoreProcedure','persistentSaveProcedure'}<=set(contract['fields']),'Configuration contract incomplete')
    require('unknown' in contract['capabilityStates'],'Unknown capability state missing')
    return data

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    result=validate(root/'industrial/sensors/manifest.json')
    print(f"Sensors valid: {len(result['types'])} types; {len(result['packs'])} published packs")
