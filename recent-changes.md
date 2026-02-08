# Recent Changes

## 2026-02-08

- Implemented foundational gameplay runtime modules:
  - `src/core/game_state.py`: validated game state manager for `menu`, `playing`, `paused`, `crashed`.
  - `src/core/game_clock.py`: delta-time and elapsed-time tracking.
  - `src/core/input_handler.py`: WASD + mouse-look input normalization.
  - `src/core/game_loop.py`: frame-stepped loop that dispatches updates only in `playing`.
- Implemented player systems in `src/player/player.py`:
  - player creation with position/rotation/health/money
  - health damage/heal/death behavior
  - money add/spend behavior with validation
  - weapon inventory ownership and equip rules
  - shooting through equipped weapon with ammo/cooldown enforcement
- Implemented weapon systems:
  - `src/weapons/weapon.py`: reusable weapon base class with common stats and cooldown-aware firing.
  - `src/weapons/pistol.py`: starter pistol stats and behavior.
- Added/updated developer documentation:
  - `src/developer-guide.md`
  - `src/core/developer-guide.md`
  - `src/player/developer-guide.md`
  - `src/weapons/developer-guide.md`
  - `tests/developer-guide.md`
  - root `developer-guide.md`
- Added automated tests and fixed import configuration:
  - `tests/conftest.py`
  - `tests/test_core_systems.py`
  - `tests/test_player_and_weapons.py`
- Added `test_player_position_and_rotation_setters` to `tests/test_player_and_weapons.py` to verify transform updates.
- **Error Handling Improvements (Code Review Fixes)**:
  - `src/player/player.py`: Changed `equipped_weapon_name` default from `"Pistol"` to `None`. Added validation in `equipped_weapon` property to raise descriptive `ValueError` if weapon is not equipped or not in inventory, preventing `KeyError` crashes.
  - `src/weapons/weapon.py`: Added validation in `__post_init__` to ensure `fire_rate > 0`, preventing `ZeroDivisionError` in `cooldown_seconds` property.
  - `src/core/game_loop.py`: Added per-callback exception handling in `step()` method. Callbacks that fail now log errors without crashing the game loop, ensuring other callbacks continue to run.
- Validation: `pytest -q` passes (`14 passed`).
