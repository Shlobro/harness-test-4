"""Projectile entities for bullets, pellets, and rockets."""

from __future__ import annotations

import math
from dataclasses import dataclass


Vector3 = tuple[float, float, float]


def _normalize(direction: Vector3) -> Vector3:
    length = math.sqrt(
        (direction[0] * direction[0])
        + (direction[1] * direction[1])
        + (direction[2] * direction[2])
    )
    if length <= 0.0:
        raise ValueError("Projectile direction must be non-zero.")
    return (
        direction[0] / length,
        direction[1] / length,
        direction[2] / length,
    )


@dataclass
class Projectile:
    """Simple projectile with position, velocity, and collision radius."""

    kind: str
    position: Vector3
    velocity: Vector3
    radius: float
    damage: float
    max_distance: float
    distance_traveled: float = 0.0
    is_active: bool = True

    @classmethod
    def from_payload(cls, payload: dict) -> "Projectile":
        direction = _normalize(payload["direction"])
        speed = payload["speed"]
        velocity = (
            direction[0] * speed,
            direction[1] * speed,
            direction[2] * speed,
        )
        return cls(
            kind=payload["kind"],
            position=payload["origin"],
            velocity=velocity,
            radius=payload["radius"],
            damage=payload["damage"],
            max_distance=payload.get("max_distance", 150.0),
        )

    def advance(self, delta_time: float) -> None:
        if not self.is_active or delta_time <= 0.0:
            return
        displacement = (
            self.velocity[0] * delta_time,
            self.velocity[1] * delta_time,
            self.velocity[2] * delta_time,
        )
        self.position = (
            self.position[0] + displacement[0],
            self.position[1] + displacement[1],
            self.position[2] + displacement[2],
        )
        self.distance_traveled += math.sqrt(
            (displacement[0] * displacement[0])
            + (displacement[1] * displacement[1])
            + (displacement[2] * displacement[2])
        )
        if self.distance_traveled >= self.max_distance:
            self.is_active = False
