# FPS Bot Arena Prototype

Python/Ursina foundation for a first-person wave-shooter prototype with progression weapons and a glitch ending path.

## Requirements
- Python 3.11+
- `pip`

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run Tests
```bash
pytest
```

## Project Layout
- `src/core/`: game loop, state manager, clock/time controls, camera/input, movement/collision, raycasting.
- `src/player/`: player state, health/economy, inventory, weapon switching, firing logic.
- `src/weapons/`: weapon definitions, switch transitions, weapon visual primitive definitions.
- `src/projectiles/`: projectile entities and projectile physics simulation.
- `config/`: centralized runtime configuration.
- `tests/`: pytest suite validating gameplay foundations.

## Current Gameplay Foundations
- WASD/mouse input normalization and first-person camera state.
- Collision-aware movement against world AABBs.
- Weapon progression classes: Pistol, Shotgun, Assault Rifle, RPG.
- Projectile and hit-scan shooting paths.
- Smooth timed weapon-switch state model.
- RPG crash trigger flag for glitch-sequence integration.

## Controls and Gameplay Doc
See `GAMEPLAY.md` for player controls, loop, and progression summary.
