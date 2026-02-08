# Src Developer Guide

## Purpose
`src/` contains the game runtime modules for loop/state management, player logic, weapons, and projectile simulation.

## Folder Overview
- `core/`: frame stepping, game clock (pause + time scale), state machine, input normalization, first-person camera state, movement, collision primitives, raycasting, and HUD runtime event bridges.
- `player/`: player runtime model (health, money, inventory, immediate + smooth weapon switching, reload, hit-scan/projectile shooting, game-over/respawn).
- `weapons/`: reusable weapon abstractions, concrete weapons (pistol/shotgun/assault rifle/RPG), switch-transition state, and primitive visual definitions.
- `projectiles/`: projectile entities plus physics stepping and world collision checks.
- `ui/`: shop wheel catalog, radial layout generation, affordability/equipped status projection, and open/close interaction controller.
- `hud/`: HUD overlay payload generation for health, ammo, money, crosshair, damage feedback, and kill notifications.
- `ai/`: bot runtime model, shot-accuracy helpers, tactical decision/cover/flank planners, and wave spawning+difficulty scaling.
- `economy/`: money pickup entities, glowing primitive visual definitions, pickup lifecycle, and player collection logic.
- `environment/`: multi-room facility definitions, doorway connectivity, spawn/light validation helpers, cover placements, collision world generation, and nav graph generation.

## Integration Flow
1. The platform layer collects raw input and passes it to `core.input_handler.InputHandler`.
2. Mouse look deltas update `core.camera.FirstPersonCamera`; resulting yaw drives movement direction.
3. `core.movement.PlayerMovementController` computes collision-aware movement against `core.collision.CollisionWorld`.
4. The game loop (`core.game_loop.GameLoop`) advances time using `core.game_clock.GameClock`.
5. Player actions call weapon models for cooldown/ammo/reload behavior, smooth switch timing, and projectile payload generation.
6. `projectiles.physics.ProjectilePhysicsSystem` advances active projectiles and resolves wall/bounds collisions.
7. Hit-scan fire paths use `core.raycasting.RaycastingSystem` to resolve nearest target hits.
8. `core.input_handler.InputHandler` emits a `toggle_shop` action on `B` key press edges for `ui.shop_wheel.ShopWheelController` consumption.
9. `environment.create_default_facility_layout()` provides rooms/doorways/cover/waypoints as a single world source.
10. `environment.build_collision_world(...)` generates wall/cover AABBs for movement and projectile collision.
11. `environment.build_waypoint_pathfinder(...)` creates pathfinding data aligned with the same facility layout.
12. `ai.bot.Bot` instances can fire at players using inaccuracy-aware aim and spawn money drops on death.
13. `ai.tactics` chooses between attack/cover/flank and computes flanking approach routes.
14. `ai.waves.WaveDirector` scales wave difficulty and spawns multiple bots from configured spawn positions.
15. `economy.money.MoneyPickupSystem` resolves pickup collisions and deposits collected money to `player.Player`.
16. `hud.HudOverlayController` builds render-ready HUD state and manages damage/kill feedback timers.
17. `core.runtime.RuntimeSession` and `HudEventRuntimeBridge` queue gameplay damage/kill events and flush them to HUD only during active `playing` loop frames.
