"""Optional JSON Lines event history for Personal PC 2 monitoring."""

import json
import time
from pathlib import Path
from typing import Any, Mapping


class JsonlEventHistory:
    """Append monitoring events to a user-selected JSON Lines file."""

    def __init__(self, path: str | Path) -> None:
        if not str(path).strip():
            raise ValueError("path must not be empty")
        self.path = Path(path)

    def append(
        self,
        *,
        event_type: str,
        simulation_time_ns: int,
        payload: Mapping[str, Any],
        received_wall_time_ns: int | None = None,
    ) -> dict[str, Any]:
        """Append one event and return the exact serialized record."""

        if not event_type.strip():
            raise ValueError("event_type must not be empty")
        if simulation_time_ns < 0:
            raise ValueError("simulation_time_ns must not be negative")
        if received_wall_time_ns is not None and received_wall_time_ns < 0:
            raise ValueError("received_wall_time_ns must not be negative")

        record = {
            "event_type": event_type,
            "simulation_time_ns": simulation_time_ns,
            "received_wall_time_ns": (
                time.time_ns()
                if received_wall_time_ns is None
                else received_wall_time_ns
            ),
            "payload": dict(payload),
        }
        encoded = json.dumps(record, ensure_ascii=False, sort_keys=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(encoded)
            stream.write("\n")
        return record
