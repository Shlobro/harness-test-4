"""Base weapon model used by all weapon types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Weapon:
    """Shared weapon attributes and firing cooldown logic."""

    name: str
    damage: float
    fire_rate: float
    magazine_size: int
    reserve_ammo: int
    ammo_in_magazine: int | None = None
    _last_fired_at: float = -1_000_000.0

    def __post_init__(self) -> None:
        if self.ammo_in_magazine is None:
            self.ammo_in_magazine = self.magazine_size
        if self.fire_rate <= 0:
            raise ValueError(f"fire_rate must be positive, got {self.fire_rate}")

    @property
    def cooldown_seconds(self) -> float:
        return 1.0 / self.fire_rate

    def can_fire(self, now: float) -> bool:
        """Return True when weapon has ammo and cooldown is ready."""
        has_ammo = self.ammo_in_magazine > 0
        off_cooldown = (now - self._last_fired_at) >= self.cooldown_seconds
        return has_ammo and off_cooldown

    def fire(self, now: float) -> bool:
        """Spend one ammo and start cooldown. Returns True on successful shot."""
        if not self.can_fire(now):
            return False
        self.ammo_in_magazine -= 1
        self._last_fired_at = now
        return True

