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
  - `cycle_weapon(direction)` supports next/previous switching through owned weapons.
  - Smooth transitions are available through `start_smooth_weapon_switch`, `start_smooth_cycle_weapon`, and `update_weapon_switch`.
- Combat logic:
  - `shoot(now)` delegates to the equipped weapon and consumes ammo only on successful shots.
  - `reload_weapon()` delegates magazine refill from reserve ammo.
  - `shoot_projectiles(...)` returns instantiated projectile entities for projectile simulation systems.
  - `shoot_hitscan(...)` performs a raycast-backed hit-scan shot and returns nearest hit metadata.
- Death/respawn logic:
  - Health reaching `0` marks `is_game_over=True`.
  - `shoot` is blocked while game over.
  - `respawn(spawn_position)` resets health and clears game-over state.
