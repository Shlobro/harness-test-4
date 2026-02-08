"""Lightweight game clock and delta-time tracking."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GameClock:
    """Tracks elapsed and per-frame timing."""

    elapsed_time: float = 0.0
    frame_count: int = 0
    _last_timestamp: float | None = None

    def tick(self, now: float) -> float:
        """Advance the clock and return frame delta-time in seconds."""
        if self._last_timestamp is None:
            self._last_timestamp = now
            return 0.0

        delta_time = max(0.0, now - self._last_timestamp)
        self._last_timestamp = now
        self.elapsed_time += delta_time
        self.frame_count += 1
        return delta_time

