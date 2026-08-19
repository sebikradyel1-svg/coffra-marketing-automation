"""
Rate limiter + retry wrapper for Anthropic API calls (P7 pipeline).

Wraps client.messages.create() with:
- A rolling-window throttle (max N calls per WINDOW_SECONDS) so the
  pipeline doesn't burst past your Anthropic rate limit when qualification,
  outreach, and governance fire in quick succession.
- Exponential backoff + retry specifically on 429 / rate-limit errors.
  Any other API error (bad request, auth, etc.) is re-raised immediately -
  retrying those would just waste time and hide real bugs.

Thread-safe within a single Streamlit process (module-level state guarded
by a lock). This is a single-process limiter, not a distributed one - fine
for a demo/portfolio app running on one Streamlit Cloud instance.

Usage (drop-in replacement for client.messages.create(**kwargs)):

    from utils.rate_limiter import call_claude

    client = Anthropic()
    response = call_claude(
        client,
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
"""

from __future__ import annotations

import threading
import time
from collections import deque
from typing import Any

import anthropic
from anthropic import Anthropic

# Tune these to your actual Anthropic tier / usage pattern.
MAX_CALLS_PER_WINDOW = 60
WINDOW_SECONDS = 60.0
MAX_RETRIES = 4
BASE_BACKOFF_SECONDS = 2.0

_call_times: deque[float] = deque()
_lock = threading.Lock()


def _throttle() -> None:
    """Block until there's room in the rolling window for one more call."""
    with _lock:
        now = time.monotonic()
        while _call_times and now - _call_times[0] > WINDOW_SECONDS:
            _call_times.popleft()

        if len(_call_times) >= MAX_CALLS_PER_WINDOW:
            wait = WINDOW_SECONDS - (now - _call_times[0])
            if wait > 0:
                time.sleep(wait)
            now = time.monotonic()
            while _call_times and now - _call_times[0] > WINDOW_SECONDS:
                _call_times.popleft()

        _call_times.append(time.monotonic())


def call_claude(client: Anthropic, **kwargs: Any):
    """
    Rate-limited, retrying drop-in for client.messages.create(**kwargs).

    Raises RuntimeError if the call still fails after MAX_RETRIES retries
    due to rate limiting. Any non-rate-limit API error is raised immediately,
    unchanged, on the first attempt.
    """
    last_error: Exception | None = None

    for attempt in range(MAX_RETRIES + 1):
        _throttle()
        try:
            return client.messages.create(**kwargs)
        except anthropic.RateLimitError as e:
            last_error = e
        except anthropic.APIStatusError as e:
            if e.status_code != 429:
                raise
            last_error = e
        else:
            continue

        backoff = BASE_BACKOFF_SECONDS * (2**attempt)
        time.sleep(backoff)

    raise RuntimeError(
        f"Claude API call failed after {MAX_RETRIES} retries due to rate limiting."
    ) from last_error
