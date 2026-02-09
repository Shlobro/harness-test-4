# Menus Developer Guide

## Purpose
`src/menus/` defines render-facing menu screen payloads and a lightweight game-flow coordinator for menu/crash/pause/game-over transitions.

## Files
- `screens.py`: immutable screen/action models plus builders for main menu, controls, pause, game over, and RPG crash ending screens.
- `controller.py`: `GameFlowController` that orchestrates `menu`/`controls`/`playing`/`paused`/`game_over`/`crashed` transitions, manages game-over stats, and handles generic menu actions.
- `__init__.py`: package exports.

## Behavior Summary
- Main menu payload includes a primary `start_game` action, a `controls` submenu action, and `quit`.
- Controls screen lists key bindings with a back action.
- Pause menu provides `resume_game` and `quit_to_menu` options.
- Game Over screen displays session stats (score, waves) with `restart_game` and `quit_to_menu` options.
- Crash ending payload wraps glitch BSOD lines into a dedicated `crash_ending` screen with a primary restart action.
- `GameFlowController.update(...)` advances glitch timing and transitions to `crashed` when appropriate.
- `GameFlowController.handle_menu_action(action_id)` processes UI events to drive state transitions.

## Integration Notes
- Call `handle_menu_action(action.action_id)` when the user interacts with a menu button.
- Call `toggle_pause()` when the user presses ESC during gameplay.
- Call `trigger_game_over(score, waves)` when the player dies (health <= 0).
- During runtime, call `update(...)` once per frame to manage glitch state.
- Use `get_active_screen(...)` to retrieve the current UI payload based on `GameState`.
