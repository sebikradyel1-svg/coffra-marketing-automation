"""Append pipeline decisions to a local JSONL log for audit/debugging."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "decisions.jsonl"


def log_decision(step: str, input_data: Any, output_data: Any) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "step": step,
        "input": input_data,
        "output": output_data,
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
