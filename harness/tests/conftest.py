"""Keeps the harness tests independent of a developer's .env."""

from __future__ import annotations

import os

import pytest

# The suite must be hermetic: no test may depend on a developer's .env. Set
# before any harness import so Settings never sees a missing base URL.
os.environ.setdefault("PUBLIC_BASE_URL", "https://bench.invalid")

# Settings loads .env directly, so clearing os.environ is not
# enough -- the fields have to be nulled on the instance. Anything here is a
# value that would otherwise make a test's verdict depend on whose laptop it
# ran on. TELNYX_VENDOR_NUMBER earned its place: with a real number in .env,
# the dial-target tests silently exercised that number instead of the mocked
# account, and passed or failed accordingly.
#
# ONE list, applied twice: once at import (before any adapter reads settings)
# and once per test (so a test that sets a value cannot leak into the next).
# Two hand-maintained lists drifted apart within a day of existing.
LEAKY_SETTINGS = (
    # Carrier.
    "plivo_from_number", "plivo_auth_id", "plivo_auth_token",
    # Which agent, and which number reaches it, per vendor. A real value here
    # makes a discovery test pass without discovering anything.
    "telnyx_vendor_number", "telnyx_assistant_id",
    "vapi_phone_number", "vapi_assistant_id",
    "retell_phone_number", "retell_agent_id",
    "bland_phone_number",
    "elevenlabs_phone_number", "elevenlabs_agent_id",
    # API keys. Every adapter mocks its transport, so these should never be
    # read -- but if a mock is ever incomplete, the failure must be the same on
    # every machine. With a key present an unmocked client makes a REAL request
    # against a live account; without one it raises VendorNotReady immediately.
    "telnyx_api_key", "vapi_api_key", "retell_api_key",
    "bland_api_key", "elevenlabs_api_key",
)

from harness.config import settings as _settings  # noqa: E402

for _leaky in LEAKY_SETTINGS:
    setattr(_settings, _leaky, None)


@pytest.fixture(autouse=True)
def _no_vendor_overrides_from_env(monkeypatch):
    """The per-test half of the hermeticity above.

    The import-time pass covers adapters that read settings at import; this
    covers anything a test mutates, and re-asserts the nulls for tests that run
    after one which set a value deliberately.
    """
    from harness.config import settings

    for field in LEAKY_SETTINGS:
        monkeypatch.setattr(settings, field, None, raising=False)
