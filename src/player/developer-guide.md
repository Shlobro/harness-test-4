# Player Developer Guide

## Purpose
`src/player/` owns all player-centric gameplay state and actions.

## Files
- `player.py`: `Player` dataclass with health, money, transform state, inventory, and firing API.

## Key Behaviors
- `Player.with_starter_loadout(...)` spawns a player with a default `Pistol`.
- Health logic:
  - `apply_damage` clamps health at `0`.
  - `heal` clamps health at `max_health`.
  - `is_alive` becomes `False` at `0` health.
- Economy logic:
  - `add_money` and `spend_money` reject negative inputs.
  - `spend_money` returns `False` when balance is insufficient.
- Inventory logic:
  - Weapons are stored by name.
  - `equip_weapon` requires ownership.
- Combat logic:
  - `shoot(now)` delegates to the equipped weapon and consumes ammo only on successful shots.

