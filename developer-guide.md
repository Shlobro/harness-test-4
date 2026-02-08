# Developer Guide

## Project Architecture
This project uses **Python + Ursina** for a lightweight FPS prototype.

The current codebase implements engine-agnostic gameplay foundations in pure Python:
- Core runtime loop and timing
- State machine for high-level game flow
- Input normalization for WASD + mouse look
- Player model with health, money, inventory, and shooting
- Weapon base behavior and starter pistol

## Directory Map
- `src/`: runtime game systems.
  - `src/core/`: game loop, game clock, state manager, input handler.
  - `src/player/`: player model and starter loadout behavior.
  - `src/weapons/`: base weapon logic and concrete weapons.
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
- `Player` enforces bounded health, validated currency operations, inventory ownership checks, and alive-only firing.
- `Weapon.fire(now)` enforces cooldown + ammo consumption.
- `Pistol` is the starter weapon with tuned prototype stats.

## Development Notes
- Keep gameplay constants in `config/config.py` until a richer configuration layer is needed.
- Add per-folder `developer-guide.md` files when new code folders gain implementation files.
