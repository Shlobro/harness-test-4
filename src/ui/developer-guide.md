# UI Developer Guide

## Purpose
`src/ui/` contains non-rendering UI logic for the in-game shop wheel.

## Files
- `shop_wheel.py`: radial shop layout, catalog definitions, open/close state control, pause synchronization, and purchase/equip interactions.
- `__init__.py`: package exports for shop wheel types and helpers.

## Core Concepts
- `ShopCatalogItem` defines a weapon listing with `weapon_name`, `price`, and a weapon factory.
- `default_shop_catalog()` provides progression store inventory:
  - Shotgun (`300`)
  - AssaultRifle (`900`)
  - RPG (`2500`)
- `ShopWheelLayout.build_entries(...)` converts catalog items into render-ready `ShopWheelEntry` objects with:
  - radial slot position (`angle_degrees`, `anchor_x`, `anchor_y`)
  - ownership state (`is_owned`)
  - equipped state (`is_equipped`)
  - affordability state (`can_afford`, `is_affordable_to_buy`)

## Interaction Flow
1. Input layer emits a shop toggle request (from `B` key edge detection).
2. `ShopWheelController.handle_input_frame(...)` toggles `is_open` when requested.
3. Opening the shop:
  - pauses `GameClock`
  - transitions game state from `playing` to `paused`
4. Closing the shop:
  - unpauses `GameClock`
  - transitions game state from `paused` to `playing`
5. `purchase_or_equip(...)` behavior:
  - Owned weapon: equip it.
  - Unowned weapon with enough money: spend price, instantiate weapon, add to inventory, auto-equip.
  - Unowned weapon without enough money: reject with `insufficient_funds`.
