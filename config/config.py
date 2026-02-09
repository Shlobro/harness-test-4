"""Project-wide configuration for the FPS Bot Arena prototype.

This module centralizes tunable values so gameplay systems can import
one source of truth instead of hardcoding constants.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    """Core configuration values for the current prototype."""

    game_title: str = "FPS Bot Arena: The Glitch"
    start_health: int = 100
    start_money: int = 0
    mouse_sensitivity: float = 40.0
    walk_speed: float = 5.0


@dataclass(frozen=True)
class EconomyConfig:
    """Weapon pricing configuration used by shop and progression systems."""

    shotgun_price: int = 250
    assault_rifle_price: int = 800
    rpg_price: int = 2000
    bot_kill_reward: int = 125


GAME_CONFIG = GameConfig()
ECONOMY_CONFIG = EconomyConfig()
