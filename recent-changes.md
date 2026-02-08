# Recent Changes

## 2026-02-08 (Code Review Fixes)
- Fixed raycasting bug in `src/core/raycasting.py`: Removed incorrect early rejection of targets when `projection < 0`, which was causing false negatives for rays originating inside spheres or near large targets.
- Added `.gitignore` to properly exclude Python bytecode files (`*.pyc`, `__pycache__/`) and other build artifacts from version control.
- Removed all tracked `.pyc` files from git to reduce repository noise.

## 2026-02-08
- Implemented hit-scan raycasting in `src/core/raycasting.py` with nearest-hit sphere target detection and exported it via `src/core/__init__.py`.
- Upgraded `GameClock` in `src/core/game_clock.py` with pause/resume support, time scaling, unscaled elapsed tracking, and reset behavior.
- Added smooth weapon switch transitions via `src/weapons/switching.py` and integrated the workflow into `src/player/player.py`.
- Added geometric weapon visual definitions in `src/weapons/visuals.py` for Pistol, Shotgun, AssaultRifle, and RPG; exported through `src/weapons/__init__.py`.
- Added player hit-scan firing API (`shoot_hitscan`) using the new raycasting system.
- Expanded tests:
  - `tests/test_core_systems.py`: time controls and raycasting coverage.
  - `tests/test_advanced_combat_and_movement.py`: smooth switching, hit-scan firing, and weapon visual definitions.
- Added user-facing docs:
  - `README.md` with install/test/run overview.
  - `GAMEPLAY.md` with controls and gameplay loop documentation.
- Updated developer guides to reflect current behavior:
  - `developer-guide.md`
  - `src/developer-guide.md`
  - `src/core/developer-guide.md`
  - `src/player/developer-guide.md`
  - `src/weapons/developer-guide.md`
  - `tests/developer-guide.md`
- Updated `tasks.md` to mark 10 completed tasks as done.

