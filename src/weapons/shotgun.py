"""Shotgun weapon implementation."""

from __future__ import annotations

import math

from src.weapons.weapon import Weapon


class Shotgun(Weapon):
    """High-damage close-range weapon with pellet spread."""

    def __init__(self) -> None:
        super().__init__(
            name="Shotgun",
            damage=12.0,
            fire_rate=1.0,
            magazine_size=8,
            reserve_ammo=32,
            projectile_speed=70.0,
            projectile_radius=0.1,
            projectile_kind="pellet",
        )
        self.pellet_count = 8
        self.spread_degrees = 6.0

    def create_projectile_payload(
        self,
        origin: tuple[float, float, float],
        direction: tuple[float, float, float],
    ) -> list[dict]:
        base = super().create_projectile_payload(origin=origin, direction=direction)[0]
        spread_rad = math.radians(self.spread_degrees)
        payload: list[dict] = []
        for index in range(self.pellet_count):
            # Deterministic circular distribution keeps tests stable.
            ratio = 0.0 if self.pellet_count == 1 else (index / (self.pellet_count - 1)) - 0.5
            yaw_offset = ratio * spread_rad
            direction_x = base["direction"][0] + yaw_offset
            direction_y = base["direction"][1]
            direction_z = base["direction"][2] - abs(yaw_offset) * 0.15
            payload.append(
                {
                    **base,
                    "direction": (direction_x, direction_y, direction_z),
                }
            )
        return payload
