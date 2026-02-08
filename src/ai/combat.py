"""Combat helpers for bot aiming and shot variance."""

from __future__ import annotations

from math import radians, sqrt, tan
from random import Random


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


def _cross(a: Vector3, b: Vector3) -> Vector3:
    return (
        (a[1] * b[2]) - (a[2] * b[1]),
        (a[2] * b[0]) - (a[0] * b[2]),
        (a[0] * b[1]) - (a[1] * b[0]),
    )


def vary_direction_with_accuracy(
    *,
    direction: Vector3,
    accuracy_degrees: float,
    rng: Random,
) -> Vector3:
    """Return a normalized direction perturbed by an accuracy cone."""
    if accuracy_degrees < 0.0:
        raise ValueError("accuracy_degrees must be non-negative.")

    forward = _normalize(direction)
    max_offset = tan(radians(accuracy_degrees))
    if max_offset == 0.0:
        return forward

    up_axis = (0.0, 1.0, 0.0)
    right = _cross(forward, up_axis)
    right_length_sq = (right[0] * right[0]) + (right[1] * right[1]) + (right[2] * right[2])
    if right_length_sq < 1e-9:
        up_axis = (1.0, 0.0, 0.0)
        right = _cross(forward, up_axis)
    right = _normalize(right)
    up = _normalize(_cross(right, forward))

    offset_x = rng.uniform(-max_offset, max_offset)
    offset_y = rng.uniform(-max_offset, max_offset)
    varied = (
        forward[0] + (right[0] * offset_x) + (up[0] * offset_y),
        forward[1] + (right[1] * offset_x) + (up[1] * offset_y),
        forward[2] + (right[2] * offset_x) + (up[2] * offset_y),
    )
    return _normalize(varied)
