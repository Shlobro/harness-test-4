# Developer Guide

## Project Architecture
This project uses **Python + Ursina** for a lightweight FPS prototype.

The current codebase implements engine-agnostic gameplay foundations in pure Python:
- Core runtime loop and timing
- State machine for high-level game flow
- Input normalization for WASD + mouse look
- First-person camera and movement/collision simulation
- Player model with health, money, inventory, weapon switching, reload, and respawn/game-over
- Weapon system with pistol, shotgun, assault rifle, and RPG
- Projectile entities and physics for bullets, pellets, and rockets

## Directory Map
- `src/`: runtime game systems.
  - `src/core/`: game loop, game clock, state manager, input, camera, movement, and collision primitives.
  - `src/player/`: player runtime state, combat APIs, inventory switching, reload, and respawn.
  - `src/weapons/`: weapon base model and concrete implementations.
  - `src/projectiles/`: projectile entity construction and world collision physics.
- `assets/`: static assets (models, audio, textures). Currently placeholder-only.
- `config/`: centralized runtime configuration modules.
- `tests/`: automated test suite.
- `requirements.txt`: pinned Python dependencies.

## Technology Stack Decision
- Language/runtime: Python 3.11+.
- Engine: Ursina (`ursina==6.1.2`).
- Rationale: aligns with quick prototype goals, simple geometric rendering, and first-person mechanics without heavy custom engine work.

## Current Runtime Config
- `config/config.py` exposes `GAME_CONFIG` and `ECONOMY_CONFIG` dataclass instances.
- Game systems should import from `config.config` rather than duplicating constant values.

## Implemented Gameplay Foundations
- `GameLoop.step(now)` advances time each frame and dispatches updates only while in `playing`.
- `GameStateManager` enforces valid transitions across `menu`, `playing`, `paused`, and `crashed`.
- `InputHandler.build_frame(...)` translates keyboard/mouse input into movement/look axes.
- `FirstPersonCamera` tracks yaw/pitch and clamps vertical look.
- `PlayerMovementController` applies yaw-relative movement and resolves AABB wall collisions with slide behavior.
- `Player` enforces bounded health, game-over on death, validated currency operations, inventory ownership checks, weapon cycling, reload, projectile firing, and respawn.
- `Weapon` enforces cooldown/ammo, reload behavior, and projectile payload generation.
- `Pistol`, `Shotgun`, `AssaultRifle`, and `RPG` provide progression-ready weapon behavior; RPG toggles a crash trigger flag when fired.
- `ProjectilePhysicsSystem` advances projectile motion and deactivates projectiles that hit walls or leave world bounds.

## Development Notes
- Keep gameplay constants in `config/config.py` until a richer configuration layer is needed.
- Add per-folder `developer-guide.md` files when new code folders gain implementation files.
