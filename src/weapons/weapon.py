"""Base weapon model used by all weapon types."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


Vector3 = tuple[float, float, float]


def _normalize(direction: Vector3) -> Vector3:
    length = sqrt(
        (direction[0] * direction[0])
        + (direction[1] * direction[1])
        + (direction[2] * direction[2])
    )
    if length <= 0.0:
        raise ValueError("Direction vector must be non-zero.")
    return (
        direction[0] / length,
        direction[1] / length,
        direction[2] / length,
    )


@dataclass
class Weapon:
    """Shared weapon attributes and firing cooldown logic."""

    name: str
    damage: float
    fire_rate: float
    magazine_size: int
    reserve_ammo: int
    projectile_speed: float = 80.0
    projectile_radius: float = 0.08
    projectile_kind: str = "bullet"
    ammo_in_magazine: int | None = None
    _last_fired_at: float = -1_000_000.0

    def __post_init__(self) -> None:
        if self.ammo_in_magazine is None:
            self.ammo_in_magazine = self.magazine_size
        if self.fire_rate <= 0:
            raise ValueError(f"fire_rate must be positive, got {self.fire_rate}")
        if self.projectile_speed <= 0:
            raise ValueError(f"projectile_speed must be positive, got {self.projectile_speed}")

    @property
    def cooldown_seconds(self) -> float:
        return 1.0 / self.fire_rate

    @property
    def total_remaining_ammo(self) -> int:
        return self.reserve_ammo + self.ammo_in_magazine

    def is_magazine_full(self) -> bool:
        return self.ammo_in_magazine >= self.magazine_size

    def can_reload(self) -> bool:
        return (not self.is_magazine_full()) and self.reserve_ammo > 0

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

    def reload(self) -> int:
        """Move reserve ammo into magazine and return rounds loaded."""
        if not self.can_reload():
            return 0
        missing_rounds = self.magazine_size - self.ammo_in_magazine
        rounds_loaded = min(missing_rounds, self.reserve_ammo)
        self.ammo_in_magazine += rounds_loaded
        self.reserve_ammo -= rounds_loaded
        return rounds_loaded

    def create_projectile_payload(self, origin: Vector3, direction: Vector3) -> list[dict]:
        """Return projectile payload for a successful shot."""
        normalized = _normalize(direction)
        return [
            {
                "kind": self.projectile_kind,
                "origin": origin,
                "direction": normalized,
                "speed": self.projectile_speed,
                "radius": self.projectile_radius,
                "damage": self.damage,
            }
        ]
