# data

This folder holds the open dialog scenarios (`voice-bench/ttfab_scenarios.json`) and published board manifests (`latest-voice.json`, `manifest.json`). Raw audio recordings are never committed to git.

## Public vs. held-out evaluation sets

- **Open scenarios & manifests:** All 33 scripted turns, the agent prompt, and published summary manifests live directly in this folder.
- **Per-call runs:** Exported locally under `data/voice-runs/<run_id>/` (gitignored) via `python -m harness.export_snapshot`. Each call record references its recording URL and SHA-256 checksum.

## Files and schema

| Path | Description |
|---|---|
| `voice-bench/ttfab_scenarios.json` | Fictional Northwind Internet support prompt, 33 scripted caller questions, and required answer keywords. |
| `latest-voice.json` | Latest published run per voice platform: latency figures, cost, and applied setup. Account-specific agent ids and the vendor phone number are replaced with `<redacted>`. |
| `manifest.json` | Master index of the published board, runs, and recording links. Rebuild with `python -m judge.build_manifest` only after populating `data/voice-runs/` via `python -m harness.export_snapshot`. |

Before publishing new runs, inspect each run's `applied_config.json` for account-holder PII echoed by some platforms (for example, ElevenLabs returns `creator_name` and `creator_email`).
