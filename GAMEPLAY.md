# Gameplay And Controls

## Core Loop
1. Start with a pistol.
2. Fight bots and collect money drops.
3. Buy and switch to stronger weapons.
4. Reach RPG and fire it to trigger the glitch ending sequence.

## Controls
- `W`: move forward
- `A`: strafe left
- `S`: move backward
- `D`: strafe right
- `Mouse`: look/aim (first-person yaw + pitch)
- `Left Mouse` (planned runtime binding): shoot equipped weapon
- `R` (planned runtime binding): reload equipped weapon
- `B` (planned runtime binding): open inventory/shop wheel

## Weapon Progression
1. `Pistol`: starter, reliable semi-auto.
2. `Shotgun`: short-range burst with pellet spread.
3. `AssaultRifle`: rapid sustained fire.
4. `RPG`: high damage; firing triggers crash/glitch state.

## HUD Expectations
- Health
- Ammo (magazine + reserve)
- Money balance
- Crosshair

## Current Prototype Scope
The codebase currently provides backend gameplay systems (logic and tests). Full rendering/UI integration is the next layer on top of these modules.
