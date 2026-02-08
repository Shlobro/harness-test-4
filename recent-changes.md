# Recent Changes

## 2026-02-08
- Added `src/ai/` with a `Bot` runtime model, AI state enum, accuracy-variance shooting helpers, and waypoint-based pathfinding.
- Added bot death money-drop spawning integration through a new economy pickup system.
- Added `src/economy/` with `MoneyPickup`, pickup visuals (glowing cube/sphere), collision checks, TTL handling, spawn tracking, and player collection/balance updates.
- Added `tests/test_ai_and_economy.py` to validate bot health/state, pathfinding, shooting variance, money drops, pickup collision, visual mapping, and collection flow.
- Updated developer guides in `src/ai/`, `src/economy/`, `src/`, root, and `tests/` to document the new systems.

