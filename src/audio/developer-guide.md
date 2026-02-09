# Audio Developer Guide

## Purpose
`src/audio/` provides a backend-agnostic audio layer for gameplay events.

## Files
- `engine.py`: lightweight audio event engine that tracks active sounds, supports play/stop, and supports channel-wide stops.
- `sound_manager.py`: high-level event mapping. It defines placeholder procedural profiles and playback APIs for weapon fire, footsteps, bot combat/death, money pickup, shop UI interactions, ambient facility loop audio, RPG pre-crash warning cue, and glitch-sequence crash cues.
- `__init__.py`: package exports.

## Behavior Summary
- `AudioEngine` generates stable event IDs and stores active events as plain data, making integration and tests deterministic.
- `SoundManager` ships default procedural profiles for:
  - weapon shots (`Pistol`, `Shotgun`, `AssaultRifle`, `RPG`)
  - movement (`footstep_walk`, `footstep_run`)
  - enemy events (`bot_shot`, `bot_death`)
  - economy (`money_pickup`)
  - UI events (`shop_open`, `shop_close`, `purchase_success`, `purchase_fail`)
  - ambient loop (`ambient_facility_hum`)
  - RPG pre-crash cue (`rpg_pre_crash_warning`)
  - glitch sequence cues (`glitch_transition_ramp`, `glitch_crash_impact`, `glitch_recovery_confirm`)
- `play_weapon_fire("RPG")` plays the pre-crash warning cue and then the RPG shot.
- Ambient playback is idempotent: repeated `start_ambient_facility()` returns the same active loop event until stopped.
- Dedicated glitch methods (`play_glitch_transition_cue`, `play_glitch_crash_impact_cue`, `play_glitch_recovery_cue`) are used by flow controllers that consume glitch phase cues.

## Integration Notes
- Replace `ProceduralSoundProfile` entries with real asset-backed profiles later without changing gameplay call sites.
- Route gameplay events through the dedicated methods (`play_weapon_fire`, `play_footstep`, `play_bot_fire`, `play_bot_death`, `play_money_pickup`, `play_ui_event`, `start_ambient_facility`, `stop_ambient_facility`).
