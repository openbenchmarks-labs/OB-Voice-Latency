"""Turn a run's per-call measurements into its reported figures.

Pure: reads measured results, never audio, network or credentials.
"""

from __future__ import annotations

import numpy as np


def _percentiles(values: list[float], points=(50, 90, 95, 99)) -> dict:
    if not values:
        return {}
    arr = np.array(values, dtype=np.float64)
    return {f"p{p}": round(float(np.percentile(arr, p)), 1) for p in points}


def _turns_of(result) -> list:
    """Every turn of a call, including single-turn calls recorded before turns
    existed (their top-level fields are the one turn)."""
    turns = getattr(result, "turns", None)
    if turns:
        return turns
    return [result]


def build_report(results: list, vendor_name: str, run_id: str,
                 applied: dict) -> dict:
    """Turn per-call results into the reported figures.

    Latency figures are POOLED OVER TURNS, not over calls: a 4-turn call
    contributes four measurements. Discards are counted per turn too, because one
    bad turn should not waste the other three.
    """
    # A call-level discard invalidates the whole conversation; otherwise each turn
    # stands or falls on its own.
    all_turns = []
    for r in results:
        if r.discard_reason is not None:
            continue
        all_turns.extend(_turns_of(r))

    usable_turns = [t for t in all_turns if getattr(t, "usable", False)]
    onset = [t.ttfab_onset_ms for t in usable_turns if t.ttfab_onset_ms is not None]
    content = [t.ttfab_content_ms for t in usable_turns
               if t.ttfab_content_ms is not None]

    # TTFG is a property of the CALL (the greeting happens once), so it stays
    # call-scoped.
    usable_calls = [r for r in results if r.usable]
    ttfg = [r.ttfg_ms for r in usable_calls if r.ttfg_ms is not None]

    discards: dict[str, int] = {}
    for r in results:
        if r.discard_reason is not None:
            # Whole call lost: count it once, and note how many turns went with it.
            discards[r.discard_reason] = discards.get(r.discard_reason, 0) + 1
            continue
        for turn in _turns_of(r):
            if not getattr(turn, "usable", False):
                key = turn.discard_reason or "unknown"
                discards[key] = discards.get(key, 0) + 1

    turn_counts = sorted({getattr(t, "index", 1) or 1 for t in all_turns})
    per_turn = {}
    for index in turn_counts:
        at_index = [t for t in all_turns if (getattr(t, "index", 1) or 1) == index]
        good = [t for t in at_index if getattr(t, "usable", False)]
        values = [t.ttfab_onset_ms for t in good if t.ttfab_onset_ms is not None]
        per_turn[str(index)] = {
            "attempts": len(at_index),
            "usable": len(good),
            "n": len(values),
            **_percentiles(values, points=(50, 90, 95)),
        }

    report = {
        "run_id": run_id,
        "vendor": vendor_name,
        "attempts": len(results),
        "usable": len(usable_calls),
        "turns_per_call": max(turn_counts) if turn_counts else 1,
        "turn_attempts": len(all_turns),
        "turns_usable": len(usable_turns),
        "per_turn": per_turn,
        "discards": discards,
        "ttfab_onset_ms": _percentiles(onset),
        "ttfab_onset_n": len(onset),
        "ttfab_content_ms": _percentiles(content, points=(50, 95)),
        "ttfab_content_n": len(content),
        # Labelled at every point of use: this is measured from the start of the
        # recording, which is when our record_start took effect -- NOT carrier
        # answer.
        "ttfg_from_recording_start_ms": _percentiles(ttfg, points=(50, 95)),
        "negative_ttfab_count": sum(1 for v in onset if v < 0),
        "vendor_config_sha256": applied.get("sha256"),
        "vendor_defaults_used": applied.get("defaults_used"),
        "vendor_unsupported": applied.get("unsupported"),
    }

    if onset:
        p50 = float(np.percentile(onset, 50))
        p95 = float(np.percentile(onset, 95))
        report["consistency_p95_over_p50"] = round(p95 / p50, 3) if p50 else None
        report["beyond_2x_median_fraction"] = round(
            sum(1 for v in onset if v > 2 * p50) / len(onset), 3
        )

    # Does this vendor's TTS wait for the whole answer before
    # speaking? If so, longer replies start later and TTFAB correlates with
    # response duration. Reported, never corrected for.
    pairs = [(t.vendor_response_duration_ms, t.ttfab_onset_ms) for t in usable_turns
             if t.vendor_response_duration_ms and t.ttfab_onset_ms is not None]
    if len(pairs) >= 4:
        durations = np.array([p[0] for p in pairs], dtype=np.float64)
        onsets = np.array([p[1] for p in pairs], dtype=np.float64)
        if durations.std() > 0 and onsets.std() > 0:
            report["buffering_correlation_r"] = round(
                float(np.corrcoef(durations, onsets)[0, 1]), 3
            )
            report["buffering_n"] = len(pairs)

    return report
