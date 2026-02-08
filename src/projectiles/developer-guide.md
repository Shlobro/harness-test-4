# Projectiles Developer Guide

## Purpose
`src/projectiles/` models fired projectiles (bullets/pellets/rockets) and simulates their movement/collision.

## Files
- `projectile.py`: `Projectile` entity with movement, distance lifetime, and payload-based construction.
- `physics.py`: `ProjectilePhysicsSystem` frame-step logic that deactivates projectiles on wall or bounds collisions.

## Runtime Flow
1. A weapon returns payload dictionaries describing projectile spawn info.
2. `Projectile.from_payload(...)` converts payload into a normalized velocity-based entity.
3. `ProjectilePhysicsSystem.step(...)` advances active projectiles each frame.
4. Projectiles are deactivated when exceeding max distance, hitting static walls, or leaving world bounds.
