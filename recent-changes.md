# Recent Changes

## Code Review Fixes
- Fixed `src/ai/tactics.py:113`: `choose_tactical_action(...)` now raises `ValueError` when called on dead bots instead of returning `TacticalAction.TAKE_COVER`, preventing invalid post-death AI actions. Callers must filter dead bots before calling.
- Updated `src/ai/developer-guide.md` to document the dead-bot validation requirement.

## Previous Changes
- Added `src/environment/` with a 5-room indoor facility model (`lobby`, `central_hall`, `storage`, `lab`, `security`), doorway definitions, cover placements, waypoint graph, spawn points, and engine-agnostic lighting data.
- Implemented environment-to-collision conversion in `src/environment/collision.py`, generating doorway-aware wall AABBs plus cover collision volumes for player/projectile systems.
- Implemented environment navigation integration in `src/environment/navigation.py` with validation and `WaypointPathfinder` construction.
- Added tactical AI behavior in `src/ai/tactics.py`: cover detection/selection, tactical decision logic (`attack`, `take_cover`, `flank`), and flank route planning.
- Added wave orchestration in `src/ai/waves.py`: per-wave bot count scaling, difficulty scaling, and deterministic multi-bot spawning.
- Updated package exports in `src/ai/__init__.py` and `src/environment/__init__.py`.
- Added `tests/test_environment_and_tactics.py` covering facility layout, doorway/collision behavior, nav pathfinding usage, tactical AI decisions, and wave scaling.
- Updated developer guides in `src/environment/developer-guide.md`, `src/ai/developer-guide.md`, `src/developer-guide.md`, `developer-guide.md`, and `tests/developer-guide.md`.
- Marked 10 completed tasks in `tasks.md` for environment layout/collision/nav, tactical AI, wave systems, and environment documentation.

