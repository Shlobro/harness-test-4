"""Pistol weapon implementation."""

from __future__ import annotations

from src.weapons.weapon import Weapon


class Pistol(Weapon):
    """Default starter weapon with reliable semi-auto fire."""

    def __init__(self) -> None:
        super().__init__(
            name="Pistol",
            damage=20.0,
            fire_rate=3.0,
            magazine_size=12,
            reserve_ammo=48,
        )

