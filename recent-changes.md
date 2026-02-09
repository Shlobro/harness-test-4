# Recent Changes

## 2026-02-09
- Implemented a new `src/graphics/` subsystem with:
  - 3D render context setup (`rendering.py`).
  - Primitive model blueprints for player and bot characters (`primitives.py`).
  - Weapon model blueprint conversion using simple geometric shapes (`primitives.py`).
  - Environment object blueprints (floor, walls, crate, pillar, doorway frame) (`primitives.py`).
  - Ambient + directional lighting rig setup (`lighting.py`).
  - Muzzle flash particle effect system (`effects.py`).
  - RPG explosion effect payload generation (`effects.py`).
  - Hit/damage visual feedback system with time-decay (`effects.py`).
  - Full scene composition helper that bundles context, lighting, and model sets (`scene_builder.py`).
- Added `src/graphics/developer-guide.md` and package exports in `src/graphics/__init__.py`.
- Added coverage for graphics systems in `tests/test_graphics_system.py`.
- Updated documentation to reflect graphics integration:
  - `src/developer-guide.md`
  - `developer-guide.md`
  - `tests/developer-guide.md`
- Fixed two existing regressions discovered during validation:
  - Crash transition now moves gameplay to `crashed` for all gameplay-locking glitch phases in `src/menus/controller.py`.
  - Fake BSOD restart hint wording now includes the expected `ENTER or ESC` text in `src/glitch/bsod.py`.
- Updated `src/menus/developer-guide.md` to document the crash transition behavior.
- Updated `src/menus/developer-guide.md` to document the crash transition behavior.

## 2026-02-09 (Game Flow & Menus)
- **Completed Game Flow Logic** (`src/menus/` and `src/core/`):
  - Added `GameState.GAME_OVER` and `GameState.CONTROLS` to `src/core/game_state.py`.
  - Implemented `build_pause_menu_screen`, `build_game_over_screen`, and `build_controls_screen` in `src/menus/screens.py`.
  - Updated `GameFlowController` in `src/menus/controller.py` to:
    - Handle transitions to/from `PAUSED`, `CONTROLS`, and `GAME_OVER`.
    - Manage session stats (score, waves) for the Game Over screen.
    - Process generic menu actions via `handle_menu_action(action_id)`.
- **Validation**:
  - Added `test_game_flow_manages_controls_pause_and_game_over_screens` to `tests/test_core_systems.py`.
  - Verified menu navigation, pause toggling, and game over triggering.
- **Documentation**:
  - Updated `src/menus/developer-guide.md` with new screen payloads and integration notes.
  - Updated `src/developer-guide.md` to reflect expanded menu capabilities.
  - Marked Game Flow tasks as complete in `tasks.md`.

## 2026-02-09 (UI/UX Review Fixes)
- **Fixed abrupt crash screen transition** (`src/menus/controller.py`):
  - Changed game state transition to `CRASHED` to only occur when `is_crash_screen_visible` is true (after transition completes).
  - Previously used `should_lock_gameplay` which triggered immediately during `TRANSITION` phase, causing the BSOD to appear before visual effects finished ramping.
  - Now the 1.2-second transition effect plays completely before the crash screen appears.
- Updated `src/menus/developer-guide.md` to reflect corrected crash transition timing.
- Updated test in `tests/test_core_systems.py` to validate correct transition timing (game stays in `PLAYING` during transition, switches to `CRASHED` after transition completes).
- Validation: `pytest -q` passes (`66 passed`).
- Validation: `pytest -q` passes (`66 passed`).

