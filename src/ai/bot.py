"""Bot runtime model with combat hooks and money-drop behavior."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import sqrt
from random import Random

from src.ai.combat import vary_direction_with_accuracy
from src.economy.money import MoneyPickup, MoneyPickupSystem
from src.weapons.assault_rifle import AssaultRifle
from src.weapons.weapon import Weapon


Vector3 = tuple[float, float, float]


class BotAIState(str, Enum):
    """High-level tactical state labels for bots."""

    IDLE = "idle"
    CHASING = "chasing"
    ATTACKING = "attacking"
    SEEKING_COVER = "seeking_cover"
    FLANKING = "flanking"
    DEAD = "dead"


def _normalize(direction: Vector3) -> Vector3:
    length = sqrt(
        (direction[0] * direction[0])
        + (direction[1] * direction[1])
        + (direction[2] * direction[2])
    )
    if length <= 0.0:
        raise ValueError("Direction vector must be non-zero.")
    return (
        direction[0] / length,
        direction[1] / length,
        direction[2] / length,
    )


@dataclass
class Bot:
    """Basic tactical bot state with shooting and money-drop support."""

    bot_id: str
    max_health: int
    health: int
    position: Vector3
    ai_state: BotAIState = BotAIState.IDLE
    weapon: Weapon = field(default_factory=AssaultRifle)

    @classmethod
    def create_default(cls, bot_id: str, position: Vector3) -> "Bot":
        return cls(bot_id=bot_id, max_health=100, health=100, position=position)

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def set_state(self, state: BotAIState) -> None:
        if self.is_alive:
            self.ai_state = state

    def apply_damage(self, amount: int) -> bool:
        """Apply damage. Returns True when this call kills the bot."""
        if amount < 0:
            raise ValueError("Damage must be non-negative.")
        if not self.is_alive:
            return False
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.ai_state = BotAIState.DEAD
            return True
        return False

    def shoot_at(
        self,
        *,
        now: float,
        target_position: Vector3,
        rng: Random,
        accuracy_degrees: float = 3.0,
    ) -> tuple[bool, Vector3]:
        """Attempt to fire at target with configurable inaccuracy."""
        if not self.is_alive:
            return (False, (0.0, 0.0, 0.0))
        if accuracy_degrees < 0.0:
            raise ValueError("accuracy_degrees must be non-negative.")

        base_direction = _normalize(
            (
                target_position[0] - self.position[0],
                target_position[1] - self.position[1],
                target_position[2] - self.position[2],
            )
        )
        shot_direction = vary_direction_with_accuracy(
            direction=base_direction,
            accuracy_degrees=accuracy_degrees,
            rng=rng,
        )
        if not self.weapon.fire(now):
            return (False, shot_direction)
        return (True, shot_direction)

    def spawn_money_drop(
        self,
        *,
        pickup_system: MoneyPickupSystem,
        amount: int,
        pickup_radius: float = 0.55,
    ) -> MoneyPickup:
        """Spawn a collectible drop at this bot's position."""
        if self.is_alive:
            raise ValueError("Money drops can only be spawned after bot death.")
        return pickup_system.spawn_pickup(
            amount=amount,
            position=self.position,
            radius=pickup_radius,
        )
