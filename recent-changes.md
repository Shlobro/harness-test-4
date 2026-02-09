# Recent Changes

## 2026-02-09

### UI/UX Review Fixes (Crash Flow)
- Fixed premature crash screen display during transition phase:
  - Removed `GlitchPhase.TRANSITION` from the state-transition check in `src/menus/controller.py:62`
  - Now only transitions to `GameState.CRASHED` when glitch phase is `CRASH_SCREEN` or `RECOVERING`
  - This allows the transition visual effects to complete before displaying the crash-ending screen, preventing abrupt UI jumps
- Standardized restart key instructions across crash UI flow:
  - Updated `src/glitch/bsod.py:57` to say "Press ENTER, ESC, or R" (was missing R)
  - Updated `src/menus/screens.py:68` to use consistent capitalization: "Press ENTER, ESC, or R"
  - All three locations (`bsod.py`, `screens.py`, `sequence.py`) now document the same recovery keys with consistent formatting

## Earlier on 2026-02-09

### Glitch Sequence and Game Flow Completion
- Completed 10 previously incomplete tasks across glitch and game-flow systems:
  - Designed and expanded fake BSOD mockup payload in `src/glitch/bsod.py` with visual-style fields (`background_hex`, `text_hex`), support URL text, and progress text while preserving explicit recoverability messaging.
  - Finalized RPG-triggered transition and pre-crash visual effect behavior in `src/glitch/sequence.py` (transition -> crash_screen -> recovering -> idle).
  - Added ordered crash-lifecycle audio cue intents in `GlitchSequenceController` via `GlitchAudioCue` and `consume_audio_cues()`.
  - Implemented dedicated crash-sequence audio playback methods in `src/audio/sound_manager.py`:
    - `play_glitch_transition_cue()`
    - `play_glitch_crash_impact_cue()`
    - `play_glitch_recovery_cue()`
  - Added `src/menus/` module:
    - `screens.py` for `build_main_menu_screen()` (with primary start action) and `build_crash_ending_screen()` payloads.
    - `controller.py` for `GameFlowController` state orchestration and glitch recovery input handling.
    - `__init__.py` package exports and `developer-guide.md`.
  - Implemented glitch-driven game-state transitions to `crashed` and back to `menu` after recovery completion through `GameFlowController.update(...)`.
- Added/updated automated coverage:
  - `tests/test_glitch_and_audio.py`:
    - fake BSOD mockup metadata/content assertions
    - glitch audio cue ordering assertions
    - glitch cue playback assertions in sound manager
  - `tests/test_core_systems.py`:
    - main menu start-action assertions
    - crash ending screen and restart-action assertions
    - end-to-end game-flow transition test (`menu` -> `playing` -> `crashed` -> `menu`)
- Updated developer documentation for touched folders and ancestors:
  - `src/glitch/developer-guide.md`
  - `src/audio/developer-guide.md`
  - `src/menus/developer-guide.md` (new)
  - `src/developer-guide.md`
  - `tests/developer-guide.md`
  - `developer-guide.md`

## 2026-02-08

### UI/UX Review Fixes
- Fixed UI audio timing issue where shop open/close sounds were delayed or missing:
  - Changed `AudioEventRuntimeBridge.queue_ui_event()` to `play_ui_event_immediate()` to play UI sounds immediately regardless of game state
  - Removed `_pending_ui_events` queue since UI audio no longer needs to be deferred
  - Updated `RuntimeSession.register_ui_audio()` to call immediate playback instead of queueing
  - Updated test `test_runtime_session_routes_audio_events_during_playing_frames` to verify UI audio plays immediately while other gameplay audio remains queued
  - This ensures responsive UI feedback even when game is paused (e.g., when shop wheel is open)
- Updated `src/core/developer-guide.md` to document immediate UI audio playback behavior

## Earlier on 2026-02-08
- Fixed code review issues from general.md review:
  - Corrected `recent-changes.md:5` to remove false claim about reverting audio system completion marks (audio system is actually completed and should remain checked)
  - Untracked `.agentharness/` directory and `.codex_last_message.txt` from git to make `.gitignore` rules effective (previously these were already tracked, so the ignore rule had no effect)
  - Updated `recent-changes.md:7` to clarify that already-tracked files need manual untracking for gitignore to work
- Fixed code review issues in general.md:
  - Reverted premature completion marks in `tasks.md` for glitch system tasks that were documented but not yet committed
  - Reverted premature implementation claims in `recent-changes.md` for uncommitted glitch/audio subsystems and tests
  - Added `.agentharness/` and `.codex_last_message.txt` to `.gitignore` (note: already-tracked files need manual untracking)
- Updated architecture documentation in:
  - `src/developer-guide.md`
  - `developer-guide.md`
  - `tests/developer-guide.md`
- Completed and validated runtime HUD/audio integration tasks:
  - Confirmed HUD runtime event-hook integration (`HudEventRuntimeBridge` + `RuntimeSession`) is active in the update loop and validated via tests
  - Expanded `SoundManager` with procedural profiles and playback APIs for footsteps, bot fire/death, money pickup, shop UI events, ambient facility loop, and RPG pre-crash warning cue
  - Added `AudioEventRuntimeBridge` and optional `RuntimeSession` audio APIs to queue audio intents and flush playback only during active `playing` frames
  - Added/updated automated coverage in `tests/test_glitch_and_audio.py` and `tests/test_core_systems.py` for expanded audio events, RPG cue ordering, ambient lifecycle, and runtime playback gating
- Updated developer documentation for audio/runtime behavior in:
  - `src/audio/developer-guide.md`
  - `src/core/developer-guide.md`
  - `src/developer-guide.md`
  - `developer-guide.md`
  - `tests/developer-guide.md`
