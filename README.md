# OB-Voice-Latency

Open, independent voice agent latency benchmark: how long a caller waits before a voice AI agent starts speaking on real PSTN phone calls, measured as time to first audio byte (TTFAB) in milliseconds. Every platform runs the same agent prompt and faces the same scripted caller over the same phone carrier, and an offline audio analyzer times every reply from the call recording, never from platform-reported timestamps. Platforms measured: Telnyx, Retell, Vapi, ElevenLabs and Bland.

**Live leaderboard:** [openbenchmarks.com/voice-agent-latency](https://openbenchmarks.com/voice-agent-latency)

Published and maintained by **[OpenBenchmarks Labs](https://openbenchmarks.com)**.

## Methodology

The benchmark measures **TTFAB (Time To First Audio Byte)**: the gap between the end of the caller's speech (`t1`) and the start of the agent's reply (`t2`), on real phone calls across 33 scripted customer-support turns.

- **Fixed protocol:** Every voice platform runs the identical fictional Northwind Internet support prompt (`data/voice-bench/ttfab_scenarios.json`) against the same scripted caller (`harness/dialog.yaml`) over the same carrier.
- **Offline audio measurement:** `judge/measure.py` and `judge/onset.py` detect speech boundaries directly from the saved call recordings using Silero VAD, producing median and tail latency, turn usability, and cost with no vendor self-reporting.

## Tools evaluated

5 voice-agent platforms configured in [`tools/`](tools/README.md):

`bland`, `elevenlabs`, `retell`, `telnyx`, `vapi`

## Dataset

All benchmark scenarios and published manifest snapshots are open in [`data/`](data/README.md):

- `data/voice-bench/ttfab_scenarios.json`: Support agent prompt, 33 scripted caller questions, and required answer keywords.
- `data/latest-voice.json` and `data/manifest.json`: Published latency summaries and run index (raw audio recordings are linked by URL and checksum, never committed to git).

See [`data/README.md`](data/README.md) for export and manifest rebuild instructions.

## Repository structure

- [`data/`](data/README.md): Caller scenarios, support prompt, and published latency manifests.
- [`harness/`](harness/README.md): PSTN call runner (`harness/bench.py`, `harness/sync_bench.py`), dialog spec, and platform adapters.
- [`tools/`](tools/README.md): One `<tool>.yaml` config per voice platform (5 tools).
- [`judge/`](judge/README.md): Offline audio analyzer (`measure.py`, `onset.py`, Silero VAD) and manifest builder.
- [`benchmark.yaml`](benchmark.yaml): Benchmark contract, scope, and refresh cadence.
- [`AGENTS.md`](AGENTS.md): Entry guide for coding agents.

## Quick start

Run the offline tests and audio gate check (no API keys or phone calls required):

```sh
uv venv && uv pip install -r requirements.txt
.venv/bin/pytest
.venv/bin/python -m judge --gate-a
```

To place live calls, copy `.env.example` to `.env`, add your carrier and platform keys, and inspect the runner:

```sh
cp .env.example .env
.venv/bin/python -m harness.bench --help
```

## Adding or updating a tool

1. Add or edit `tools/<tool>.yaml` (and add `harness/adapters/<tool>.py` plus one line in `harness/adapters/registry.py` if adding a new platform).
2. Run `.venv/bin/pytest` and `.venv/bin/python -m judge --gate-a`.
3. Open a pull request.

## Links

- [Live leaderboard](https://openbenchmarks.com/voice-agent-latency) and [how latency is measured](https://openbenchmarks.com/voice-agent-latency/how-voice-agent-latency-is-measured)
- [JSON API](https://openbenchmarks.com/api/benchmarks/voice-agent-latency)
- [`llms.txt`](https://openbenchmarks.com/llms.txt)

## Related benchmarks

- [OB-Inference-Microtasks](https://github.com/openbenchmarks-labs/OB-Inference-Microtasks): Serverless LLM inference latency and accuracy ([leaderboard](https://openbenchmarks.com/inference))
- [OB-LegalQA-Document-Parsing](https://github.com/openbenchmarks-labs/OB-LegalQA-Document-Parsing): Document parsers on redlined legal contracts ([leaderboard](https://openbenchmarks.com/document-processing))
- [OB-Code-WebSearch](https://github.com/openbenchmarks-labs/OB-Code-WebSearch): Web search APIs for coding agents ([leaderboard](https://openbenchmarks.com/web-search-for-coding-agents))
- [All OpenBenchmarks leaderboards](https://openbenchmarks.com)

## License

MIT. See [LICENSE](LICENSE).
