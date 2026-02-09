"""Graphics blueprints and lightweight effect systems."""

from src.graphics.effects import (
    ExplosionEffect,
    ExplosionEffectSystem,
    HitFeedbackSnapshot,
    HitFeedbackSystem,
    MuzzleFlashEffectSystem,
    Particle,
)
from src.graphics.lighting import AmbientLight, DirectionalLight, LightingRig, create_basic_lighting_rig
from src.graphics.primitives import (
    ModelBlueprint,
    PrimitiveMesh,
    create_bot_model,
    create_environment_object_models,
    create_player_model,
    create_weapon_visual_models,
)
from src.graphics.rendering import RenderSettings, RenderingContext, setup_default_rendering_context
from src.graphics.scene_builder import SceneBlueprint, build_default_scene_blueprint

__all__ = [
    "AmbientLight",
    "DirectionalLight",
    "ExplosionEffect",
    "ExplosionEffectSystem",
    "HitFeedbackSnapshot",
    "HitFeedbackSystem",
    "LightingRig",
    "ModelBlueprint",
    "MuzzleFlashEffectSystem",
    "Particle",
    "PrimitiveMesh",
    "RenderSettings",
    "RenderingContext",
    "SceneBlueprint",
    "build_default_scene_blueprint",
    "create_basic_lighting_rig",
    "create_bot_model",
    "create_environment_object_models",
    "create_player_model",
    "create_weapon_visual_models",
    "setup_default_rendering_context",
]
