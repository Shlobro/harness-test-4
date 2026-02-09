from src.graphics.effects import ExplosionEffectSystem, HitFeedbackSystem, MuzzleFlashEffectSystem
from src.graphics.lighting import create_basic_lighting_rig
from src.graphics.primitives import (
    create_bot_model,
    create_environment_object_models,
    create_player_model,
    create_weapon_visual_models,
)
from src.graphics.rendering import setup_default_rendering_context
from src.graphics.scene_builder import build_default_scene_blueprint


def test_rendering_context_is_initialized_and_scene_bound():
    context = setup_default_rendering_context()
    assert context.is_initialized is True
    assert context.active_scene_id == "arena_facility"
    assert context.settings.field_of_view_degrees > 0


def test_player_and_bot_models_use_primitives():
    player = create_player_model()
    bot = create_bot_model()
    assert player.model_id == "player_character"
    assert bot.model_id == "bot_character"
    assert len(player.primitives) >= 3
    assert len(bot.primitives) >= 3


def test_weapon_and_environment_models_are_available():
    weapons = create_weapon_visual_models()
    environment = create_environment_object_models()
    assert set(("Pistol", "Shotgun", "AssaultRifle", "RPG")).issubset(weapons.keys())
    assert set(("floor_tile", "wall_section", "cover_crate", "pillar", "doorway_frame")).issubset(
        environment.keys()
    )


def test_basic_lighting_has_ambient_and_directional():
    rig = create_basic_lighting_rig()
    assert rig.ambient.intensity > 0
    assert len(rig.directional) >= 1
    assert all(light.intensity > 0 for light in rig.directional)


def test_muzzle_flash_and_explosion_effects_emit_particles():
    muzzle_system = MuzzleFlashEffectSystem()
    explosion_system = ExplosionEffectSystem()

    muzzle_particles = muzzle_system.spawn((0.0, 1.2, 0.5), (0.0, 0.0, 1.0))
    explosion = explosion_system.spawn((1.0, 0.0, 2.0))

    assert len(muzzle_particles) >= 3
    assert explosion.radius > 0
    assert len(explosion.particles) >= 4


def test_hit_feedback_decays_over_time():
    feedback = HitFeedbackSystem()
    feedback.register_hit(60)
    strong = feedback.snapshot()
    assert strong.is_active is True
    assert strong.intensity > 0

    feedback.step(0.3)
    weaker = feedback.snapshot()
    assert weaker.intensity < strong.intensity

    feedback.step(1.0)
    ended = feedback.snapshot()
    assert ended.is_active is False
    assert ended.intensity == 0.0


def test_scene_blueprint_composes_full_graphics_stack():
    scene = build_default_scene_blueprint()
    assert scene.scene_id == "arena_facility"
    assert scene.rendering_context.is_initialized is True
    assert scene.player_model.model_id == "player_character"
    assert scene.bot_model.model_id == "bot_character"
    assert "RPG" in scene.weapon_models
    assert "wall_section" in scene.environment_models
