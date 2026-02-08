"""Smooth weapon switching state machine."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WeaponSwitchState:
    """Tracks in-progress weapon transition timing."""

    switch_duration_seconds: float = 0.2
    source_weapon_name: str | None = None
    pending_weapon_name: str | None = None
    started_at: float | None = None

    def __post_init__(self) -> None:
        if self.switch_duration_seconds <= 0.0:
            raise ValueError("switch_duration_seconds must be positive.")

    @property
    def is_switching(self) -> bool:
        return self.pending_weapon_name is not None and self.started_at is not None

    def start_switch(self, current_weapon_name: str, next_weapon_name: str, now: float) -> bool:
        """Begin a new smooth switch. Returns False when no switch is needed."""
        if current_weapon_name == next_weapon_name:
            return False
        self.source_weapon_name = current_weapon_name
        self.pending_weapon_name = next_weapon_name
        self.started_at = now
        return True

    def progress(self, now: float) -> float:
        """Current normalized transition progress [0, 1]."""
        if not self.is_switching:
            return 1.0
        elapsed = max(0.0, now - self.started_at)
        return min(1.0, elapsed / self.switch_duration_seconds)

    def complete_if_ready(self, now: float) -> str | None:
        """Finalize switch when duration elapsed and return new weapon name."""
        if not self.is_switching:
            return None
        if self.progress(now) < 1.0:
            return None
        equipped = self.pending_weapon_name
        self.source_weapon_name = None
        self.pending_weapon_name = None
        self.started_at = None
        return equipped

