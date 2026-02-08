# Recent Changes

- Implemented HUD runtime event integration via `src/core/runtime.py`:
  - Added `HudEventRuntimeBridge` to queue damage/kill events and flush them during `GameLoop` playing-frame callbacks.
  - Added `RuntimeSession` to compose `Player`, `GameLoop`, and HUD hooks (`apply_player_damage`, `register_bot_kill`, `build_hud_state`).
  - Exported new runtime types from `src/core/__init__.py`.
- Expanded environment completeness in `src/environment/facility.py`:
  - Added explicit doorway connectivity graph traversal (`doorway_graph`, `connected_room_ids`).
  - Added room lookup helper for positions (`find_room_for_position`).
  - Added lighting vector helper (`lighting_direction_length`).
  - Added layout validation for doorway references/widths, spawn presence/placement, lighting sanity, and room validity.
  - `create_default_facility_layout()` now validates before returning.
- Added targeted complex-algorithm comments:
  - Doorway wall-segment splitting in `src/environment/collision.py`.
  - Segment-projection geometry in `src/ai/tactics.py`.
- Strengthened tests:
  - `tests/test_core_systems.py` now verifies runtime HUD damage/kill hooks only apply on `playing` frames.
  - `tests/test_environment_and_tactics.py` now verifies full room connectivity, spawn positions inside rooms, and lighting validity.
- Verified documentation/codebase constraints:
  - No `developer-guide.md` file exceeds 500 lines.
  - No Python code file exceeds 1000 lines.
  - No folder contains more than 10 Python code files.
- Updated relevant developer guides after folder changes:
  - `src/core/developer-guide.md`
  - `src/environment/developer-guide.md`
  - `src/ai/developer-guide.md`
  - `src/developer-guide.md`
  - `tests/developer-guide.md`
  - `developer-guide.md`

