# Core Developer Guide

## Purpose
`src/core/` provides engine-level systems that are independent from rendering backends.

## Files
- `game_state.py`: `GameState` enum and `GameStateManager` with validated state transitions.
- `game_clock.py`: `GameClock` for frame delta-time, pause/resume, time scaling, and elapsed time tracking.
- `input_handler.py`: `InputSnapshot` and `InputHandler` for WASD + mouse look normalization.
- `game_loop.py`: `GameLoop` that runs frame steps and calls update callbacks while in `playing`.
- `camera.py`: `FirstPersonCamera` yaw/pitch state with clamped vertical look limits.
- `collision.py`: AABB and `CollisionWorld` primitives for wall/bounds collision checks.
- `movement.py`: `PlayerMovementController` for yaw-relative movement with collision + slide resolution.
- `raycasting.py`: `RaycastingSystem` with nearest-hit line traces against spherical targets for hit-scan shooting.
- `runtime.py`: runtime composition helpers that wire HUD events and queued audio events into `GameLoop` frame updates.

## Behavior Notes
- `GameStateManager` blocks invalid transitions with `ValueError`.
- Allowed transitions include:
  - `PAUSED` → `PLAYING` (resume gameplay)
  - `PAUSED` → `GAME_OVER` (player died while paused/shopping)
  - `PAUSED` → `MENU` (quit from pause)
- `GameLoop.step(now)` always advances the clock, but only runs callbacks in `playing`.
- `GameClock` supports paused time and positive time-scale multipliers for slowed/accelerated simulation.
- Mouse look is sensitivity-scaled and pitch is inverted (`mouse up` => positive look pitch).
- Input frames include `toggle_shop`, triggered only on `B` key press edges (held key does not retrigger).
- Camera pitch is clamped to avoid flipping.
- Movement uses local input (`WASD`) transformed by yaw into world-space direction.
- Movement checks full displacement first, then attempts axis-aligned slide fallback before stopping.
- `CollisionWorld.outside_world_bounds` checks full containment: returns `True` if any part of the box is outside world bounds.
- `RaycastingSystem.cast_ray(...)` returns the closest valid target hit (or `None`) within max distance.
- `HudEventRuntimeBridge` queues damage/kill events and flushes them only on active `playing` frames.
- `AudioEventRuntimeBridge` queues gameplay audio intents (weapon fire, footsteps, bot fire/death, money pickup, ambient start/stop) and flushes them only on active `playing` frames. UI audio events are played immediately regardless of game state to ensure responsive UI feedback.
- `RuntimeSession` provides a minimal player runtime wrapper for HUD + optional audio integration, exposing helper APIs for damage/kill HUD hooks and audio event registration.
