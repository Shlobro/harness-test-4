import pytest

from src.player.player import Player
from src.weapons.pistol import Pistol
from src.weapons.weapon import Weapon


def test_player_starter_loadout_and_properties():
    player = Player.with_starter_loadout(start_health=100, start_money=0)

    assert player.health == 100
    assert player.money == 0
    assert player.position == (0.0, 1.8, 0.0)
    assert player.rotation == (0.0, 0.0)
    assert player.equipped_weapon_name == "Pistol"
    assert isinstance(player.equipped_weapon, Pistol)


def test_player_health_system_damage_heal_and_death():
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    player.apply_damage(30)
    assert player.health == 70
    assert player.is_alive

    player.apply_damage(1000)
    assert player.health == 0
    assert not player.is_alive

    player.heal(10)
    assert player.health == 10

    with pytest.raises(ValueError):
        player.apply_damage(-1)
    with pytest.raises(ValueError):
        player.heal(-1)


def test_player_money_tracking_and_spend_validation():
    player = Player.with_starter_loadout(start_health=100, start_money=50)

    player.add_money(25)
    assert player.money == 75

    assert player.spend_money(70) is True
    assert player.money == 5
    assert player.spend_money(6) is False
    assert player.money == 5

    with pytest.raises(ValueError):
        player.add_money(-1)
    with pytest.raises(ValueError):
        player.spend_money(-1)


def test_player_inventory_tracking_and_equipping():
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    custom_weapon = Weapon(
        name="TestGun",
        damage=5,
        fire_rate=5,
        magazine_size=2,
        reserve_ammo=0,
    )

    player.add_weapon(custom_weapon)
    player.equip_weapon("TestGun")
    assert player.equipped_weapon_name == "TestGun"

    with pytest.raises(ValueError):
        player.equip_weapon("MissingWeapon")


def test_player_position_and_rotation_setters():
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    
    player.set_position(10.0, 5.0, -10.0)
    assert player.position == (10.0, 5.0, -10.0)

    player.set_rotation(90.0, -45.0)
    assert player.rotation == (90.0, -45.0)


def test_base_weapon_fire_rate_and_ammo_consumption():
    weapon = Weapon(
        name="BaseWeapon",
        damage=10,
        fire_rate=2,
        magazine_size=2,
        reserve_ammo=0,
    )
    assert weapon.ammo_in_magazine == 2

    assert weapon.fire(1.0) is True
    assert weapon.ammo_in_magazine == 1
    assert weapon.fire(1.2) is False
    assert weapon.fire(1.5) is True
    assert weapon.ammo_in_magazine == 0
    assert weapon.fire(2.5) is False


def test_pistol_defaults_and_player_shooting_behavior():
    pistol = Pistol()
    assert pistol.name == "Pistol"
    assert pistol.damage == 20.0
    assert pistol.fire_rate == 3.0
    assert pistol.magazine_size == 12
    assert pistol.reserve_ammo == 48

    player = Player.with_starter_loadout(start_health=100, start_money=0)
    assert player.shoot(1.0) is True
    assert player.equipped_weapon.ammo_in_magazine == 11
    assert player.shoot(1.1) is False

    player.apply_damage(100)
    assert player.shoot(2.0) is False

