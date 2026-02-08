from dataclasses import FrozenInstanceError
import pytest
from config.config import GAME_CONFIG, ECONOMY_CONFIG, GameConfig, EconomyConfig

def test_game_config_defaults():
    """Verify that GameConfig loads with the expected default values."""
    assert GAME_CONFIG.game_title == "FPS Bot Arena: The Glitch"
    assert GAME_CONFIG.start_health == 100
    assert GAME_CONFIG.start_money == 0
    assert GAME_CONFIG.mouse_sensitivity == 40.0
    assert GAME_CONFIG.walk_speed == 5.0
    assert isinstance(GAME_CONFIG, GameConfig)

def test_economy_config_defaults():
    """Verify that EconomyConfig loads with the expected default values."""
    assert ECONOMY_CONFIG.shotgun_price == 300
    assert ECONOMY_CONFIG.assault_rifle_price == 900
    assert ECONOMY_CONFIG.rpg_price == 2500
    assert isinstance(ECONOMY_CONFIG, EconomyConfig)

def test_config_immutability():
    """Verify that configuration objects are frozen (immutable)."""
    with pytest.raises(FrozenInstanceError):
        GAME_CONFIG.start_health = 200