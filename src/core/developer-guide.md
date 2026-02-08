# Core Developer Guide

## Purpose
`src/core/` provides engine-level systems that are independent from rendering backends.

## Files
- `game_state.py`: `GameState` enum and `GameStateManager` with validated state transitions.
- `game_clock.py`: `GameClock` for frame delta-time and total elapsed time tracking.
- `input_handler.py`: `InputSnapshot` and `InputHandler` for WASD + mouse look normalization.
- `game_loop.py`: `GameLoop` that runs frame steps and calls update callbacks while in `playing`.

## Behavior Notes
- `GameStateManager` blocks invalid transitions with `ValueError`.
- `GameLoop.step(now)` always advances the clock, but only runs callbacks in `playing`.
- Mouse look is sensitivity-scaled and pitch is inverted (`mouse up` => positive look pitch).

