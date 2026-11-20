# harness

Places the calls, records them, and talks to each platform's API. No timing or scoring lives here; every reported number comes from `judge/`.

- `dialog.yaml` — The caller's voice, how long it waits for each reply, and which questions it asks.
- `bench.py` — Runs one tool: checks its live agent matches `tools/<tool>.yaml`, places the calls, and saves the report.
- `sync_bench.py` — Runs all tools side by side, one call to each per round, so they share the same hour.
- `onecall.py` — Places one call and measures it; shared by the side-by-side run.
- `dialog.py` — The scripted caller: reads the questions out, waits for each answer, and fetches the recording.
- `answerxml.py` — Builds the carrier's call-control XML.
- `serving.py` — Sets the address and TLS for the local web server the carrier calls back, and checks them before a run.
- `signature.py` — Checks that incoming carrier callbacks are genuine.
- `config.py` — Reads settings and keys from `.env`.
- `instrument.py` — What is known, and not yet known, about the measuring setup's own delay.
- `costs.py` — Matches each call to the platform's billing record and works out the price per minute.
- `backfill_costs.py` — Fetches costs for saved runs later, once billing has caught up.
- `html_report.py` — Draws a run as a single HTML page.
- `rebuild_report.py` — Redraws that page from a saved run.
- `reanalyze_run.py` — Re-times a saved run after a judge change and shows what moved.
- `export_snapshot.py` — Copies a finished run into `data/` for publishing.
- `probe_dialog.py` — One test call that checks how the carrier records and steers a call before real runs rely on it.
- `main.py` — A small health-check server and log setup.
- `venv_check.py` — Stops a script early with a clear message when run with the wrong Python.
- `carriers/` — The phone carrier that places every call (Plivo only, so no platform is measured over its own network).
- `adapters/` — One file per platform that reads its live agent, its phone number, and its billing. Read-only. `registry.py` is the one place that lists them.
- `provision/` — One setup script per platform that creates or fixes the agent under test. Run by hand, never by the bench.
- `tests/` — Offline tests for everything above.
