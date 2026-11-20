"""Shared fixture building.

Fixtures are assembled once per test session into a tmp dir rather than committed
as WAVs: the inputs (speech clips in judge/fixtures/sources/) are committed, and
assembly is deterministic, so this keeps the repo small without giving up
reproducibility.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from judge.fixtures import build_all


@pytest.fixture(scope="session")
def fixture_dir(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("fixtures")
    build_all(out)
    return out


@pytest.fixture(scope="session")
def truths(fixture_dir) -> dict[str, dict]:
    import json

    return {
        p.stem.replace(".truth", ""): json.loads(p.read_text())
        for p in fixture_dir.glob("*.truth.json")
    }


def load_fixture(fixture_dir: Path, truth: dict):
    """Return (near, far, reference, rate) for a fixture."""
    audio, rate = sf.read(fixture_dir / truth["wav"], dtype="int16")
    ref, ref_rate = sf.read(fixture_dir / truth["reference_wav"], dtype="int16")
    assert ref_rate == rate
    near = audio[:, truth["channels"]["near"]]
    far = audio[:, truth["channels"]["far"]]
    return np.ascontiguousarray(near), np.ascontiguousarray(far), ref, rate
