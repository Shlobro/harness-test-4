"""Wave spawning and difficulty scaling for bot encounters."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from src.ai.bot import Bot
from src.weapons.assault_rifle import AssaultRifle


Vector3 = tuple[float, float, float]


@dataclass(frozen=True)
class WaveDifficulty:
    """Difficulty profile for a single wave."""

    wave_number: int
    bot_health: int
    accuracy_degrees: float
    fire_rate_multiplier: float


class WaveDirector:
    """Provides deterministic wave sizes and bot stat scaling."""

    def __init__(
        self,
        *,
        base_bot_count: int = 3,
        max_extra_bots: int = 10,
    ) -> None:
        self.base_bot_count = base_bot_count
        self.max_extra_bots = max_extra_bots

    def bot_count_for_wave(self, wave_number: int) -> int:
        if wave_number <= 0:
            raise ValueError("wave_number must be positive.")
        extra = min(self.max_extra_bots, (wave_number - 1) * 2)
        return self.base_bot_count + extra

    def difficulty_for_wave(self, wave_number: int) -> WaveDifficulty:
        if wave_number <= 0:
            raise ValueError("wave_number must be positive.")
        health = 100 + ((wave_number - 1) * 12)
        accuracy = max(0.8, 4.5 - ((wave_number - 1) * 0.35))
        fire_rate_multiplier = 1.0 + ((wave_number - 1) * 0.06)
        return WaveDifficulty(
            wave_number=wave_number,
            bot_health=health,
            accuracy_degrees=accuracy,
            fire_rate_multiplier=fire_rate_multiplier,
        )

    def spawn_wave(
        self,
        *,
        wave_number: int,
        spawn_positions: list[Vector3],
        rng: Random,
    ) -> list[Bot]:
        """Spawn a wave of bots with scaled health and weapon fire rates."""
        if not spawn_positions:
            raise ValueError("spawn_positions must not be empty.")
        difficulty = self.difficulty_for_wave(wave_number)
        count = self.bot_count_for_wave(wave_number)
        bots: list[Bot] = []
        for index in range(count):
            position = spawn_positions[rng.randrange(0, len(spawn_positions))]
            weapon = AssaultRifle()
            weapon.fire_rate *= difficulty.fire_rate_multiplier
            bot = Bot(
                bot_id=f"wave-{wave_number}-bot-{index + 1}",
                max_health=difficulty.bot_health,
                health=difficulty.bot_health,
                position=position,
                weapon=weapon,
            )
            bots.append(bot)
        return bots
