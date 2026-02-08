# AI Developer Guide

## Purpose
`src/ai/` contains bot runtime behavior, bot aiming logic, and waypoint pathfinding.

## Files
- `bot.py`: `Bot` model with health/state, damage/death flow, inaccuracy-aware shooting, and money-drop spawning.
- `combat.py`: deterministic helper for applying directional aim variance from an accuracy cone.
- `navigation.py`: `WaypointPathfinder` for nearest-waypoint BFS path generation.
- `__init__.py`: package exports for AI modules.

## Key Behaviors
- `Bot.create_default(...)` creates a standard bot with assault rifle loadout.
- `Bot.apply_damage(...)` clamps health and sets state to `dead` on kill.
- `Bot.shoot_at(...)` computes normalized target direction, applies accuracy variance, and respects weapon cooldown/ammo.
- `Bot.spawn_money_drop(...)` emits a `MoneyPickup` through `MoneyPickupSystem` and is allowed only after death.
- `WaypointPathfinder.find_path(...)` maps world positions to nearest waypoints and returns a connected path using BFS over waypoint links.
