import pytest

from src.core.game_clock import GameClock
from src.core.game_state import GameState, GameStateManager
from src.core.input_handler import InputHandler, InputSnapshot
from src.player.player import Player
from src.ui.shop_wheel import ShopWheelController


def test_shop_wheel_layout_distributes_entries_radially_with_prices():
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    controller = ShopWheelController()

    entries = controller.get_entries(player)
    assert [entry.weapon_name for entry in entries] == ["Shotgun", "AssaultRifle", "RPG"]
    assert [entry.price for entry in entries] == [300, 900, 2500]
    assert [entry.slot_index for entry in entries] == [0, 1, 2]
    assert [entry.angle_degrees for entry in entries] == pytest.approx([-90.0, 30.0, 150.0])


def test_b_key_toggle_opens_and_closes_shop_wheel_once_per_press():
    handler = InputHandler(mouse_sensitivity=1.0)
    manager = GameStateManager()
    manager.transition_to(GameState.PLAYING)
    clock = GameClock()
    clock.tick(0.0)
    controller = ShopWheelController()

    first_press = handler.build_frame(InputSnapshot(pressed_keys={"b"}))
    assert first_press.toggle_shop is True
    assert (
        controller.handle_input_frame(
            toggle_shop_requested=first_press.toggle_shop,
            game_state_manager=manager,
            game_clock=clock,
        )
        is True
    )

    held_press = handler.build_frame(InputSnapshot(pressed_keys={"b"}))
    assert held_press.toggle_shop is False
    assert (
        controller.handle_input_frame(
            toggle_shop_requested=held_press.toggle_shop,
            game_state_manager=manager,
            game_clock=clock,
        )
        is True
    )

    handler.build_frame(InputSnapshot(pressed_keys=set()))
    second_press = handler.build_frame(InputSnapshot(pressed_keys={"b"}))
    assert second_press.toggle_shop is True
    assert (
        controller.handle_input_frame(
            toggle_shop_requested=second_press.toggle_shop,
            game_state_manager=manager,
            game_clock=clock,
        )
        is False
    )


def test_open_shop_pauses_time_and_moves_state_to_paused_then_resumes():
    manager = GameStateManager()
    manager.transition_to(GameState.PLAYING)
    clock = GameClock()
    clock.tick(1.0)
    controller = ShopWheelController()

    controller.handle_shop_toggle(game_state_manager=manager, game_clock=clock)
    assert controller.is_open is True
    assert manager.current_state == GameState.PAUSED
    assert clock.is_paused is True

    delta = clock.tick(2.0)
    assert delta == 0.0

    controller.handle_shop_toggle(game_state_manager=manager, game_clock=clock)
    assert controller.is_open is False
    assert manager.current_state == GameState.PLAYING
    assert clock.is_paused is False


def test_shop_entries_show_affordability_ownership_and_equipped_flags():
    player = Player.with_starter_loadout(start_health=100, start_money=850)
    controller = ShopWheelController()
    controller.purchase_or_equip(player=player, weapon_name="Shotgun")

    entries = {entry.weapon_name: entry for entry in controller.get_entries(player)}
    assert entries["Shotgun"].is_owned is True
    assert entries["Shotgun"].is_equipped is True
    assert entries["Shotgun"].can_afford is True
    assert entries["Shotgun"].is_affordable_to_buy is False
    assert entries["AssaultRifle"].can_afford is False
    assert entries["AssaultRifle"].is_affordable_to_buy is False
    assert entries["RPG"].can_afford is False


def test_purchase_logic_buys_when_affordable_and_rejects_otherwise():
    player = Player.with_starter_loadout(start_health=100, start_money=350)
    controller = ShopWheelController()

    shotgun_result = controller.purchase_or_equip(player=player, weapon_name="Shotgun")
    assert shotgun_result.success is True
    assert shotgun_result.action == "purchased"
    assert shotgun_result.amount_spent == 300
    assert player.money == 50
    assert "Shotgun" in player.inventory
    assert player.equipped_weapon_name == "Shotgun"

    rpg_result = controller.purchase_or_equip(player=player, weapon_name="RPG")
    assert rpg_result.success is False
    assert rpg_result.reason == "insufficient_funds"
    assert "RPG" not in player.inventory


def test_shop_selection_equips_owned_weapon_from_inventory():
    player = Player.with_starter_loadout(start_health=100, start_money=2000)
    controller = ShopWheelController()
    controller.purchase_or_equip(player=player, weapon_name="Shotgun")
    controller.purchase_or_equip(player=player, weapon_name="AssaultRifle")
    assert player.equipped_weapon_name == "AssaultRifle"

    equip_result = controller.purchase_or_equip(player=player, weapon_name="Shotgun")
    assert equip_result.success is True
    assert equip_result.action == "equipped"
    assert player.equipped_weapon_name == "Shotgun"
