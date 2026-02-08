# Weapons Developer Guide

## Purpose
`src/weapons/` defines weapon behavior shared across loadout items.

## Files
- `weapon.py`: base `Weapon` dataclass with ammo, fire-rate cooldown, and firing logic.
- `pistol.py`: starter `Pistol` implementation with tuned default stats.

## Key Behaviors
- `Weapon.fire(now)` returns `True` only when:
  - ammo remains in the magazine, and
  - cooldown time since last shot has elapsed.
- Successful fire events decrement `ammo_in_magazine` by exactly one.
- `Pistol` defaults:
  - damage `20`
  - fire rate `3` shots/sec
  - magazine size `12`
  - reserve ammo `48`

