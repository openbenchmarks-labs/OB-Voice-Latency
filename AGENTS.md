# AGENTS.md — OB-Voice-Latency

Quick navigation guide for coding agents working in `OB-Voice-Latency`.

## Structure (Zero Overlap)

| Folder | Owns | Files |
|---|---|---|
| **`data/`** | The caller's questions, the agent prompt, and published results | `data/README.md`, `data/voice-bench/ttfab_scenarios.json`, `data/latest-voice.json`, `data/manifest.json` |
| **`harness/`** | Execution only: caller script, call runner, carrier, platform adapters, setup scripts, cost lookup, HTML report, export | `harness/dialog.yaml`, `harness/bench.py`, `harness/sync_bench.py`, `harness/dialog.py`, `harness/carriers/`, `harness/adapters/`, `harness/provision/`, ... |
| **`tools/`** | Tool setups (one file per tool for clean PRs) | `tools/<tool>.yaml` (5 tools) |
| **`judge/`** | Grading only: reply timing from audio, run figures, board, re-checks | `judge/measure.py`, `judge/onset.py`, `judge/summary.py`, `judge/build_manifest.py`, `judge/verify_run.py`, `judge/fixtures/` |

Benchmark order & win condition live at the root in `benchmark.yaml`.

## Commands

```sh
# Offline tests and the judge's accuracy check (no API keys)
uv venv && uv pip install -r requirements.txt
.venv/bin/pytest
.venv/bin/python -m judge --gate-a

# Live run against one tool (needs .env)
.venv/bin/python -m harness.bench --vendor telnyx --calls 10
```

## Guidelines

- **Keep folders strictly separated:** Questions and results in `data/`; calls and platform APIs in `harness/`; per-tool setups in `tools/<tool>.yaml`; timing and the board in `judge/`.
- **Adding or tuning a tool:** Edit `tools/<tool>.yaml` (and `harness/adapters/<tool>.py` for a new platform), then run `pytest`.
- **Adapters are read-only:** They check a platform's live agent and never change it. Only `harness/provision/` writes to a platform account, and only when a person runs it.
- **No secrets or raw recordings in git:** Keep API keys in `.env` and run output in `runs/` (both gitignored).
- **Consistent terminology:** Use `tool`, `setup`, `question`, `ground truth`, `judge`, `board`, `TTFAB` (time to first audio byte: from the end of the caller's question to the start of the agent's reply).
