# Glitch Developer Guide

## Purpose
`src/glitch/` implements the fake crash ending that is triggered by firing the RPG.

## Files
- `bsod.py`: fake BSOD content model and message builder. It provides realistic crash text, mockup styling fields (colors/support URL/progress text), and an explicit recoverability hint.
- `sequence.py`: glitch timeline state machine with phases (`idle`, `transition`, `crash_screen`, `recovering`), pre-crash visual effect values, RPG trigger consumption, restart flow, and phase-based audio cue emission.
- `__init__.py`: package exports.

## Behavior Summary
- `build_fake_bsod_screen()` returns structured crash text that looks system-like but clearly states it is an in-game simulation.
- `GlitchSequenceController.trigger_from_weapon(...)` detects and consumes `crash_triggered` from RPG-like weapons.
- Transition effects ramp up during `transition` and max out in `crash_screen`.
- Recovery starts with `request_recover(...)` using `Enter`, `Escape`, or `R`.
- Recovery completes after cooldown via `complete_recovery_if_ready(...)`, returning the sequence to `idle`.
- `consume_audio_cues()` returns ordered cue intents (`transition_ramp`, `crash_impact`, `recovery_confirm`) for external audio playback mapping.

## Integration Notes
- Call `trigger_from_weapon(...)` after weapon fire resolution.
- Call `update(now)` each frame to get render-facing effect values.
- While `should_lock_gameplay` is true, normal gameplay input should be ignored.
- Route `consume_audio_cues()` to `SoundManager` glitch cue playback so crash-sequence audio stays phase-aligned.
