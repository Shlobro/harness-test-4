"""Lighting blueprints for ambient and directional scene setup."""

from __future__ import annotations

from dataclasses import dataclass


Vector3 = tuple[float, float, float]
ColorRGB = tuple[int, int, int]


@dataclass(frozen=True)
class AmbientLight:
    """Low-frequency fill light that keeps shadows readable."""

    color: ColorRGB
    intensity: float


@dataclass(frozen=True)
class DirectionalLight:
    """Main directional key light for depth and shape definition."""

    direction: Vector3
    color: ColorRGB
    intensity: float


@dataclass(frozen=True)
class LightingRig:
    """Complete static lighting rig used in the arena scene."""

    ambient: AmbientLight
    directional: tuple[DirectionalLight, ...]


def create_basic_lighting_rig() -> LightingRig:
    """Build ambient + directional lights for the facility prototype."""
    return LightingRig(
        ambient=AmbientLight(color=(95, 106, 128), intensity=0.42),
        directional=(
            DirectionalLight(
                direction=(-0.42, -1.0, -0.18),
                color=(255, 242, 220),
                intensity=0.78,
            ),
            DirectionalLight(
                direction=(0.28, -0.7, 0.36),
                color=(140, 180, 255),
                intensity=0.3,
            ),
        ),
    )
