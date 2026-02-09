# Tests Developer Guide

## Overview
This directory contains the automated test suite for the FPS Bot Arena project.

## Testing Framework
- **Framework:** `pytest`
- **Rationale:** Standard, powerful, and easy-to-use testing framework for Python.

## Structure
- Test files should be named `test_<module_name>.py`.
- Tests should mirror the structure of the `src/` and `config/` directories where applicable.
- `conftest.py` inserts the repository root into `sys.path` so package-style imports (`src.*`, `config.*`) work in pytest.

## Current Test Modules
- `test_config.py`: validates immutable config defaults.
- `test_core_systems.py`: validates game clock timing controls, raycasting behavior, state transitions, input handling, loop update dispatch behavior, runtime HUD event hook integration, runtime audio event bridge playback gating by game state, and menu/game-flow transitions for glitch-driven crash ending behavior.
- `test_player_and_weapons.py`: validates player health/economy/inventory/shooting and weapon cooldown/ammo behavior.
- `test_advanced_combat_and_movement.py`: validates camera look, movement collision/slide, smooth weapon switching transitions, hit-scan shooting, weapon visuals, weapon behaviors, and projectile collisions.
- `test_shop_ui.py`: validates shop wheel radial layout, `B`-toggle input behavior, pause/state synchronization while shopping, pricing visibility, affordability feedback, purchase validation, and owned-weapon selection/equip behavior.
- `test_ai_and_economy.py`: validates bot health/state transitions, waypoint pathfinding, accuracy-varied bot shooting, death money-drop spawning, pickup collision, visual mapping, and player collection flow.
- `test_environment_and_tactics.py`: validates multi-room facility structure, doorway connectivity traversal, spawn placement inside rooms, lighting validity, doorway-aware collision generation, environment nav graph usage, tactical cover/flank decisions, and wave difficulty scaling/spawning.
- `test_hud.py`: validates HUD snapshot generation (health/ammo/money/crosshair), damage indicator timing, and kill notification/counter behavior.
- `test_glitch_and_audio.py`: validates fake BSOD content quality/recoverability (including mockup metadata), RPG-triggered crash transition effects, crash lifecycle audio cue emission ordering, recovery flow back to idle, audio event lifecycle controls, expanded sound-manager event coverage (movement/enemy/economy/UI/ambient/glitch), and RPG pre-crash cue playback ordering.
- `test_graphics_system.py`: validates rendering-context initialization, primitive player/bot/environment/weapon model blueprints, ambient+directional lighting rig creation, muzzle flash/explosion particle payload generation, hit-feedback decay behavior, and full graphics scene blueprint composition.

## Running Tests
To run all tests, execute the following command from the project root:
```bash
pytest
```
