"""Timeline helper for the synthetic process-triage exercise."""

from __future__ import annotations

import argparse
import base64
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = ROOT / "challenges" / "log_triage" / "auth.jsonl"
REQUIRED_FIELDS = {"event_id", "timestamp", "host", "user", "action", "detail"}


def read_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_number}: invalid JSON") from exc
        if not isinstance(event, dict) or not REQUIRED_FIELDS.issubset(event):
            missing = sorted(REQUIRED_FIELDS - set(event)) if isinstance(event, dict) else sorted(REQUIRED_FIELDS)
            raise ValueError(f"line {line_number}: missing required fields {missing}")
        try:
            datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
        except (AttributeError, TypeError, ValueError) as exc:
            raise ValueError(f"line {line_number}: invalid timestamp") from exc
        events.append(event)
    return sorted(events, key=lambda event: event["timestamp"])


def summarize(events: Iterable[dict[str, Any]]) -> dict[str, Any]:
    ordered = list(events)
    encoded_notes = [event["encoded_note"] for event in ordered if "encoded_note" in event]
    decoded_notes: list[str] = []
    for encoded in encoded_notes:
        try:
            decoded_notes.append(base64.b64decode(encoded, validate=True).decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise ValueError("invalid encoded_note in event data") from exc
    return {
        "event_ids": [event["event_id"] for event in ordered],
        "actions": [event["action"] for event in ordered],
        "decoded_notes": decoded_notes,
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", nargs="?", type=Path, default=DEFAULT_LOG)
    args = parser.parse_args(argv)
    print(json.dumps(summarize(read_events(args.log)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
