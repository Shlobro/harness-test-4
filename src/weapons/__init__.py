"""Weapon definitions and shared weapon behavior."""

from src.weapons.assault_rifle import AssaultRifle
from src.weapons.pistol import Pistol
from src.weapons.rpg import RPG
from src.weapons.shotgun import Shotgun
from src.weapons.weapon import Weapon

__all__ = ["Weapon", "Pistol", "Shotgun", "AssaultRifle", "RPG"]
