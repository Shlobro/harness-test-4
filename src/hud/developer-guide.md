# HUD Developer Guide

## Purpose
`src/hud/` contains engine-agnostic HUD state generation and short-lived feedback systems.

## Files
- `overlay.py`: HUD domain models and `HudOverlayController` for health/ammo/money/crosshair rendering payloads, damage flash timing, and kill notifications/counter.
- `__init__.py`: package exports for HUD state/controller types.

## Core Behaviors
- `HudOverlayController.build_state(player)` returns one render-ready payload with:
  - health bar data (`current_health`, `max_health`, `fill_ratio`, severity color)
  - ammo data (`weapon_name`, `in_magazine`, `magazine_size`, `reserve_ammo`, formatted text)
  - money display text
  - center-screen crosshair style and placement
  - damage indicator visibility/intensity/alpha countdown values
  - kill counter and active kill notifications
- `register_damage(amount)` triggers or refreshes the damage indicator flash.
- `register_kill(enemy_label)` increments kill count and adds a short-lived kill notification.
- `step(delta_time)` advances timers and expires transient damage/notification effects.

## Integration Notes
- Keep this module rendering-agnostic: platform/UI layers should only consume `HudOverlayState`.
- Call `step(...)` once per frame and `build_state(...)` when preparing HUD draw data.
- Hook `register_damage(...)` to player damage events and `register_kill(...)` to bot death events.
