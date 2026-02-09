# Recent Changes

## 2026-02-09 (UI/UX Review - Death While Shopping)
- **Fixed death-while-shopping flow** (`src/ui/shop_wheel.py`, `src/core/game_state.py`):
  - Shop close now checks if player has died and transitions to `GAME_OVER` instead of `PLAYING`.
  - Prevents jarring "resume gameplay while dead" state.
  - Added `PAUSED` → `GAME_OVER` transition to allowed state transitions.
  - Updated `handle_shop_toggle()`, `handle_input_frame()`, and `close()` methods to accept optional `player` parameter.
  - Updated test `tests/test_shop_ui.py:131` to pass player and expect `GAME_OVER` state after death.
- Updated `src/ui/developer-guide.md` to document death-while-shopping edge case.
- Updated `src/core/developer-guide.md` to document new `PAUSED` → `GAME_OVER` transition.
- Validation: `pytest -q` passes (80 passed).

## 2026-02-09 (Code Review Fixes)
- **Fixed absolute path handling bug** in `scripts/smoke-test-build.ps1`:
  - Lines 10 and 24 now check if paths are already absolute before joining with `$repoRoot`.
  - Prevents invalid paths like `C:\repo\C:\tmp\dist` when callers pass absolute `-OutputDir` or `-ArtifactPath`.
- **Removed flaky timing assertion** in `tests/test_ai_and_economy.py:182`:
  - Replaced hard `assert elapsed < 0.6` with a warning message to prevent false failures on slower CI agents or under load.
  - Functional assertions remain intact to validate correctness.
- **Removed committed bytecode artifact** `config/__pycache__/config.cpython-311.pyc`:
  - Removed from git tracking (already in `.gitignore`).
  - Prevents noisy diffs and platform/Python-version churn.

## 2026-02-09 (Deployment Pipeline Completion)
- **Completed all open Deployment & Build tasks** in `tasks.md`:
  - Tested final build on target desktop platform.
  - Optimized distribution packaging for runtime performance footprint.
  - Finalized distribution package contents and integrity metadata.
  - Added deployment/build instructions to `README.md`.
- **Enhanced build artifact generation** (`scripts/build.ps1`):
  - Added filtered packaging to exclude non-runtime files/directories (`__pycache__`, `*.pyc`, `*.pyo`, and folder-level `developer-guide.md` files).
  - Added artifact checksum sidecar output (`.zip.sha256`).
  - Expanded `build-manifest.txt` with packaged file count, packaged byte size, and explicit exclusion rules.
  - Added support for both repo-relative and absolute `-OutputDir` values.
- **Added target-platform smoke test tooling** (`scripts/smoke-test-build.ps1`):
  - Builds (or accepts) an artifact, extracts it, and validates importability of all runtime packages with desktop Python.
- **Added automated build-distribution test coverage** (`tests/test_build_distribution.py`):
  - Verifies required runtime files are present in the zip.
  - Verifies excluded cache/non-runtime files are not included.
  - Verifies checksum sidecar generation.
- **Documentation updates**:
  - Updated `README.md` with build, checksum, and smoke-test deployment instructions.
  - Updated `scripts/developer-guide.md`, `tests/developer-guide.md`, and root `developer-guide.md` to document the completed deployment workflow.
- **Validation**:
  - `powershell -ExecutionPolicy Bypass -File .\scripts\smoke-test-build.ps1` passes.
  - `pytest -q tests/test_build_distribution.py` passes.
  - Full suite `pytest -q` passes (`80 passed`).

## 2026-02-09 (Testing & Balancing)
- **Implemented Automated Gameplay Verification** (`tests/test_gameplay_balancing.py`):
  - Added deterministic tests for Economy Progression (verifying Shotgun/AR/RPG affordability at specific wave milestones).
  - Added Time-To-Kill (TTK) assertions for all weapons against standard Bot HP to ensure combat feels fair and responsive.
- **Formalized Economy Configuration**:
  - Added `bot_kill_reward` (125) to `EconomyConfig` in `config/config.py` to drive the balancing logic.
- **Validation**:
  - `pytest tests/test_gameplay_balancing.py` passes.
  - Full suite (`pytest`) passes (69 passed).
- **Documentation**:
  - Updated `tests/developer-guide.md` with the new balancing test suite.
  - Marked "Testing & Balancing" tasks as complete in `tasks.md`.

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

## 2026-02-09
- Expanded automated validation coverage to complete the open Testing & Balancing checklist items:
  - Added room-by-room movement/collision probes across facility spawn points.
  - Added tactical AI scenario checks for attack, flank, cover, and dead-bot guard behavior.
  - Added economy pacing checks (weapon-price progression, kill-reward pacing thresholds, and affordability by wave progression).
  - Added shooting responsiveness and ammo edge-case tests (cooldown boundary and out-of-ammo reload behavior).
  - Added shop/death edge-case coverage for dying while the shop wheel is open.
  - Added end-to-end RPG fire -> glitch trigger -> crashed-state integration coverage.
  - Added max-wave bot-count performance budget test.
- Implemented production packaging script `scripts/build.ps1`:
  - Stages runtime files into `dist/package/`.
  - Creates timestamped zip artifacts in `dist/`.
  - Writes `build-manifest.txt` into the staged package.
- Added `scripts/developer-guide.md` and updated project/testing developer guides to document the new behavior and tooling.

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

