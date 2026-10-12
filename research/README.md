# Candidate research and publication review

Reviewed 2026-10-12. Manufacturer presence is used as a prioritization proxy; this is **not a verified ranking of worldwide model sales**. This scan covers the major global supplier landscape and every existing manufacturer directory. It cannot certify that every model in the world has been researched.

## Published field subsets

| Family | Parameters | Faults / warnings | Pack |
| --- | ---: | ---: | --- |
| Altivar Process ATV930 | 14 | 10 | [schneider/atv930.json](../schneider/atv930.json) |
| Altivar Process ATV950 | 14 | 10 | [schneider/atv950.json](../schneider/atv950.json) |
| Altivar Process ATV630 | 14 | 10 | [schneider/atv630.json](../schneider/atv630.json) |
| Altivar Process ATV650 | 14 | 10 | [schneider/atv650.json](../schneider/atv650.json) |
| Altivar ATV12 | 12 | 11 | [schneider/atv12.json](../schneider/atv12.json) |
| PowerFlex 523 | 14 | 13 | [rockwell/pf523.json](../rockwell/pf523.json) |
| PowerFlex 525 | 14 | 15 | [rockwell/pf525.json](../rockwell/pf525.json) |
| ACS480 | 13 | 5 | [abb/acs480.json](../abb/acs480.json) |
| ACS380 | 13 | 5 | [abb/acs380.json](../abb/acs380.json) |
| ACH580 | 13 | 5 | [abb/ach580.json](../abb/ach580.json) |
| ACQ580 | 13 | 5 | [abb/acq580.json](../abb/acq580.json) |
| ACS550 | 12 | 10 | [abb/acs550.json](../abb/acs550.json) |
| VLT HVAC Drive FC 102 | 9 | 9 | [danfoss/fc102.json](../danfoss/fc102.json) |
| VLT Aqua Drive FC 202 | 9 | 9 | [danfoss/fc202.json](../danfoss/fc202.json) |
| CFW300 | 9 | 6 | [weg/cfw300.json](../weg/cfw300.json) |
| CFW-11 | 9 | 6 | [weg/cfw11.json](../weg/cfw11.json) |
| Goodrive20 | 10 | 13 | [invt/gd20.json](../invt/gd20.json) |
| Goodrive200A | 10 | 13 | [invt/gd200a.json](../invt/gd200a.json) |
| SINAMICS V20 | 11 | 6 | [siemens/v20.json](../siemens/v20.json) |
| MOVITRAC B | 7 | 7 | [sew/movitrac_b.json](../sew/movitrac_b.json) |
| SV-iC5 | 9 | 6 | [ls/ic5.json](../ls/ic5.json) |
| PowerXL DE1 | 8 | 6 | [eaton/de1.json](../eaton/de1.json) |
| Unidrive M200/M201 | 12 | 7 | [control_techniques/unidrive_m200.json](../control_techniques/unidrive_m200.json) |
| FREQROL FR-E700 | 9 | 9 | [mitsubishi/fr_e700.json](../mitsubishi/fr_e700.json) |
| U1000 Matrix Drive | 9 | 6 | [yaskawa/u1000.json](../yaskawa/u1000.json) |
| PowerFlex 40 | 10 | 12 | [rockwell/pf40.json](../rockwell/pf40.json) |
| TOSVERT VF-nC3 | 10 | 9 | [toshiba/vf_nc3.json](../toshiba/vf_nc3.json) |
| SYSDRIVE JX | 7 | 8 | [omron/jx.json](../omron/jx.json) |
| SJ-P1 | 11 | 5 | [hitachi/sj_p1.json](../hitachi/sj_p1.json) |
| J1000 | 8 | 8 | [yaskawa/j1000.json](../yaskawa/j1000.json) |
| Optidrive CoolVert | 8 | 7 | [invertek/optidrive_coolvert.json](../invertek/optidrive_coolvert.json) |
| FRENIC-Lift LM1S | 7 | 11 | [fuji/frenic_lift_lm1s.json](../fuji/frenic_lift_lm1s.json) |

## Additional researched candidates

| Family | Review status | Evidence / remaining requirement |
| --- | --- | --- |
| VFD-EL / VFD-EL-W | pending-manual-content | [Official source](https://www.deltaww.com/en-US/products/AC-Motor-Drives/113). Official product family confirmed; filecenter manual URL returned HTML instead of PDF. No codes imported from distributors. |
| NORDAC FLEX SK 200E | pending-manual-content | [Official source](https://www.nord.com/us/services/documentation/manuals/details/bu0200.jsp). Official BU0200 manual listing confirmed; indexed direct PDF returned 404 and direct listing retrieval returned 403. |
| COMBIVERT G6 | pending-control-manual | [Official source](https://www.keb-automation.com/en-it/products/drive-technology/proven-technology/frequency-inverter-combivert-g6). Product confirmed; retained IO-Link control manual describes the communication interface, not motor parameters and trips; core drive manual still needed. |
| AC30 | pending-control-manual | [Official source](https://www.parker.com/content/dam/Parker-com/Literature/empd---electric-motion-and-pneumatic-division-europe/user-guides/em/ac30/HA503711U002-KR%20AC30%20Hardware_K-N.pdf). Hardware document identifies HA501718 control/product manual; parameter/fault content not verified. |
| IndraDrive | deferred-variant-specific | [Official source](https://www.boschrexroth.com/en/US/c/drive-integrated-connectivity/). Servo family confirmed; requires exact controller and firmware selection before parameter enrichment. |
| i950 | deferred-variant-specific | [Official source](https://www.lenze.com/en-us/distributor-webinars). Servo platform confirmed; existing i510/i550 cover general-purpose inverter families. Application/firmware needed. |
| SmartVFD HVAC / HVAC2 | pending-control-manual | [Official source](https://buildings.honeywell.com/pl/en/products/by-category/building-management/field-devices/variable-frequency-drives/smartvfd-hvac2-variable-frequency-drive). Product confirmed; engineering specification alone is insufficient to populate codes. |
| FRENIC-Lift LM2/LM3 | deferred-specialized | [Official source](https://www.fujielectric.com/products/drives_inverters/ac_drives_lv/product_series/frenic-lift.html). LM1S field subset published; LM2/LM3 require separate generation-specific manuals and lift-specific review. |
| Active / Active Next | pending-generation-review | [Official source](https://www.bonfiglioli.com/uk/en/product/active-series_inverters-servo-drives_premium-inverters). Official family confirmed. Active, Active Cube and Active Next are separate generations; no code reuse without exact manual. |

ATV940 and ATV990 remain unconfirmed exact-model queries. ATV930 and ATV950 are independent verified families and must not be used as silent aliases.

## Evidence and limits

- [Manual registry](manual_sources.json) records document revisions and PDF hashes where downloads succeeded. J1000 was reviewed from official PDF web extraction.
- Each published item references its manual and PDF page. LS, Omron, CoolVert and FRENIC-Lift display codes were visually checked because PDF fonts/images prevented reliable text extraction.
- Code/page references from downloaded PDFs passed an independent text check before publication. This check verifies references, not electrical commissioning of hardware.
- New diagnostic summaries are short field checks, not full troubleshooting procedures. Default values and ranges are supplied only where reviewed; no global defaults are assumed for motor/drive ratings.
- New content is English/Portuguese. Previously available translations are retained on enriched existing codes; six-language completeness is not claimed.
- Older manuals are explicitly identified for installed-fleet support. Verify exact hardware, firmware and control program when using them.
