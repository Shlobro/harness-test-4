# Src Developer Guide

## Purpose
`src/` contains the game runtime modules for loop/state management, player logic, and weapons.

## Folder Overview
- `core/`: frame stepping, game clock, state machine, and input normalization.
- `player/`: player runtime model (health, money, inventory, equipped weapon, shooting).
- `weapons/`: reusable weapon abstractions and concrete weapon implementations.

## Integration Flow
1. The platform layer collects raw input and passes it to `core.input_handler.InputHandler`.
2. The game loop (`core.game_loop.GameLoop`) advances time using `core.game_clock.GameClock`.
3. When in `playing` state, registered update callbacks apply gameplay changes each frame.
4. Player actions call into weapon models for ammo/cooldown-validated firing.

