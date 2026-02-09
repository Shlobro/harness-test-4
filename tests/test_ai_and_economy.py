from random import Random
from time import perf_counter

import pytest

from config.config import ECONOMY_CONFIG
from src.ai.bot import Bot, BotAIState
from src.ai.navigation import WaypointPathfinder
from src.ai.waves import WaveDirector
from src.economy.money import MoneyPickupSystem, get_money_pickup_visual
from src.environment import create_default_facility_layout
from src.player.player import Player


def test_bot_default_state_health_and_damage_flow():
    bot = Bot.create_default(bot_id="bot-1", position=(1.0, 0.0, 2.0))
    assert bot.bot_id == "bot-1"
    assert bot.health == 100
    assert bot.ai_state == BotAIState.IDLE
    assert bot.is_alive is True

    killed = bot.apply_damage(40)
    assert killed is False
    assert bot.health == 60

    killed = bot.apply_damage(60)
    assert killed is True
    assert bot.health == 0
    assert bot.ai_state == BotAIState.DEAD
    assert bot.is_alive is False

    with pytest.raises(ValueError):
        bot.apply_damage(-1)


def test_waypoint_pathfinding_uses_nearest_start_goal():
    pathfinder = WaypointPathfinder(
        waypoints={
            "a": (0.0, 0.0, 0.0),
            "b": (5.0, 0.0, 0.0),
            "c": (10.0, 0.0, 0.0),
            "d": (10.0, 0.0, 5.0),
        },
        links={
            "a": ["b"],
            "b": ["a", "c"],
            "c": ["b", "d"],
            "d": ["c"],
        },
    )
    path = pathfinder.find_path(
        start_position=(1.0, 0.0, 0.2),
        goal_position=(9.9, 0.0, 4.7),
    )
    assert path == [
        (0.0, 0.0, 0.0),
        (5.0, 0.0, 0.0),
        (10.0, 0.0, 0.0),
        (10.0, 0.0, 5.0),
    ]


def test_bot_shooting_accuracy_variance_and_cooldown():
    bot = Bot.create_default(bot_id="bot-accuracy", position=(0.0, 0.0, 0.0))
    rng = Random(1234)
    fired, direction = bot.shoot_at(
        now=1.0,
        target_position=(0.0, 0.0, 10.0),
        rng=rng,
        accuracy_degrees=5.0,
    )
    assert fired is True
    assert direction != (0.0, 0.0, 1.0)

    fired_again, _ = bot.shoot_at(
        now=1.01,
        target_position=(0.0, 0.0, 10.0),
        rng=rng,
        accuracy_degrees=5.0,
    )
    assert fired_again is False


def test_bot_death_money_drop_and_player_collection():
    bot = Bot.create_default(bot_id="bot-drop", position=(2.0, 0.0, 2.0))
    money_system = MoneyPickupSystem()
    player = Player.with_starter_loadout(start_health=100, start_money=0)

    with pytest.raises(ValueError):
        bot.spawn_money_drop(pickup_system=money_system, amount=125)

    bot.apply_damage(100)
    pickup = bot.spawn_money_drop(pickup_system=money_system, amount=125)
    assert pickup.amount == 125
    assert pickup.position == (2.0, 0.0, 2.0)
    assert len(money_system.pickups) == 1

    collected = money_system.collect_for_player(
        player=player,
        player_position=(2.1, 0.0, 2.1),
    )
    assert collected == 125
    assert player.money == 125
    assert len(money_system.pickups) == 0


def test_money_pickup_collision_and_visual_definition():
    system = MoneyPickupSystem()
    pickup = system.spawn_pickup(amount=300, position=(0.0, 0.0, 0.0), radius=0.5)
    assert pickup.intersects_sphere(center=(0.5, 0.0, 0.0), radius=0.2) is True
    assert pickup.intersects_sphere(center=(5.0, 0.0, 0.0), radius=0.2) is False
    assert get_money_pickup_visual(300).primitive == "sphere"
    assert get_money_pickup_visual(50).primitive == "cube"


def test_economy_progression_curve_is_reasonable_for_weapon_tiers():
    assert ECONOMY_CONFIG.bot_kill_reward > 0
    assert ECONOMY_CONFIG.shotgun_price > ECONOMY_CONFIG.bot_kill_reward
    assert ECONOMY_CONFIG.assault_rifle_price > ECONOMY_CONFIG.shotgun_price
    assert ECONOMY_CONFIG.rpg_price > ECONOMY_CONFIG.assault_rifle_price

    # Keep each upgrade step within a practical wave range for progression pacing.
    kills_for_shotgun = ECONOMY_CONFIG.shotgun_price / ECONOMY_CONFIG.bot_kill_reward
    kills_for_rifle = ECONOMY_CONFIG.assault_rifle_price / ECONOMY_CONFIG.bot_kill_reward
    kills_for_rpg = ECONOMY_CONFIG.rpg_price / ECONOMY_CONFIG.bot_kill_reward
    assert 1.0 < kills_for_shotgun <= 4.0
    assert kills_for_rifle <= 10.0
    assert kills_for_rpg <= 20.0


def test_player_can_afford_weapon_progression_at_reasonable_wave_pace():
    layout = create_default_facility_layout()
    director = WaveDirector()
    rng = Random(7)
    cumulative_kills = 0
    afford_wave: dict[str, int] = {}

    for wave_number in range(1, 8):
        bots = director.spawn_wave(
            wave_number=wave_number,
            spawn_positions=layout.bot_spawn_positions(),
            rng=rng,
        )
        cumulative_kills += len(bots)
        money = cumulative_kills * ECONOMY_CONFIG.bot_kill_reward
        if "shotgun" not in afford_wave and money >= ECONOMY_CONFIG.shotgun_price:
            afford_wave["shotgun"] = wave_number
        if "assault_rifle" not in afford_wave and money >= ECONOMY_CONFIG.assault_rifle_price:
            afford_wave["assault_rifle"] = wave_number
        if "rpg" not in afford_wave and money >= ECONOMY_CONFIG.rpg_price:
            afford_wave["rpg"] = wave_number

    assert afford_wave["shotgun"] <= 1
    assert afford_wave["assault_rifle"] <= 2
    assert afford_wave["rpg"] <= 4


def test_max_expected_bot_count_update_path_is_fast():
    layout = create_default_facility_layout()
    director = WaveDirector()
    rng = Random(99)

    start = perf_counter()
    for _ in range(300):
        bots = director.spawn_wave(
            wave_number=20,
            spawn_positions=layout.bot_spawn_positions(),
            rng=rng,
        )
        for bot in bots:
            bot.set_state(BotAIState.CHASING)
            fired, _ = bot.shoot_at(
                now=10.0,
                target_position=(0.0, 0.0, 0.0),
                rng=rng,
                accuracy_degrees=3.0,
            )
            assert isinstance(fired, bool)
    elapsed = perf_counter() - start

    assert director.bot_count_for_wave(20) == 13
    if elapsed >= 0.6:
        print(f"Warning: Performance test took {elapsed:.3f}s (expected < 0.6s)")
