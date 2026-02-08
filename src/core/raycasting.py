"""Raycasting primitives used for hit-scan shooting mechanics."""

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
        raise ValueError("Ray direction must be non-zero.")
    return (
        direction[0] / length,
        direction[1] / length,
        direction[2] / length,
    )


def _subtract(a: Vector3, b: Vector3) -> Vector3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a: Vector3, b: Vector3) -> float:
    return (a[0] * b[0]) + (a[1] * b[1]) + (a[2] * b[2])


@dataclass(frozen=True)
class RaycastTarget:
    """Sphere target used by hit-scan line traces."""

    target_id: str
    center: Vector3
    radius: float
    is_active: bool = True


@dataclass(frozen=True)
class RaycastHit:
    """Result of a successful line trace hit."""

    target_id: str
    distance: float
    hit_point: Vector3


@dataclass
class RaycastingSystem:
    """Performs nearest-hit raycasts against spherical targets."""

    def cast_ray(
        self,
        *,
        origin: Vector3,
        direction: Vector3,
        max_distance: float,
        targets: list[RaycastTarget],
    ) -> RaycastHit | None:
        if max_distance <= 0.0:
            raise ValueError("max_distance must be positive.")

        normalized_direction = _normalize(direction)
        nearest_distance = max_distance
        nearest_hit: RaycastHit | None = None

        for target in targets:
            if (not target.is_active) or target.radius <= 0.0:
                continue

            to_center = _subtract(target.center, origin)
            projection = _dot(to_center, normalized_direction)

            center_distance_sq = _dot(to_center, to_center)
            perpendicular_sq = center_distance_sq - (projection * projection)
            radius_sq = target.radius * target.radius
            if perpendicular_sq > radius_sq:
                continue

            half_chord = sqrt(radius_sq - perpendicular_sq)
            near_distance = projection - half_chord
            if near_distance < 0.0:
                near_distance = projection + half_chord
            if near_distance < 0.0 or near_distance > nearest_distance:
                continue

            nearest_distance = near_distance
            nearest_hit = RaycastHit(
                target_id=target.target_id,
                distance=near_distance,
                hit_point=(
                    origin[0] + (normalized_direction[0] * near_distance),
                    origin[1] + (normalized_direction[1] * near_distance),
                    origin[2] + (normalized_direction[2] * near_distance),
                ),
            )

        return nearest_hit
