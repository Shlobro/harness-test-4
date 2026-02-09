"""Primitive-model blueprints for characters, weapons, and environment props."""

from __future__ import annotations

from dataclasses import dataclass

from src.weapons.visuals import WEAPON_VISUALS


Vector3 = tuple[float, float, float]
ColorRGB = tuple[int, int, int]


@dataclass(frozen=True)
class PrimitiveMesh:
    """A single render primitive and its transform-style values."""

    shape: str
    size: Vector3
    offset: Vector3
    color: ColorRGB


@dataclass(frozen=True)
class ModelBlueprint:
    """Collection of primitives describing one renderable model."""

    model_id: str
    primitives: tuple[PrimitiveMesh, ...]


def create_player_model() -> ModelBlueprint:
    """Build a simple FPS player body from cubes and spheres."""
    return ModelBlueprint(
        model_id="player_character",
        primitives=(
            PrimitiveMesh("box", (0.5, 0.9, 0.35), (0.0, 1.1, 0.0), (55, 90, 140)),
            PrimitiveMesh("sphere", (0.32, 0.32, 0.32), (0.0, 1.8, 0.0), (230, 210, 180)),
            PrimitiveMesh("box", (0.18, 0.7, 0.18), (-0.18, 0.35, 0.0), (35, 45, 55)),
            PrimitiveMesh("box", (0.18, 0.7, 0.18), (0.18, 0.35, 0.0), (35, 45, 55)),
        ),
    )


def create_bot_model() -> ModelBlueprint:
    """Build a tactical bot model with distinct silhouette/colors."""
    return ModelBlueprint(
        model_id="bot_character",
        primitives=(
            PrimitiveMesh("box", (0.52, 0.88, 0.36), (0.0, 1.08, 0.0), (80, 40, 40)),
            PrimitiveMesh("box", (0.36, 0.26, 0.3), (0.0, 1.74, 0.0), (45, 45, 45)),
            PrimitiveMesh("sphere", (0.08, 0.08, 0.08), (-0.1, 1.74, 0.16), (200, 45, 45)),
            PrimitiveMesh("sphere", (0.08, 0.08, 0.08), (0.1, 1.74, 0.16), (200, 45, 45)),
        ),
    )


def create_weapon_visual_models() -> dict[str, ModelBlueprint]:
    """Convert progression weapon visuals into graphics-model blueprints."""
    models: dict[str, ModelBlueprint] = {}
    for weapon_name, weapon_visual in WEAPON_VISUALS.items():
        models[weapon_name] = ModelBlueprint(
            model_id=f"weapon_{weapon_name.lower()}",
            primitives=tuple(
                PrimitiveMesh(
                    shape=primitive.shape,
                    size=primitive.size,
                    offset=primitive.offset,
                    color=primitive.color,
                )
                for primitive in weapon_visual.primitives
            ),
        )
    return models


def create_environment_object_models() -> dict[str, ModelBlueprint]:
    """Create base environment props built from simple geometric shapes."""
    return {
        "floor_tile": ModelBlueprint(
            model_id="env_floor_tile",
            primitives=(PrimitiveMesh("box", (4.0, 0.12, 4.0), (0.0, -0.06, 0.0), (65, 68, 74)),),
        ),
        "wall_section": ModelBlueprint(
            model_id="env_wall_section",
            primitives=(PrimitiveMesh("box", (4.0, 3.0, 0.25), (0.0, 1.5, 0.0), (95, 98, 108)),),
        ),
        "cover_crate": ModelBlueprint(
            model_id="env_cover_crate",
            primitives=(
                PrimitiveMesh("box", (1.0, 1.0, 1.0), (0.0, 0.5, 0.0), (105, 78, 52)),
                PrimitiveMesh("box", (0.8, 0.1, 0.8), (0.0, 1.05, 0.0), (135, 100, 66)),
            ),
        ),
        "pillar": ModelBlueprint(
            model_id="env_pillar",
            primitives=(PrimitiveMesh("cylinder", (0.55, 3.0, 0.55), (0.0, 1.5, 0.0), (90, 92, 98)),),
        ),
        "doorway_frame": ModelBlueprint(
            model_id="env_doorway_frame",
            primitives=(
                PrimitiveMesh("box", (0.2, 2.6, 0.3), (-0.9, 1.3, 0.0), (88, 90, 98)),
                PrimitiveMesh("box", (0.2, 2.6, 0.3), (0.9, 1.3, 0.0), (88, 90, 98)),
                PrimitiveMesh("box", (2.0, 0.2, 0.3), (0.0, 2.6, 0.0), (88, 90, 98)),
            ),
        ),
    }
