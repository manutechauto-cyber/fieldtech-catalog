# FieldTech Industrial Sensors

Sensor catalog version 5: **398 published packs** across 9 manufacturers and 23 type filters. Each pack is a selected field reference. Source checks cover 241 official document references (238 distinct PDFs); electrical operation has not been tested.

## Coverage and research scope

The initial target of 20 references per type is met. Selection is inferred field-service priority, not a proven worldwide model-sales ranking. Electrical/connector/decoder variants and documented emitter/receiver assemblies count as distinct references; a pair counts once. One canonical pack can appear in multiple filters.

| Type | Published references | Remaining to 20 |
| --- | ---: | ---: |
| Fotoelétrico emissor/receptor | 36 | 0 |
| Fotoelétrico com refletor | 36 | 0 |
| Fotoelétrico difuso | 20 | 0 |
| Fotoelétrico com supressão de fundo | 29 | 0 |
| Laser emissor/receptor | 20 | 0 |
| Laser com refletor | 20 | 0 |
| Laser de presença/difuso | 20 | 0 |
| Laser de distância/deslocamento | 21 | 0 |
| Detecção de transparentes | 22 | 0 |
| Fibra óptica e amplificador | 20 | 0 |
| Forquilha e detecção de etiquetas | 20 | 0 |
| Sensor de contraste | 22 | 0 |
| Proximidade indutiva | 20 | 0 |
| Proximidade capacitiva | 20 | 0 |
| Ultrassônico | 20 | 0 |
| Magnético de cilindro/posição | 20 | 0 |
| Pressão/vácuo | 20 | 0 |
| Temperatura | 20 | 0 |
| Nível | 20 | 0 |
| Vazão | 20 | 0 |
| Sensor de cor | 20 | 0 |
| Leitor industrial de códigos 1D | 21 | 0 |
| Leitor industrial de códigos 2D | 20 | 0 |

**No remaining selection positions**, but manual depth remains incomplete: **20 datasheet-field-subset**, **12 installation-field-subset**, **366 manual-field-subset**. No pack claims a full manual transcription. Datasheet packs contain verified identity/specifications and selected options; empty diagnostics or software sections explicitly require more research. Legacy documents establish the recorded facts, without confirming current availability or firmware compatibility.

## Published manufacturers

| Manufacturer | Packs |
| --- | ---: |
| Banner Engineering | 91 |
| Baumer | 1 |
| Datalogic | 10 |
| Omron | 83 |
| Pepperl+Fuchs | 2 |
| SICK | 42 |
| Turck | 1 |
| Zebra | 16 |
| ifm | 152 |

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

## Next manual research

Version 5 deepens 22 packs with 84 references, using five new original documents and two verified retained PDFs. Of the previous 41 datasheet-only packs, nine now have operating-manual excerpts, twelve have installation supplements, and twenty remain datasheet-only. Version 4 previously deepened 44 packs. Version 3 previously deepened 121 packs. Pressure, flow, temperature and level variants now include selected commissioning/diagnostic references. Zebra backup interrupts jobs and restore reboots the device; SICK permanent saving and external project backup are separate. Prioritize the remaining 20 datasheet-only packs and the 12 installation-only supplements, then complete parameter/diagnostic tables, wiring and software compatibility. [Per-pack completion queue](completion_queue.json) retains explicit gaps. [Research report](research_results.json) retains deferred leads and scope limitations. Zebra FS decoder licenses are recorded per exact SKU; VS camera variants are not counted as barcode readers. The Omron F430 example pack includes the A code-reading license, not the S vision-only license.

## Validation and incremental build

```sh
python scripts/validate_sensor_structure.py
python scripts/build_sensor_distribution.py
python scripts/build_cloud_database.py
python -m unittest discover -s tests -v
```

CI checks source identity, type mappings, document provenance, sensor archive contents, unified SQLite contents and checksums. The drive validator and legacy drive bundle remain independent. Grow coverage using official exact-model documentation; keep pending research outside published device packs. PDFs are linked, not redistributed.

## Optical and fibre variants reviewed in version 4

Omron standard amplifiers and IO-Link variants use distinct instruction sheets. Advanced E3NX bank/EEPROM functions are not assigned to standard models. Internal User Save is not inferred for IO-Link models. Datalogic TL46-A uses a sensitivity knob; W/WL pulse extension is 20 ms; WLF on/off delays are configurable to 100 ms. SICK opposed pairs retain alignment/TEACH procedures and WL4SLG transparent/opaque modes remain separate. Datasensing-hosted manuals identify Datalogic legacy products; current availability is still unverified.

## Installation evidence is separate from operating manuals

`installation-field-subset` contains selected installation instructions or Info cards, with source kind and applicability retained. It does not establish a complete operating manual, configurable software, alarm tables or an exact pinout. Fixed MK variants do not inherit MK59 IO-Link functions. F430 job download/run and Save to Camera are separate actions. Source registry counts refer to document records; duplicate retained PDF bytes are counted separately only when their provenance records differ.
