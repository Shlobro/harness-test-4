# Economy Developer Guide

## Purpose
`src/economy/` models world money drops, pickup visuals, collision checks, and player collection.

## Files
- `money.py`: money pickup entity, visual definitions, spawn/update lifecycle, and collection system.
- `__init__.py`: package exports for economy modules.

## Key Behaviors
- `MoneyPickupSystem.spawn_pickup(...)` creates uniquely identified pickups with primitive visual definitions.
- `MoneyPickup.intersects_sphere(...)` handles pickup collision checks against player pickup radius.
- `MoneyPickupSystem.collect_for_player(...)` transfers money to the player when collisions occur and removes collected pickups.
- `MoneyPickup.step(...)` supports TTL expiration; expired pickups are removed during `MoneyPickupSystem.step(...)`.
- `get_money_pickup_visual(amount)` returns a glowing cube for smaller amounts and glowing sphere for larger drops.
