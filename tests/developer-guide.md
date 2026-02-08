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
- `test_core_systems.py`: validates game clock timing controls, raycasting behavior, state transitions, input handling, and loop update dispatch behavior.
- `test_player_and_weapons.py`: validates player health/economy/inventory/shooting and weapon cooldown/ammo behavior.
- `test_advanced_combat_and_movement.py`: validates camera look, movement collision/slide, smooth weapon switching transitions, hit-scan shooting, weapon visuals, weapon behaviors, and projectile collisions.
- `test_shop_ui.py`: validates shop wheel radial layout, `B`-toggle input behavior, pause/state synchronization while shopping, pricing visibility, affordability feedback, purchase validation, and owned-weapon selection/equip behavior.
- `test_ai_and_economy.py`: validates bot health/state transitions, waypoint pathfinding, accuracy-varied bot shooting, death money-drop spawning, pickup collision, visual mapping, and player collection flow.
- `test_environment_and_tactics.py`: validates multi-room facility structure, doorway-aware collision generation, environment nav graph usage, tactical cover/flank decisions, and wave difficulty scaling/spawning.

## Running Tests
To run all tests, execute the following command from the project root:
```bash
pytest
```
