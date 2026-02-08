# Core Developer Guide

## Purpose
`src/core/` provides engine-level systems that are independent from rendering backends.

## Files
- `game_state.py`: `GameState` enum and `GameStateManager` with validated state transitions.
- `game_clock.py`: `GameClock` for frame delta-time and total elapsed time tracking.
- `input_handler.py`: `InputSnapshot` and `InputHandler` for WASD + mouse look normalization.
- `game_loop.py`: `GameLoop` that runs frame steps and calls update callbacks while in `playing`.
- `camera.py`: `FirstPersonCamera` yaw/pitch state with clamped vertical look limits.
- `collision.py`: AABB and `CollisionWorld` primitives for wall/bounds collision checks.
- `movement.py`: `PlayerMovementController` for yaw-relative movement with collision + slide resolution.

## Behavior Notes
- `GameStateManager` blocks invalid transitions with `ValueError`.
- `GameLoop.step(now)` always advances the clock, but only runs callbacks in `playing`.
- Mouse look is sensitivity-scaled and pitch is inverted (`mouse up` => positive look pitch).
- Camera pitch is clamped to avoid flipping.
- Movement uses local input (`WASD`) transformed by yaw into world-space direction.
- Movement checks full displacement first, then attempts axis-aligned slide fallback before stopping.
- `CollisionWorld.outside_world_bounds` checks full containment: returns `True` if any part of the box is outside world bounds.
