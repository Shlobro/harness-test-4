"""Money pickup entities and collection logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.player.player import Player


Vector3 = tuple[float, float, float]


def _distance(a: Vector3, b: Vector3) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return sqrt((dx * dx) + (dy * dy) + (dz * dz))


@dataclass(frozen=True)
class MoneyPickupVisual:
    """Simple visual definition for primitive-based money pickups."""

    primitive: str
    base_color: str
    emissive_color: str
    pulse_hz: float
    scale: tuple[float, float, float]


@dataclass
class MoneyPickup:
    """Collectible currency item dropped into the world."""

    pickup_id: str
    amount: int
    position: Vector3
    radius: float = 0.55
    ttl_seconds: float = 30.0
    age_seconds: float = 0.0
    is_active: bool = True
    visual: MoneyPickupVisual = field(default_factory=lambda: get_money_pickup_visual(0))

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("amount must be positive.")
        if self.radius <= 0.0:
            raise ValueError("radius must be positive.")
        if self.ttl_seconds <= 0.0:
            raise ValueError("ttl_seconds must be positive.")
        if self.visual.primitive == "":
            self.visual = get_money_pickup_visual(self.amount)

    def step(self, delta_time: float) -> None:
        if delta_time < 0.0:
            raise ValueError("delta_time must be non-negative.")
        if not self.is_active:
            return
        self.age_seconds += delta_time
        if self.age_seconds >= self.ttl_seconds:
            self.is_active = False

    def intersects_sphere(self, center: Vector3, radius: float) -> bool:
        if radius <= 0.0:
            raise ValueError("radius must be positive.")
        return _distance(self.position, center) <= (self.radius + radius)


def get_money_pickup_visual(amount: int) -> MoneyPickupVisual:
    """Return primitive visual config for a money pickup amount."""
    if amount >= 200:
        return MoneyPickupVisual(
            primitive="sphere",
            base_color="gold",
            emissive_color="yellow",
            pulse_hz=3.0,
            scale=(0.45, 0.45, 0.45),
        )
    return MoneyPickupVisual(
        primitive="cube",
        base_color="green",
        emissive_color="lime",
        pulse_hz=2.0,
        scale=(0.35, 0.35, 0.35),
    )


@dataclass
class MoneyPickupSystem:
    """Tracks spawned pickups and resolves player collection."""

    pickups: list[MoneyPickup] = field(default_factory=list)
    _next_id: int = 1

    def spawn_pickup(
        self,
        *,
        amount: int,
        position: Vector3,
        radius: float = 0.55,
        ttl_seconds: float = 30.0,
    ) -> MoneyPickup:
        pickup = MoneyPickup(
            pickup_id=f"money-{self._next_id}",
            amount=amount,
            position=position,
            radius=radius,
            ttl_seconds=ttl_seconds,
            visual=get_money_pickup_visual(amount),
        )
        self._next_id += 1
        self.pickups.append(pickup)
        return pickup

    def step(self, delta_time: float) -> None:
        for pickup in self.pickups:
            pickup.step(delta_time)
        self.pickups = [pickup for pickup in self.pickups if pickup.is_active]

    def collect_for_player(
        self,
        *,
        player: "Player",
        player_position: Vector3,
        player_radius: float = 0.7,
    ) -> int:
        """Collect active pickups that intersect the player's pickup sphere."""
        if player_radius <= 0.0:
            raise ValueError("player_radius must be positive.")
        collected_amount = 0
        for pickup in self.pickups:
            if not pickup.is_active:
                continue
            if not pickup.intersects_sphere(center=player_position, radius=player_radius):
                continue
            player.add_money(pickup.amount)
            collected_amount += pickup.amount
            pickup.is_active = False
        self.pickups = [pickup for pickup in self.pickups if pickup.is_active]
        return collected_amount
