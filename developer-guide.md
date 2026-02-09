# Developer Guide

## Project Architecture
This project uses **Python + Ursina** for a lightweight FPS prototype.

The current codebase implements engine-agnostic gameplay foundations in pure Python:
- Core runtime loop and timing
- State machine for high-level game flow
- Clock pause/resume and time scaling controls
- Runtime bridge for HUD damage/kill event hooks through the frame loop
- Runtime bridge for queued audio events through the frame loop (weapon, movement, AI, economy, UI, ambient)
- Input normalization for WASD + mouse look
- First-person camera and movement/collision simulation
- Raycasting-based hit-scan traces
- Player model with health, money, inventory, immediate/smooth weapon switching, reload, projectile fire, hit-scan fire, and respawn/game-over
- Weapon system with pistol, shotgun, assault rifle, RPG, switch transitions, and primitive visual recipes
- Projectile entities and physics for bullets, pellets, and rockets
- Glitch/crash sequence system with fake BSOD content, RPG-triggered transition timing, and recoverable restart flow
- Menu/game-flow layer with main menu payload, crash ending screen payload, and glitch-driven state transitions
- Audio abstraction layer with sound-event engine and placeholder/procedural profiles for weapon fire, footsteps, bot events, pickup/UI sounds, ambient loop audio, and RPG pre-crash cue
- Shop wheel UI logic with radial layout, weapon prices, affordability feedback, purchase validation, and inventory equip flow
- HUD overlay logic for health/ammo/money/crosshair, damage feedback, and kill notifications
- Multi-room facility model with doorway connectivity, cover placements, lighting profile, and nav waypoints
- Facility layout validation for doorways, spawn placement, and non-degenerate lighting vectors
- Collision world generation from environment rooms/doorways/cover for movement and projectile systems
- Bot runtime model with stateful health/death handling, shot variance, tactical action selection, cover/flank planning, and wave spawning
- Money drop economy with collectible pickups, collision-based collection, and primitive visual definitions

## Directory Map
- `src/`: runtime game systems.
- `src/core/`: game loop, game clock, state manager, input, camera, movement, collision primitives, raycasting, and HUD/audio runtime bridges.
  - `src/player/`: player runtime state, combat APIs, instant/smooth inventory switching, reload, hit-scan, and respawn.
  - `src/weapons/`: weapon base model, concrete implementations, visual definitions, and switch transition state.
  - `src/projectiles/`: projectile entity construction and world collision physics.
  - `src/glitch/`: fake crash screen content plus transition/recovery state machine for the RPG ending.
  - `src/menus/`: menu screen payload definitions and game-flow controller for main/crash screens and transitions.
  - `src/audio/`: audio event engine and gameplay sound mappings.
  - `src/ui/`: shop wheel layout + controller logic for open/close, pause synchronization, and purchasing/equipping.
  - `src/hud/`: render-ready HUD state generation and transient damage/kill feedback timers.
  - `src/ai/`: bot runtime model, bot aiming variance helper, tactical decisions, and wave progression systems.
  - `src/environment/`: room/doorway/cover layout definitions plus collision/nav data builders.
  - `src/economy/`: money pickup entities, spawn/update/collect systems, and visual style definitions.
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
- Current economy progression curve: Shotgun `250`, AssaultRifle `800`, RPG `2000`.

## Implemented Gameplay Foundations
- `GameLoop.step(now)` advances time each frame and dispatches updates only while in `playing`.
- `GameClock` supports time scaling and pause/resume without losing wall-clock tracking.
- `GameStateManager` enforces valid transitions across `menu`, `playing`, `paused`, and `crashed`.
- `InputHandler.build_frame(...)` translates keyboard/mouse input into movement/look axes.
- `InputHandler.build_frame(...)` also emits one-shot `toggle_shop` actions for `B` key presses.
- `FirstPersonCamera` tracks yaw/pitch and clamps vertical look.
- `PlayerMovementController` applies yaw-relative movement and resolves AABB wall collisions with slide behavior.
- `RaycastingSystem` resolves nearest-target line traces for hit-scan shooting paths.
- `Player` enforces bounded health, game-over on death, validated currency operations, inventory ownership checks, weapon cycling, smooth timed switching, reload, projectile/hit-scan firing, and respawn.
- `Weapon` enforces cooldown/ammo, reload behavior, and projectile payload generation.
- `Pistol`, `Shotgun`, `AssaultRifle`, and `RPG` provide progression-ready weapon behavior; RPG toggles a crash trigger flag when fired.
- `glitch.build_fake_bsod_screen()` provides realistic crash text with explicit in-game recoverability messaging.
- `GlitchSequenceController` manages RPG-triggered transition effects (shake/distortion/static), crash-screen visibility, restart inputs (`Enter`/`Escape`/`R`), and emits phase-aligned crash audio cues.
- `GameFlowController` builds the main menu + crash ending screens, transitions to `crashed` during glitch phases, and returns to `menu` after recovery completion.
- `AudioEngine` tracks active sound events with per-event and per-channel stop controls.
- `SoundManager` defines and plays default profiles for weapon fire, movement, bot fire/death, money pickup, shop UI interactions, ambient facility hum, RPG pre-crash warning cue, and glitch sequence cues.
- `get_weapon_visual(...)` returns geometric primitive recipes for all progression weapons.
- `ProjectilePhysicsSystem` advances projectile motion and deactivates projectiles that hit walls or leave world bounds.
- `ShopWheelController` renders shop entry state (owned/equipped/affordable), toggles pause when opened, and enforces money checks for purchases.
- `Bot` supports health/state transitions, cooldown-aware shooting with accuracy variance, and money-drop spawning hooks.
- `ai.tactics` evaluates cover and picks `attack`/`take_cover`/`flank`, including side-approach flank routes.
- `ai.waves.WaveDirector` scales bot count and difficulty as waves progress.
- `WaypointPathfinder` computes nearest-waypoint BFS paths for baseline bot movement planning.
- `environment.create_default_facility_layout()` defines and validates a 5-room indoor map with doorways, cover, waypoints, bot/player spawns, and lighting values.
- `environment.build_collision_world(...)` transforms environment geometry into wall+cover collision AABBs.
- `environment.build_waypoint_pathfinder(...)` builds validated nav graphs from facility waypoint data.
- `MoneyPickupSystem` manages spawned money drops, pickup collisions, TTL expiration, and player-balance updates.
- `HudOverlayController` builds a single HUD payload and tracks timed damage/kill feedback effects.
- `HudEventRuntimeBridge` + `RuntimeSession` hook HUD damage/kill events into `GameLoop` update callbacks and expose frame-ready HUD state.
- `AudioEventRuntimeBridge` + `RuntimeSession` optionally queue and flush audio events only during active `playing` frames.

## Development Notes
- Keep gameplay constants in `config/config.py` until a richer configuration layer is needed.
- Add per-folder `developer-guide.md` files when new code folders gain implementation files.
