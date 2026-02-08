"""Weapon visual definitions built from geometric primitives."""

from __future__ import annotations

from dataclasses import dataclass


Vector3 = tuple[float, float, float]
ColorRGB = tuple[int, int, int]


@dataclass(frozen=True)
class PrimitiveVisual:
    """Single geometric primitive used by a weapon model."""

    shape: str
    size: Vector3
    offset: Vector3
    color: ColorRGB


@dataclass(frozen=True)
class WeaponVisual:
    """Renderable visual recipe for a weapon."""

    weapon_name: str
    primitives: tuple[PrimitiveVisual, ...]


WEAPON_VISUALS: dict[str, WeaponVisual] = {
    "Pistol": WeaponVisual(
        weapon_name="Pistol",
        primitives=(
            PrimitiveVisual("box", (0.35, 0.12, 0.6), (0.0, -0.08, 0.0), (35, 35, 35)),
            PrimitiveVisual("box", (0.2, 0.22, 0.2), (0.0, -0.24, -0.1), (60, 60, 60)),
        ),
    ),
    "Shotgun": WeaponVisual(
        weapon_name="Shotgun",
        primitives=(
            PrimitiveVisual("cylinder", (0.09, 0.9, 0.09), (0.0, -0.03, 0.2), (50, 50, 50)),
            PrimitiveVisual("box", (0.2, 0.16, 0.45), (0.0, -0.08, -0.15), (95, 70, 40)),
        ),
    ),
    "AssaultRifle": WeaponVisual(
        weapon_name="AssaultRifle",
        primitives=(
            PrimitiveVisual("box", (0.38, 0.14, 0.92), (0.0, -0.05, 0.12), (40, 70, 45)),
            PrimitiveVisual("box", (0.18, 0.3, 0.16), (0.0, -0.22, -0.12), (25, 25, 25)),
            PrimitiveVisual("box", (0.16, 0.18, 0.28), (0.0, -0.02, 0.0), (30, 30, 30)),
        ),
    ),
    "RPG": WeaponVisual(
        weapon_name="RPG",
        primitives=(
            PrimitiveVisual("cylinder", (0.16, 1.2, 0.16), (0.0, -0.04, 0.2), (55, 80, 50)),
            PrimitiveVisual("cone", (0.3, 0.24, 0.3), (0.0, -0.04, 0.82), (120, 55, 40)),
            PrimitiveVisual("box", (0.22, 0.14, 0.22), (0.0, -0.2, -0.1), (30, 30, 30)),
        ),
    ),
}


def get_weapon_visual(weapon_name: str) -> WeaponVisual:
    """Return geometric primitive recipe for a known weapon."""
    if weapon_name not in WEAPON_VISUALS:
        raise ValueError(f"No visual definition for weapon '{weapon_name}'.")
    return WEAPON_VISUALS[weapon_name]

