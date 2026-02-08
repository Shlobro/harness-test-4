"""Engine-agnostic HUD overlay state and update logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import floor

from src.player.player import Player


@dataclass(frozen=True)
class HealthBarState:
    """Normalized health bar values for renderers."""

    current_health: int
    max_health: int
    fill_ratio: float
    color: str


@dataclass(frozen=True)
class AmmoCounterState:
    """Ammo values for equipped weapon display."""

    weapon_name: str
    in_magazine: int
    magazine_size: int
    reserve_ammo: int
    display_text: str


@dataclass(frozen=True)
class MoneyDisplayState:
    """Currency display data."""

    amount: int
    display_text: str


@dataclass(frozen=True)
class CrosshairState:
    """Crosshair placement and style."""

    center_x: float
    center_y: float
    size: float
    thickness: float
    color: str


@dataclass(frozen=True)
class DamageIndicatorState:
    """Transient damage feedback layer values."""

    is_visible: bool
    alpha: float
    intensity: float
    remaining_seconds: float


@dataclass(frozen=True)
class KillNotification:
    """One kill-feed line with countdown lifetime."""

    message: str
    remaining_seconds: float


@dataclass(frozen=True)
class HudOverlayState:
    """Complete HUD payload passed to a rendering layer."""

    health: HealthBarState
    ammo: AmmoCounterState
    money: MoneyDisplayState
    crosshair: CrosshairState
    damage_indicator: DamageIndicatorState
    kill_count: int
    kill_notifications: list[KillNotification]


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


@dataclass
class HudOverlayController:
    """Builds HUD state and manages short-lived visual notifications."""

    damage_flash_seconds: float = 0.5
    kill_notification_seconds: float = 2.0
    max_notifications: int = 3
    _damage_remaining_seconds: float = 0.0
    _damage_intensity: float = 0.0
    _kill_count: int = 0
    _kill_notifications: list[KillNotification] = field(default_factory=list)

    def step(self, delta_time: float) -> None:
        """Advance temporary HUD effect timers."""
        if delta_time < 0.0:
            raise ValueError("delta_time must be non-negative.")
        if self._damage_remaining_seconds > 0.0:
            self._damage_remaining_seconds = max(0.0, self._damage_remaining_seconds - delta_time)
            if self._damage_remaining_seconds == 0.0:
                self._damage_intensity = 0.0

        next_notifications: list[KillNotification] = []
        for note in self._kill_notifications:
            remaining = note.remaining_seconds - delta_time
            if remaining > 0.0:
                next_notifications.append(
                    KillNotification(
                        message=note.message,
                        remaining_seconds=remaining,
                    )
                )
        self._kill_notifications = next_notifications

    def register_damage(self, amount: int) -> None:
        """Start or refresh a damage flash from player damage intake."""
        if amount <= 0:
            raise ValueError("amount must be positive.")
        scaled_intensity = _clamp01(amount / 60.0)
        self._damage_intensity = max(self._damage_intensity, scaled_intensity)
        self._damage_remaining_seconds = max(
            self._damage_remaining_seconds,
            self.damage_flash_seconds,
        )

    def register_kill(self, enemy_label: str = "Bot") -> None:
        """Record a kill and append a short-lived kill notification."""
        self._kill_count += 1
        message = f"{enemy_label} eliminated"
        self._kill_notifications.insert(
            0,
            KillNotification(
                message=message,
                remaining_seconds=self.kill_notification_seconds,
            ),
        )
        if len(self._kill_notifications) > self.max_notifications:
            self._kill_notifications = self._kill_notifications[: self.max_notifications]

    def build_state(self, player: Player) -> HudOverlayState:
        """Create a render-ready HUD snapshot from current player state."""
        weapon = player.equipped_weapon
        health_ratio = _clamp01(player.health / player.max_health) if player.max_health > 0 else 0.0
        health_color = "green"
        if health_ratio <= 0.25:
            health_color = "red"
        elif health_ratio <= 0.5:
            health_color = "yellow"

        damage_ratio = (
            _clamp01(self._damage_remaining_seconds / self.damage_flash_seconds)
            if self.damage_flash_seconds > 0.0
            else 0.0
        )
        damage_alpha = _clamp01(damage_ratio * self._damage_intensity)

        return HudOverlayState(
            health=HealthBarState(
                current_health=player.health,
                max_health=player.max_health,
                fill_ratio=health_ratio,
                color=health_color,
            ),
            ammo=AmmoCounterState(
                weapon_name=weapon.name,
                in_magazine=weapon.ammo_in_magazine,
                magazine_size=weapon.magazine_size,
                reserve_ammo=weapon.reserve_ammo,
                display_text=f"{weapon.ammo_in_magazine}/{weapon.magazine_size} | {weapon.reserve_ammo}",
            ),
            money=MoneyDisplayState(
                amount=player.money,
                display_text=f"${player.money}",
            ),
            crosshair=CrosshairState(
                center_x=0.5,
                center_y=0.5,
                size=16.0,
                thickness=2.0,
                color="white",
            ),
            damage_indicator=DamageIndicatorState(
                is_visible=self._damage_remaining_seconds > 0.0,
                alpha=damage_alpha,
                intensity=self._damage_intensity,
                remaining_seconds=self._damage_remaining_seconds,
            ),
            kill_count=self._kill_count,
            kill_notifications=[
                KillNotification(
                    message=note.message,
                    remaining_seconds=floor(note.remaining_seconds * 1000.0) / 1000.0,
                )
                for note in self._kill_notifications
            ],
        )
