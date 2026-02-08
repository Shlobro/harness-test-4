"""Player model with health, currency, inventory, and shooting."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.weapons.pistol import Pistol
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

    def shoot(self, now: float) -> bool:
        """Attempt to fire the equipped weapon. Returns True when a shot is fired."""
        if not self.is_alive:
            return False
        return self.equipped_weapon.fire(now)

