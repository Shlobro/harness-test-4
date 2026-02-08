import pytest

from src.hud import HudOverlayController
from src.player.player import Player


def test_hud_overlay_core_displays_health_ammo_money_and_crosshair():
    player = Player.with_starter_loadout(start_health=100, start_money=425)
    hud = HudOverlayController()

    state = hud.build_state(player)
    assert state.health.current_health == 100
    assert state.health.max_health == 100
    assert state.health.fill_ratio == pytest.approx(1.0)
    assert state.health.color == "green"

    assert state.ammo.weapon_name == "Pistol"
    assert state.ammo.in_magazine == 12
    assert state.ammo.magazine_size == 12
    assert state.ammo.reserve_ammo == 48
    assert state.ammo.display_text == "12/12 | 48"

    assert state.money.amount == 425
    assert state.money.display_text == "$425"

    assert state.crosshair.center_x == pytest.approx(0.5)
    assert state.crosshair.center_y == pytest.approx(0.5)
    assert state.crosshair.size == pytest.approx(16.0)
    assert state.crosshair.color == "white"


def test_hud_health_bar_colors_track_damage_levels():
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    hud = HudOverlayController()

    player.apply_damage(55)
    mid_state = hud.build_state(player)
    assert mid_state.health.fill_ratio == pytest.approx(0.45)
    assert mid_state.health.color == "yellow"

    player.apply_damage(25)
    low_state = hud.build_state(player)
    assert low_state.health.fill_ratio == pytest.approx(0.20)
    assert low_state.health.color == "red"


def test_hud_damage_indicator_shows_then_fades_with_step():
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    hud = HudOverlayController(damage_flash_seconds=0.5)

    hud.register_damage(30)
    state = hud.build_state(player)
    assert state.damage_indicator.is_visible is True
    assert state.damage_indicator.alpha > 0.0
    assert state.damage_indicator.intensity == pytest.approx(0.5)

    hud.step(0.25)
    half_state = hud.build_state(player)
    assert half_state.damage_indicator.is_visible is True
    assert half_state.damage_indicator.alpha < state.damage_indicator.alpha

    hud.step(0.25)
    final_state = hud.build_state(player)
    assert final_state.damage_indicator.is_visible is False
    assert final_state.damage_indicator.alpha == pytest.approx(0.0)


def test_hud_kill_counter_and_notifications_are_tracked_and_expire():
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    hud = HudOverlayController(kill_notification_seconds=1.5, max_notifications=2)

    hud.register_kill("Bot Alpha")
    hud.register_kill("Bot Beta")
    hud.register_kill("Bot Gamma")

    state = hud.build_state(player)
    assert state.kill_count == 3
    assert [note.message for note in state.kill_notifications] == [
        "Bot Gamma eliminated",
        "Bot Beta eliminated",
    ]

    hud.step(1.5)
    expired_state = hud.build_state(player)
    assert expired_state.kill_count == 3
    assert expired_state.kill_notifications == []


def test_hud_damage_rejects_non_positive_amounts():
    hud = HudOverlayController()
    with pytest.raises(ValueError):
        hud.register_damage(0)
