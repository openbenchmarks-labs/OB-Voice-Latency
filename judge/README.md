# judge

Times every reply from the saved call recording and builds the board. No calling or platform code lives here, and nothing here needs a key.

- `measure.py` — Turns one call recording into its result: when each question ended, when each reply started, and whether the turn is usable.
- `onset.py` — Finds where speech starts and stops, using the Silero speech detector.
- `correlate.py` — Finds a known sound inside a recording; used to check the judge against fixtures with known answers.
- `codec.py` — Phone-line audio encoding, so test audio sounds like a real call.
- `resample.py` — Converts audio between sample rates.
- `summary.py` — Pools every usable turn of a run into its median and tail latency and its discard counts.
- `build_manifest.py` — Ranks the tools by median reply time and writes `data/manifest.json`.
- `verify_run.py` — Downloads a published run's recordings and re-times them, so anyone can check our numbers.
- `blind_test.py` — Hides a delay in a fake call and checks the judge finds it.
- `__main__.py` — `python -m judge`: times a saved run, or runs Gate A (the accuracy check against fixtures).
- `models/silero_vad.onnx` — The speech detector model.
- `fixtures/` — Builds fake calls with known reply times from short speech clips, for Gate A and the tests.
- `tests/` — Offline tests for everything above.
