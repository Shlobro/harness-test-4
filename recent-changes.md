# Recent Changes

- Added a new `src/hud/` module with `HudOverlayController` and render-ready HUD state models for health bar, ammo counter, money display, center crosshair, damage indicator, and kill notifications/counter.
- Added `tests/test_hud.py` to validate core HUD behavior, damage flash timing, and kill feed lifecycle.
- Rebalanced economy progression prices in `config/config.py` to Shotgun `250`, AssaultRifle `800`, RPG `2000`, and updated affected tests/docs.
- Updated developer guides in `developer-guide.md`, `src/developer-guide.md`, `src/ui/developer-guide.md`, `config/developer-guide.md`, and `tests/developer-guide.md` to reflect the new HUD system and economy curve.

