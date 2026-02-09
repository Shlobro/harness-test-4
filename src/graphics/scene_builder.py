"""Scene composition helpers for the FPS Bot Arena prototype."""

from __future__ import annotations

from dataclasses import dataclass

from src.graphics.lighting import LightingRig, create_basic_lighting_rig
from src.graphics.primitives import (
    ModelBlueprint,
    create_bot_model,
    create_environment_object_models,
    create_player_model,
    create_weapon_visual_models,
)
from src.graphics.rendering import RenderingContext, setup_default_rendering_context


@dataclass(frozen=True)
class SceneBlueprint:
    """Single payload describing everything needed to render the arena."""

    scene_id: str
    rendering_context: RenderingContext
    lighting: LightingRig
    player_model: ModelBlueprint
    bot_model: ModelBlueprint
    environment_models: dict[str, ModelBlueprint]
    weapon_models: dict[str, ModelBlueprint]


def build_default_scene_blueprint() -> SceneBlueprint:
    """Build the default FPS arena rendering payload."""
    return SceneBlueprint(
        scene_id="arena_facility",
        rendering_context=setup_default_rendering_context(),
        lighting=create_basic_lighting_rig(),
        player_model=create_player_model(),
        bot_model=create_bot_model(),
        environment_models=create_environment_object_models(),
        weapon_models=create_weapon_visual_models(),
    )
