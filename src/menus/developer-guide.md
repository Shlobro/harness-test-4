# Menus Developer Guide

## Purpose
`src/menus/` defines render-facing menu screen payloads and a lightweight game-flow coordinator for menu/crash transitions.

## Files
- `screens.py`: immutable screen/action models plus builders for the main menu and RPG crash ending screen.
- `controller.py`: `GameFlowController` that orchestrates `menu`/`playing`/`paused`/`crashed` transitions, bridges crash-recovery key input to the glitch controller, and maps glitch audio cues to `SoundManager`.
- `__init__.py`: package exports.

## Behavior Summary
- Main menu payload includes a primary `start_game` action (`Start Arena Run`) and basic controls summary lines.
- Crash ending payload wraps glitch BSOD lines into a dedicated `crash_ending` screen with a primary restart action.
- `GameFlowController.update(...)` advances glitch timing each frame, transitions gameplay to `crashed` when glitch phases begin, and returns to `menu` after recovery cooldown completes.
- Optional glitch audio playback is handled by consuming queued `GlitchAudioCue` values and invoking dedicated glitch cue methods on `SoundManager`.

## Integration Notes
- Call `start_game()` from UI when the user chooses the start action on the main menu.
- During runtime, call `update(now=..., glitch_controller=..., sound_manager=...)` once per frame.
- Route restart key presses from crash screen through `handle_crash_recovery_input(...)`.
