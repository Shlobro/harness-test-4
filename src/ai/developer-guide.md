# AI Developer Guide

## Purpose
`src/ai/` contains bot runtime behavior, bot aiming logic, tactical decision logic, waypoint pathfinding, and wave management.

## Files
- `bot.py`: `Bot` model with health/state, damage/death flow, inaccuracy-aware shooting, and money-drop spawning.
- `combat.py`: deterministic helper for applying directional aim variance from an accuracy cone.
- `navigation.py`: `WaypointPathfinder` for nearest-waypoint BFS path generation.
- `tactics.py`: cover evaluation, tactical action selection (`attack`, `take_cover`, `flank`), and flank route construction.
- `waves.py`: wave size scaling, per-wave difficulty profiles, and deterministic bot spawning.
- `__init__.py`: package exports for AI modules.

## Key Behaviors
- `Bot.create_default(...)` creates a standard bot with assault rifle loadout.
- `Bot.apply_damage(...)` clamps health and sets state to `dead` on kill.
- `Bot.shoot_at(...)` computes normalized target direction, applies accuracy variance, and respects weapon cooldown/ammo.
- `Bot.spawn_money_drop(...)` emits a `MoneyPickup` through `MoneyPickupSystem` and is allowed only after death.
- `WaypointPathfinder.find_path(...)` maps world positions to nearest waypoints and returns a connected path using BFS over waypoint links.
- `find_cover_plan(...)` finds nearest usable cover that can break line-of-fire from player to bot.
- `choose_tactical_action(...)` decides between `attack`, `take_cover`, and `flank` based on health, distance, allies, and available cover. Raises `ValueError` if called on a dead bot; callers must filter dead bots before calling.
- `build_flank_route(...)` returns side-approach points so bots can pressure from multiple angles.
- `WaveDirector` scales bot count and difficulty per wave and spawns wave bots at provided spawn positions.
