"""RPG weapon implementation with special crash trigger behavior."""

from __future__ import annotations

from src.weapons.weapon import Weapon


class RPG(Weapon):
    """Endgame launcher that triggers the glitch sequence on fire."""

    def __init__(self) -> None:
        super().__init__(
            name="RPG",
            damage=200.0,
            fire_rate=0.5,
            magazine_size=1,
            reserve_ammo=3,
            projectile_speed=45.0,
            projectile_radius=0.3,
            projectile_kind="rocket",
        )
        self.crash_triggered = False

    def fire(self, now: float) -> bool:
        fired = super().fire(now)
        if fired:
            self.crash_triggered = True
        return fired
