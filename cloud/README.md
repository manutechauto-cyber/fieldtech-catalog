# FieldTech Industrial — downloadable cloud database

The published release is a read-only SQLite snapshot served by GitHub raw HTTPS. It contains every published drive payload, the sensor taxonomy and research candidates. It is not a running Supabase/PostgreSQL service, and does not imply any change to the app's database.

## Stable endpoints

- [Release and checksums](https://raw.githubusercontent.com/manutechauto-cyber/fieldtech-catalog/main/cloud/release.json)
- [Search index](https://raw.githubusercontent.com/manutechauto-cyber/fieldtech-catalog/main/cloud/index.json)
- [Base64 ZIP database](https://raw.githubusercontent.com/manutechauto-cyber/fieldtech-catalog/main/cloud/industrial_database.b64)

Fetch release, bundle and release again. Retry if release changed between reads. Decode base64; verify SHA-256 of ZIP bytes against `bundle.sha256`; extract `fieldtech-industrial.sqlite`; verify `database.sha256`. Open SQLite read-only and check `PRAGMA user_version = 1` and `PRAGMA integrity_check = ok`. Replace the previous local snapshot atomically only after these checks. Keep the last valid snapshot for offline use. `index.json` is for discovery, not an authoritative import when checksums fail.

Version compatibility is `databaseSchemaVersion`; content changes are identified by database SHA-256. `drivesCatalogVersion` only versions drives, and does not identify changes in sensor research. Counts explicitly separate published devices and candidates. Research candidates must never appear as verified device packs in the app.

## Tables

| Table | Contents |
| --- | --- |
| metadata | Schema version, drive catalog version, sensor manifest and scope |
| device_packs | Published canonical ID, category, manufacturer, model, version, source path and full payload JSON |
| sensor_types | Type, priority, target and classification payload |
| sensor_candidates | Exact-model research leads and review status; not published devices |

Drive payloads retain their original verification flags, including legacy basic subsets. Database publication does not upgrade the evidence quality of a pack. Sensor catalog version 1 includes 127 published field subsets from 32 official PDFs. O5D100 is now published from its official operating instructions and datasheet. The 20-model-per-type target remains incomplete. No sales ranking or hardware validation is asserted.

## Incremental updates

Edit source packs/manifests, then run:

```sh
python scripts/validate_catalog.py
python scripts/validate_sensor_structure.py
python scripts/build_distribution.py
python scripts/build_sensor_distribution.py
python scripts/build_cloud_database.py
python -m unittest discover -s tests -v
```

Commit source and generated artifacts together. CI rejects stale distributions and SQLite snapshots. The builder uses only Python stdlib, creates a new database instead of migrating an existing user's data, and generates repeatable outputs within the same SQLite runtime. CI compares table contents and schema across SQLite versions while checking the published artifact hashes. No credentials are needed to consume this public catalog.

Sensor publication uses a dedicated provenance validator and sensor ZIP distribution; verified packs are serialized into the same SQLite device_packs table. The sensor document registry is available in metadata for offline lookup. App import, UI integration and any live Supabase migration remain separate tasks requiring the corresponding project access. This database can already be downloaded and queried without those services.
