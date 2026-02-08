# Weapons Developer Guide

## Purpose
`src/weapons/` defines weapon behavior shared across loadout items.

## Files
- `weapon.py`: base `Weapon` dataclass with ammo, fire-rate cooldown, and firing logic.
- `pistol.py`: starter `Pistol` implementation with tuned default stats.
- `shotgun.py`: close-range spread weapon with multi-pellet projectile payload.
- `assault_rifle.py`: rapid-fire automatic weapon with larger magazine.
- `rpg.py`: rocket launcher that sets a crash trigger flag when fired.

## Key Behaviors
- `Weapon.fire(now)` returns `True` only when:
  - ammo remains in the magazine, and
  - cooldown time since last shot has elapsed.
- Successful fire events decrement `ammo_in_magazine` by exactly one.
- `Weapon.reload()` transfers reserve ammo into the magazine and returns rounds loaded.
- `Weapon.create_projectile_payload(...)` produces normalized projectile spawn payload consumed by the projectile system.
- `Pistol` defaults:
  - damage `20`
  - fire rate `3` shots/sec
  - magazine size `12`
  - reserve ammo `48`
