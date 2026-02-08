"""Lightweight game clock and time-management controls."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GameClock:
    """Tracks elapsed time, pause state, and time scaling."""

    elapsed_time: float = 0.0
    unscaled_elapsed_time: float = 0.0
    frame_count: int = 0
    is_paused: bool = False
    time_scale: float = 1.0
    _last_timestamp: float | None = None

    def tick(self, now: float) -> float:
        """Advance the clock and return scaled frame delta-time in seconds."""
        if self._last_timestamp is None:
            self._last_timestamp = now
            return 0.0

        unscaled_delta = max(0.0, now - self._last_timestamp)
        self._last_timestamp = now
        self.unscaled_elapsed_time += unscaled_delta
        if self.is_paused:
            return 0.0

        delta_time = unscaled_delta * self.time_scale
        self.elapsed_time += delta_time
        if delta_time > 0.0:
            self.frame_count += 1
        return delta_time

    def set_paused(self, paused: bool) -> None:
        """Pause or resume scaled time progression."""
        self.is_paused = paused

    def set_time_scale(self, scale: float) -> None:
        """Configure non-zero positive scale applied to frame delta."""
        if scale <= 0.0:
            raise ValueError("time scale must be positive.")
        self.time_scale = scale

    def reset(self, timestamp: float | None = None) -> None:
        """Reset elapsed counters and optionally set a new last timestamp."""
        self.elapsed_time = 0.0
        self.unscaled_elapsed_time = 0.0
        self.frame_count = 0
        self._last_timestamp = timestamp
