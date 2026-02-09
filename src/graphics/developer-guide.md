# Graphics Developer Guide

## Purpose
`src/graphics/` provides engine-agnostic rendering blueprints and visual-effect payloads that a real Ursina/Three.js adapter can consume.

## Files
- `rendering.py`: render-window/camera settings and context lifecycle (`initialize`, `bind_scene`) for a default 3D scene.
- `primitives.py`: primitive-mesh model blueprints for player, bot, environment props, and converted weapon visuals.
- `lighting.py`: ambient + directional lighting dataclasses and a default facility lighting rig.
- `effects.py`: deterministic muzzle flash particles, RPG explosion payloads, and decaying hit/damage feedback state.
- `scene_builder.py`: composes one `SceneBlueprint` with context, lights, character models, environment props, and weapon models.
- `__init__.py`: package exports.

## Runtime Behavior
- `setup_default_rendering_context()` initializes a ready-to-use `RenderingContext` bound to `arena_facility`.
- `create_player_model()` and `create_bot_model()` return multi-primitive silhouettes so character roles are readable without external art.
- `create_weapon_visual_models()` mirrors definitions from `src/weapons/visuals.py` into graphics-level `ModelBlueprint` values.
- `create_environment_object_models()` defines floor, wall, crate, pillar, and doorway-frame primitives for modular room assembly.
- `create_basic_lighting_rig()` returns one ambient light plus two directional lights for warm key + cool fill balance.
- `MuzzleFlashEffectSystem.spawn(...)` and `ExplosionEffectSystem.spawn(...)` return deterministic particles to keep tests stable.
- `HitFeedbackSystem` accumulates intensity on hits and decays over time; `snapshot()` provides tint, shake, and active flag values.

## Integration Notes
- This package does not render directly; it supplies data for whichever renderer layer is chosen.
- The host game loop should call `HitFeedbackSystem.step(delta_time)` every frame while playing.
- RPG detonation and standard weapon firing should request explosion/muzzle payloads from this package and hand them to the renderer.
