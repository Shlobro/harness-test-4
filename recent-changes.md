# Recent Changes

## 2026-02-08 (Code Review Fix)
- Fixed `CollisionWorld.outside_world_bounds` in `src/core/collision.py` to use containment check instead of intersection check. Now correctly returns `True` when any part of a box is outside world bounds, preventing players/projectiles from drifting outside world edges.

## 2026-02-08
- Implemented first-person camera state in `src/core/camera.py` with yaw/pitch mouse-look updates and pitch clamping.
- Implemented collision primitives and movement controller in `src/core/collision.py` and `src/core/movement.py` for player movement with wall/bounds collision and slide resolution.
- Added new weapon implementations:
  - `src/weapons/shotgun.py` (pellet spread payload)
  - `src/weapons/assault_rifle.py` (rapid fire)
  - `src/weapons/rpg.py` (crash trigger flag when fired)
- Extended `src/weapons/weapon.py` with ammo reload mechanics, total ammo tracking, and projectile payload generation.
- Extended `src/player/player.py` with weapon cycling, reload delegation, projectile firing API, game-over state on death, and respawn handling.
- Added projectile package `src/projectiles/`:
  - `projectile.py` for projectile entities and movement/lifetime
  - `physics.py` for projectile movement and world collision deactivation
- Updated package exports in `src/core/__init__.py`, `src/player/__init__.py`, and `src/weapons/__init__.py`.
- Added `tests/test_advanced_combat_and_movement.py` covering camera look, movement collision, weapon switching/reload/respawn, new weapons, and projectile physics.
- Verified full test suite passes: `19 passed`.

