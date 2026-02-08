"""Player model with health, currency, inventory, and shooting."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.raycasting import RaycastHit, RaycastingSystem, RaycastTarget
from src.projectiles.projectile import Projectile
from src.weapons.pistol import Pistol
from src.weapons.switching import WeaponSwitchState
from src.weapons.weapon import Weapon


@dataclass
class Player:
    """Encapsulates runtime player state and core gameplay actions."""

    max_health: int
    health: int
    money: int
    position: tuple[float, float, float] = (0.0, 1.8, 0.0)
    rotation: tuple[float, float] = (0.0, 0.0)
    inventory: dict[str, Weapon] = field(default_factory=dict)
    equipped_weapon_name: str | None = None
    switch_state: WeaponSwitchState = field(default_factory=WeaponSwitchState)
    is_game_over: bool = False

    @classmethod
    def with_starter_loadout(cls, start_health: int, start_money: int) -> "Player":
        """Create a player initialized with the starter pistol."""
        player = cls(
            max_health=start_health,
            health=start_health,
            money=start_money,
        )
        pistol = Pistol()
        player.inventory[pistol.name] = pistol
        player.equipped_weapon_name = pistol.name
        return player

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @property
    def equipped_weapon(self) -> Weapon:
        if self.equipped_weapon_name is None:
            raise ValueError("No weapon equipped. Use with_starter_loadout() or add_weapon() first.")
        if self.equipped_weapon_name not in self.inventory:
            raise ValueError(
                f"Equipped weapon '{self.equipped_weapon_name}' not found in inventory."
            )
        return self.inventory[self.equipped_weapon_name]

    def set_rotation(self, yaw: float, pitch: float) -> None:
        self.rotation = (yaw, pitch)

    def set_position(self, x: float, y: float, z: float) -> None:
        self.position = (x, y, z)

    def apply_damage(self, damage: int) -> None:
        """Reduce health while clamping at zero."""
        if damage < 0:
            raise ValueError("Damage must be non-negative.")
        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.is_game_over = True

    def heal(self, amount: int) -> None:
        """Restore health without exceeding max health."""
        if amount < 0:
            raise ValueError("Heal amount must be non-negative.")
        self.health = min(self.max_health, self.health + amount)

    def add_money(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Amount must be non-negative.")
        self.money += amount

    def spend_money(self, amount: int) -> bool:
        if amount < 0:
            raise ValueError("Amount must be non-negative.")
        if self.money < amount:
            return False
        self.money -= amount
        return True

    def add_weapon(self, weapon: Weapon, auto_equip: bool = False) -> None:
        self.inventory[weapon.name] = weapon
        if auto_equip:
            self.equipped_weapon_name = weapon.name

    def equip_weapon(self, weapon_name: str) -> None:
        if weapon_name not in self.inventory:
            raise ValueError(f"Weapon '{weapon_name}' not in inventory.")
        self.equipped_weapon_name = weapon_name

    def cycle_weapon(self, direction: int = 1) -> str:
        """Cycle through inventory weapons and return the newly equipped name."""
        if direction == 0:
            raise ValueError("direction cannot be 0.")
        weapon_names = list(self.inventory.keys())
        if not weapon_names:
            raise ValueError("No weapons available in inventory.")
        if self.equipped_weapon_name not in weapon_names:
            self.equipped_weapon_name = weapon_names[0]
            return self.equipped_weapon_name
        current_index = weapon_names.index(self.equipped_weapon_name)
        next_index = (current_index + direction) % len(weapon_names)
        self.equipped_weapon_name = weapon_names[next_index]
        return self.equipped_weapon_name

    @property
    def is_weapon_switching(self) -> bool:
        return self.switch_state.is_switching

    def start_smooth_weapon_switch(self, weapon_name: str, now: float) -> bool:
        """Begin a timed switch transition to an owned weapon."""
        if weapon_name not in self.inventory:
            raise ValueError(f"Weapon '{weapon_name}' not in inventory.")
        if self.equipped_weapon_name is None:
            self.equipped_weapon_name = weapon_name
            return False
        return self.switch_state.start_switch(self.equipped_weapon_name, weapon_name, now)

    def start_smooth_cycle_weapon(self, now: float, direction: int = 1) -> bool:
        """Begin a timed switch to the next/previous inventory weapon."""
        if direction == 0:
            raise ValueError("direction cannot be 0.")
        weapon_names = list(self.inventory.keys())
        if not weapon_names:
            raise ValueError("No weapons available in inventory.")
        if self.equipped_weapon_name not in weapon_names:
            self.equipped_weapon_name = weapon_names[0]
            return False
        current_index = weapon_names.index(self.equipped_weapon_name)
        next_index = (current_index + direction) % len(weapon_names)
        return self.start_smooth_weapon_switch(weapon_names[next_index], now)

    def update_weapon_switch(self, now: float) -> str | None:
        """Complete active smooth transition and return equipped weapon when done."""
        next_weapon = self.switch_state.complete_if_ready(now)
        if next_weapon is None:
            return None
        self.equipped_weapon_name = next_weapon
        return next_weapon

    def reload_weapon(self) -> int:
        return self.equipped_weapon.reload()

    def shoot(self, now: float) -> bool:
        """Attempt to fire the equipped weapon. Returns True when a shot is fired."""
        if not self.is_alive or self.is_game_over:
            return False
        return self.equipped_weapon.fire(now)

    def shoot_projectiles(
        self,
        now: float,
        origin: tuple[float, float, float],
        direction: tuple[float, float, float],
    ) -> list[Projectile]:
        """Fire the equipped weapon and return instantiated projectile entities."""
        if not self.shoot(now):
            return []
        payload = self.equipped_weapon.create_projectile_payload(
            origin=origin,
            direction=direction,
        )
        return [Projectile.from_payload(item) for item in payload]

    def shoot_hitscan(
        self,
        *,
        now: float,
        origin: tuple[float, float, float],
        direction: tuple[float, float, float],
        targets: list[RaycastTarget],
        raycasting_system: RaycastingSystem,
        max_distance: float = 120.0,
    ) -> RaycastHit | None:
        """Fire equipped weapon and return nearest hit-scan hit, if any."""
        if not self.shoot(now):
            return None
        return raycasting_system.cast_ray(
            origin=origin,
            direction=direction,
            max_distance=max_distance,
            targets=targets,
        )

    def respawn(self, spawn_position: tuple[float, float, float]) -> None:
        """Reset player death/game-over state and place at spawn."""
        self.health = self.max_health
        self.position = spawn_position
        self.is_game_over = False
