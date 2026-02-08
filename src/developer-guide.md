# Src Developer Guide

## Purpose
`src/` contains the game runtime modules for loop/state management, player logic, weapons, and projectile simulation.

## Folder Overview
- `core/`: frame stepping, game clock, state machine, input normalization, first-person camera state, movement, and collision primitives.
- `player/`: player runtime model (health, money, inventory, weapon switching, reload, shooting, game-over/respawn).
- `weapons/`: reusable weapon abstractions and concrete weapon implementations (pistol/shotgun/assault rifle/RPG).
- `projectiles/`: projectile entities plus physics stepping and world collision checks.

## Integration Flow
1. The platform layer collects raw input and passes it to `core.input_handler.InputHandler`.
2. Mouse look deltas update `core.camera.FirstPersonCamera`; resulting yaw drives movement direction.
3. `core.movement.PlayerMovementController` computes collision-aware movement against `core.collision.CollisionWorld`.
4. The game loop (`core.game_loop.GameLoop`) advances time using `core.game_clock.GameClock`.
5. Player actions call weapon models for cooldown/ammo/reload behavior and projectile payload generation.
6. `projectiles.physics.ProjectilePhysicsSystem` advances active projectiles and resolves wall/bounds collisions.
