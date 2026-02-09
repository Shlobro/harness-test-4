import pytest
from config.config import ECONOMY_CONFIG, GAME_CONFIG
from src.ai.bot import Bot
from src.ai.waves import WaveDirector
from src.weapons.pistol import Pistol
from src.weapons.shotgun import Shotgun
from src.weapons.assault_rifle import AssaultRifle
from src.weapons.rpg import RPG


def test_economy_progression_balance():
    """Verify that bot rewards allow purchasing weapons at appropriate wave milestones."""
    wave_director = WaveDirector()
    
    # Calculate cumulative earnings per wave assuming perfect survival
    def calculate_wave_earnings(wave_num):
        bot_count = wave_director.bot_count_for_wave(wave_num)
        return bot_count * ECONOMY_CONFIG.bot_kill_reward

    wave_1_earnings = calculate_wave_earnings(1)
    wave_2_earnings = calculate_wave_earnings(2)
    wave_3_earnings = calculate_wave_earnings(3)
    wave_4_earnings = calculate_wave_earnings(4)

    cumulative_wave_1 = GAME_CONFIG.start_money + wave_1_earnings
    cumulative_wave_2 = cumulative_wave_1 + wave_2_earnings
    cumulative_wave_3 = cumulative_wave_2 + wave_3_earnings
    cumulative_wave_4 = cumulative_wave_3 + wave_4_earnings

    # Milestone 1: Shotgun (Price 250)
    # Should be affordable after Wave 1 (Earnings: 3 * 125 = 375)
    assert cumulative_wave_1 >= ECONOMY_CONFIG.shotgun_price, \
        f"Shotgun should be affordable after Wave 1. Money: {cumulative_wave_1}, Price: {ECONOMY_CONFIG.shotgun_price}"

    # Milestone 2: Assault Rifle (Price 800)
    # Should be affordable after Wave 2.
    # Wave 1 (375) + Wave 2 (5 * 125 = 625) = 1000.
    assert cumulative_wave_2 >= ECONOMY_CONFIG.assault_rifle_price, \
        f"AR should be affordable after Wave 2. Money: {cumulative_wave_2}, Price: {ECONOMY_CONFIG.assault_rifle_price}"

    # Milestone 3: RPG (Price 2000)
    # Wave 1+2 (1000) + Wave 3 (7 * 125 = 875) = 1875. (Almost there)
    # Wave 4 (9 * 125 = 1125). Total ~3000.
    # So RPG is affordable during or after Wave 4.
    assert cumulative_wave_4 >= ECONOMY_CONFIG.rpg_price, \
        f"RPG should be affordable by Wave 4. Money: {cumulative_wave_4}, Price: {ECONOMY_CONFIG.rpg_price}"


def test_time_to_kill_balance():
    """Verify that weapons kill bots within reasonable timeframes."""
    bot = Bot.create_default("dummy", (0, 0, 0))
    bot_health = bot.max_health  # 100

    pistol = Pistol()
    shotgun = Shotgun()
    ar = AssaultRifle()
    rpg = RPG()

    # DPS Calculations (assuming all shots hit)
    pistol_dps = pistol.damage * pistol.fire_rate  # 20 * 3 = 60
    shotgun_dps = shotgun.damage * shotgun.pellet_count * shotgun.fire_rate  # 12 * 8 * 1 = 96
    ar_dps = ar.damage * ar.fire_rate  # 16 * 9 = 144
    rpg_damage = rpg.damage  # 200 (One shot)

    # Time to Kill (Seconds) = Health / DPS
    pistol_ttk = bot_health / pistol_dps
    shotgun_ttk = bot_health / shotgun_dps
    ar_ttk = bot_health / ar_dps

    # Assertions for game feel
    
    # Pistol: ~1.6s. Should be > 1.0s (not too fast) but < 2.5s (not spongy)
    assert 1.0 < pistol_ttk < 2.5, f"Pistol TTK {pistol_ttk} is out of intended range"

    # Shotgun: ~1.04s. Should be faster than pistol at close range.
    # Actually, shotgun fire rate is 1.0, so it fires at t=0, t=1.
    # At t=0: 96 dmg. Bot has 4 HP.
    # At t=1: 96 dmg. Bot dies.
    # So effective TTK is 1.0s.
    assert shotgun_ttk < pistol_ttk, "Shotgun should kill faster than pistol"

    # AR: ~0.69s. Should be the sustained DPS king.
    assert ar_ttk < 1.0, f"AR TTK {ar_ttk} should be sub-second"

    # RPG: One shot.
    assert rpg_damage >= bot_health, "RPG should one-shot basic bots"
