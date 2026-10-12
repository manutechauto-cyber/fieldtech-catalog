# FieldTech Industrial Sensors

Sensor catalog version 1: **127 published packs** across 4 manufacturers and 23 type filters. Each pack is a selected field reference, not a complete manual. Source checks cover 32 official PDFs; electrical operation has not been tested.

## Coverage and remaining selection

Target: 20 exact models per type. Selection is inferred field-service priority, not a proven worldwide model-sales ranking. Connector/electrical variants are individually documented, but do not prove independent popularity. One canonical pack can appear in multiple filters.

| Type | Published references | Remaining to 20 |
| --- | ---: | ---: |
| Fotoelétrico emissor/receptor | 12 | 8 |
| Fotoelétrico com refletor | 16 | 4 |
| Fotoelétrico difuso | 16 | 4 |
| Fotoelétrico com supressão de fundo | 23 | 0 |
| Laser emissor/receptor | 4 | 16 |
| Laser com refletor | 4 | 16 |
| Laser de presença/difuso | 14 | 6 |
| Laser de distância/deslocamento | 21 | 0 |
| Detecção de transparentes | 18 | 2 |
| Fibra óptica e amplificador | 6 | 14 |
| Forquilha e detecção de etiquetas | 1 | 19 |
| Sensor de contraste | 1 | 19 |
| Proximidade indutiva | 1 | 19 |
| Proximidade capacitiva | 2 | 18 |
| Ultrassônico | 9 | 11 |
| Magnético de cilindro/posição | 1 | 19 |
| Pressão/vácuo | 18 | 2 |
| Temperatura | 1 | 19 |
| Nível | 1 | 19 |
| Vazão | 1 | 19 |
| Sensor de cor | 2 | 18 |
| Leitor industrial de códigos 1D | 2 | 18 |
| Leitor industrial de códigos 2D | 1 | 19 |

**289 selection positions remain**. Some filters exceed the initial target because already published models also satisfy those principles. The catalog is usable now; the 20-per-type research goal is unfinished.

## Published manufacturers

| Manufacturer | Packs |
| --- | ---: |
| Banner Engineering | 29 |
| Omron | 66 |
| SICK | 7 |
| ifm | 25 |

## Downloads

- [Manifest and exact models](manifest.json)
- [Official document references, revisions and SHA-256](sources.json)
- [Sensor release/checksum](release.json)
- [Sensor ZIP encoded as base64](catalog_bundle.b64)
- [Unified drives + sensors SQLite database](../../cloud/README.md)
- [Coverage and validation report](research_results.json)

Sensor-only ZIP contains manifest, source registry and all packs. Decode base64 and verify ZIP SHA-256 against release.json before extraction. The unified SQLite includes the original payloads and the document registry for offline lookup. Import and UI integration in the app remain separate work.

## Pack contract

Schema version 1 has canonical identity, type filters, model evidence, specifications, parameters, diagnostics, procedures, software and explicit configuration unknowns. Every published item has en/pt labels/descriptions and an official document ID, PDF page and applicability. Resolve document IDs in sources.json; document URLs, revisions and PDF hashes are retained there. IDs in parameters/diagnostics are lookup identifiers: some are literal display codes and some describe a function; they are not assumed register addresses.

Current values include units/ranges only where reviewed. Unknown fields do not mean an unsupported feature. Full pinouts and wiring diagrams are not imported in this release; use the official manual and exact variant. No sensor in this collection is presented as a personnel-safety device.

## Configuration and variant safeguards

- Q4X IO-Link uses M12 4-pin; analog Q4X uses M12 5-pin and 0–10 V or 4–20 mA according to exact code.
- E3Z emitter/receiver sets count once; standard through-beam component codes are retained from the official order table. Laser and LED are distinct from through-beam, retroreflective and diffuse principles.
- PN7 pressure output 2 is switching; TN2511 output 2 is analog. Parameters from one family are not substituted into the other.
- CSS/CSX IO-Link variants use SOPAS ET via SiLink or an IO-Link master; SDD and Data Storage are documented. Software/firmware version compatibility remains unknown.
- CLV620-0000 is the serial/cabled variant; no built-in Ethernet is inferred from other CLV models. Working-memory edits and permanent saving are separate.
- Lector61x replacement requires an identical product type and the saved .sopas project. No Read is not automatically a hardware fault.
- Fiber-amplifier reach depends on selected fiber and response mode; no fixed range is assigned to the amplifier alone.

## Validation and incremental build

```sh
python scripts/validate_sensor_structure.py
python scripts/build_sensor_distribution.py
python scripts/build_cloud_database.py
python -m unittest discover -s tests -v
```

CI checks source identity, type mappings, document provenance, sensor archive contents, unified SQLite contents and checksums. The drive validator and legacy drive bundle remain independent. Grow coverage using official exact-model documentation; keep pending research outside published device packs. PDFs are linked, not redistributed.
