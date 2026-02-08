"""Assault rifle weapon implementation."""

from __future__ import annotations

from src.weapons.weapon import Weapon


class AssaultRifle(Weapon):
    """Rapid-fire automatic weapon for mid-range combat."""

    def __init__(self) -> None:
        super().__init__(
            name="AssaultRifle",
            damage=16.0,
            fire_rate=9.0,
            magazine_size=30,
            reserve_ammo=120,
            projectile_speed=95.0,
            projectile_radius=0.07,
            projectile_kind="bullet",
        )
