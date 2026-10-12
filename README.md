# FieldTech Drives Catalog

Downloadable field-reference catalog. Catalog version 27 contains 118 published packs across 29 manufacturer directories. These are selected subsets, not complete manufacturer manuals.

## Downloadable cloud database

[Cloud database and integration contract](cloud/README.md): a checksum-verified SQLite snapshot containing published drives, sensor types and research candidates. [Release](cloud/release.json) distinguishes published content from research. This does not assert deployment to an app or live Supabase database.

## Industrial expansion

[Industrial sensors](industrial/sensors/README.md): 398 published field-reference packs across 23 sensor and industrial code-reader type filters, with at least 20 documented references per type; full manual depth remains incomplete. Selection is inferred field-service priority, not a worldwide sales ranking. Version 3 deepens 121 sensor packs; 85 remain datasheet-only. Sensor ZIP and unified SQLite downloads are validated.

## Validation and evidence

Run `python scripts/validate_catalog.py` and `python -m unittest discover -s tests -v` before publication. CI checks every push and pull request. Published packs must contain English/Portuguese parameter names and fault titles, unique codes, and matching manifest identity/version. Items explicitly marked verified require document, revision, page and source references.

Legacy `curated-basic` status does not certify that every code has been checked against the latest manufacturer manual. `sourceVerified` alone does not verify parameters or faults. An Auto-Learn candidate remains pending until its retained evidence supports publication.

ATV340 version 2 contains 9 parameters, 6 faults and a field checklist checked against Schneider Electric NVE61643 revision 11. Its new content is in English and Portuguese; the catalog language list describes available languages across packs, not guaranteed translation coverage for every field.

## Published coverage

Counts are stored parameter/fault entries, not unique codes across the catalog.

| Directory | Models (parameters / faults) |
| --- | --- |
| abb | [ACS355](abb/acs355.json) (5 / 2); [ACS580](abb/acs580.json) (5 / 6); [ACS880](abb/acs880.json) (4 / 4); [ACS480](abb/acs480.json) (13 / 5); [ACS380](abb/acs380.json) (13 / 5); [ACH580](abb/ach580.json) (13 / 5); [ACQ580](abb/acq580.json) (13 / 5); [ACS550](abb/acs550.json) (12 / 10) |
| bonfiglioli | [Active Cube](bonfiglioli/active_cube.json) (5 / 4); [Agile](bonfiglioli/agile.json) (5 / 5); [S2U](bonfiglioli/s2u.json) (5 / 7) |
| bosch_rexroth | [EFC 3610](bosch_rexroth/efc3610.json) (5 / 13); [EFC 5610](bosch_rexroth/efc5610.json) (5 / 13) |
| control_techniques | [Commander C200](control_techniques/commander_c200.json) (7 / 9); [Commander C300](control_techniques/commander_c300.json) (7 / 9); [Unidrive M700](control_techniques/unidrive_m700.json) (7 / 8); [Digitax HD](control_techniques/digitax_hd.json) (6 / 7); [Unidrive M200/M201](control_techniques/unidrive_m200.json) (12 / 7) |
| danfoss | [VLT Midi Drive FC 280](danfoss/fc280.json) (7 / 4); [VLT AutomationDrive FC 302](danfoss/fc302.json) (7 / 4); [VLT HVAC Drive FC 102](danfoss/fc102.json) (9 / 9); [VLT Aqua Drive FC 202](danfoss/fc202.json) (9 / 9) |
| delta | [MS300](delta/ms300.json) (6 / 8); [C2000](delta/c2000.json) (6 / 10); [CP2000](delta/cp2000.json) (6 / 10); [VFD-E](delta/vfd_e.json) (6 / 8) |
| eaton | [PowerXL DG1](eaton/dg1.json) (7 / 8); [PowerXL DM1](eaton/dm1.json) (7 / 7); [PowerXL DA1](eaton/da1.json) (7 / 6); [PowerXL DE1](eaton/de1.json) (8 / 6) |
| emerson | [Commander SK](emerson/commander_sk.json) (6 / 7); [Unidrive SP](emerson/unidrive_sp.json) (7 / 7); [Mentor MP](emerson/mentor_mp.json) (6 / 6) |
| fuji | [FRENIC-Ace](fuji/frenic_ace.json) (9 / 14); [FRENIC-MEGA](fuji/frenic_mega.json) (9 / 13); [FRENIC-Mini](fuji/frenic_mini.json) (9 / 11); [FRENIC-HVAC](fuji/frenic_hvac.json) (9 / 12); [FRENIC-Lift LM1S](fuji/frenic_lift_lm1s.json) (7 / 11) |
| ge | [AF-650 GP](ge/af650_gp.json) (6 / 8); [AF-600 FP](ge/af600_fp.json) (6 / 7) |
| hitachi | [WJ200](hitachi/wj200.json) (7 / 8); [NE-S1](hitachi/nes1.json) (6 / 7); [WJ-C1](hitachi/wj_c1.json) (1 / 8); [SJ-P1](hitachi/sj_p1.json) (11 / 5) |
| honeywell | [SmartVFD COMPACT](honeywell/smartvfd_compact.json) (8 / 11) |
| invertek | [Optidrive E3](invertek/optidrive_e3.json) (6 / 6); [Optidrive P2](invertek/optidrive_p2.json) (7 / 7); [Optidrive HVAC Eco](invertek/optidrive_hvac_eco.json) (6 / 7); [Optidrive CoolVert](invertek/optidrive_coolvert.json) (8 / 7) |
| invt | [Goodrive20](invt/gd20.json) (10 / 13); [Goodrive200A](invt/gd200a.json) (10 / 13) |
| keb | [COMBIVERT F5](keb/combivert_f5.json) (6 / 6); [COMBIVERT F6](keb/combivert_f6.json) (6 / 6) |
| lenze | [i550](lenze/i550.json) (8 / 6); [i510](lenze/i510.json) (5 / 5); [8400 StateLine](lenze/8400_stateline.json) (5 / 7); [8400 HighLine](lenze/8400_highline.json) (5 / 7); [8200 Vector](lenze/8200_vector.json) (6 / 3); [9300 Vector](lenze/9300_vector.json) (5 / 4) |
| ls | [S100](ls/s100.json) (6 / 14); [G100](ls/g100.json) (6 / 14); [H100](ls/h100.json) (6 / 14); [iG5A](ls/ig5a.json) (5 / 11); [SV-iC5](ls/ic5.json) (9 / 6) |
| mitsubishi | [FREQROL FR-E800](mitsubishi/fr_e800.json) (7 / 13); [FREQROL FR-A800](mitsubishi/fr_a800.json) (7 / 15); [FREQROL FR-F800](mitsubishi/fr_f800.json) (6 / 13); [FREQROL FR-D700](mitsubishi/fr_d700.json) (8 / 14); [FREQROL FR-E700](mitsubishi/fr_e700.json) (9 / 9) |
| nord | [NORDAC PRO SK 500P](nord/sk500p.json) (8 / 7); [NORDAC LINK SK 250E-FDS](nord/sk250e_fds.json) (8 / 6) |
| omron | [3G3MX2-V2](omron/mx2_v2.json) (7 / 8); [3G3RX2](omron/rx2.json) (8 / 8); [SYSDRIVE JX](omron/jx.json) (7 / 8) |
| parker | [AC10](parker/ac10.json) (4 / 8); [AC15](parker/ac15.json) (4 / 6); [AC20](parker/ac20.json) (4 / 6) |
| rockwell | [PowerFlex 525](rockwell/pf525.json) (14 / 15); [PowerFlex 527](rockwell/pf527.json) (3 / 1); [PowerFlex 753](rockwell/pf753.json) (6 / 4); [PowerFlex 755](rockwell/pf755.json) (6 / 4); [PowerFlex 523](rockwell/pf523.json) (14 / 13); [PowerFlex 40](rockwell/pf40.json) (10 / 12) |
| schneider | [Altivar ATV320](schneider/atv320.json) (7 / 4); [Altivar Process ATV630](schneider/atv630.json) (14 / 10); [Altivar Process ATV930](schneider/atv930.json) (14 / 10); [ATV340](schneider/atv340.json) (9 / 6); [Altivar Process ATV950](schneider/atv950.json) (14 / 10); [Altivar Process ATV650](schneider/atv650.json) (14 / 10); [Altivar ATV12](schneider/atv12.json) (12 / 11) |
| sew | [MOVIFIT](sew/movifit.json) (5 / 4); [MOVIDRIVE](sew/movidrive.json) (4 / 2); [MOVITRAC B](sew/movitrac_b.json) (7 / 7) |
| siemens | [SINAMICS G120](siemens/g120.json) (7 / 5); [SINAMICS G120C](siemens/g120c.json) (7 / 4); [SINAMICS S120](siemens/s120.json) (4 / 4); [SINAMICS V90](siemens/v90.json) (4 / 1); [SINAMICS G120X](siemens/g120x.json) (4 / 3); [SINAMICS V20](siemens/v20.json) (11 / 6) |
| toshiba | [TOSVERT VF-S15](toshiba/vf_s15.json) (8 / 8); [TOSVERT VF-AS3](toshiba/vf_as3.json) (7 / 9); [TOSVERT VF-MB1](toshiba/vf_mb1.json) (8 / 8); [TOSVERT VF-nC3](toshiba/vf_nc3.json) (10 / 9) |
| vacon | [VACON 10](vacon/vacon10.json) (6 / 11); [VACON 20](vacon/vacon20.json) (6 / 11); [VACON 100](vacon/vacon100.json) (7 / 16); [VACON NXP](vacon/nxp.json) (4 / 17) |
| weg | [CFW500](weg/cfw500.json) (6 / 3); [CFW700](weg/cfw700.json) (4 / 3); [CFW900](weg/cfw900.json) (3 / 4); [CFW300](weg/cfw300.json) (9 / 6); [CFW-11](weg/cfw11.json) (9 / 6) |
| yaskawa | [GA500](yaskawa/ga500.json) (10 / 14); [GA800](yaskawa/ga800.json) (8 / 11); [A1000](yaskawa/a1000.json) (8 / 10); [V1000](yaskawa/v1000.json) (8 / 10); [U1000 Matrix Drive](yaskawa/u1000.json) (9 / 6); [J1000](yaskawa/j1000.json) (8 / 8) |

## Next filling sequence

1. Validate and deepen PF525, G120/G120C, FC302, ATV320 and ACS580 diagnostics and commissioning.
2. Resolve PF527 motion-specific references, V90 coverage and SEW variant applicability; expand WJ-C1.
3. Expand PF753/PF755, ATV630/ATV930, ACS880 and CFW500/700/900.
4. Standardize troubleshooting, checklists, translations and provenance in the remaining packs.
5. Add new families using actual field requests. ATV940 and ATV990 remain candidates, not published packs.

This order is a technical recommendation, not measured usage. Vendor codes, reset behavior and parameter applicability must be checked for the exact hardware, firmware and manual revision before further enrichment.

## Distribution

`manifest.json` and referenced JSON files are the live catalog. `catalog_bundle.b64` is a base64 ZIP snapshot of those files. `bundle_parts` contains ordered 9,000-character chunks of the same snapshot. The population workflow validates decoded content before committing all manifest-referenced packs.

## Global candidate enrichment (v27)

29 missing family packs were added and PF525, ATV630 and ATV930 were expanded using manufacturer manuals. The catalog now contains 874 parameter entries and 941 fault/warning entries. New field content is English/Portuguese; legacy translations are retained. The new subsets remain selected field references, not complete manuals.

[Candidate review](research/README.md) documents published families, additional researched gaps, applicability, access limitations and the distinction between global supplier presence and unverified model-level sales rankings. [Machine-readable review](research/candidate_review.json) covers all manufacturer directories. ATV940 and ATV990 remain unconfirmed exact-model requests.

Run `python scripts/build_distribution.py` after changes to manifest or packs, then `python scripts/build_distribution.py --check`. The build validates the live catalog and regenerates both distribution formats without bundling manufacturer PDFs.
