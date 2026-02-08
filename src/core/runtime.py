"""Runtime wiring helpers that bridge gameplay events to HUD updates."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.game_loop import GameLoop
from src.hud.overlay import HudOverlayController, HudOverlayState
from src.player.player import Player


@dataclass
class HudEventRuntimeBridge:
    """Queues gameplay events and applies them to the HUD inside game-loop updates."""

    game_loop: GameLoop
    hud_controller: HudOverlayController
    _pending_damage_events: list[int] = field(default_factory=list)
    _pending_kill_events: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.game_loop.register_update_callback(self.on_frame_update)

    def queue_damage_event(self, amount: int) -> None:
        """Queue a player damage event to be flushed during the next playing frame."""
        if amount <= 0:
            raise ValueError("amount must be positive.")
        self._pending_damage_events.append(amount)

    def queue_kill_event(self, enemy_label: str = "Bot") -> None:
        """Queue a kill event to be flushed during the next playing frame."""
        self._pending_kill_events.append(enemy_label)

    def on_frame_update(self, delta_time: float) -> None:
        """Flush queued events and advance transient HUD timers."""
        for amount in self._pending_damage_events:
            self.hud_controller.register_damage(amount)
        self._pending_damage_events.clear()

        for enemy_label in self._pending_kill_events:
            self.hud_controller.register_kill(enemy_label)
        self._pending_kill_events.clear()

        self.hud_controller.step(delta_time)


@dataclass
class RuntimeSession:
    """Minimal runtime composition helper for player + HUD integration."""

    player: Player
    game_loop: GameLoop
    hud_controller: HudOverlayController = field(default_factory=HudOverlayController)
    hud_bridge: HudEventRuntimeBridge = field(init=False)

    def __post_init__(self) -> None:
        self.hud_bridge = HudEventRuntimeBridge(
            game_loop=self.game_loop,
            hud_controller=self.hud_controller,
        )

    def apply_player_damage(self, amount: int) -> None:
        """Apply player damage and enqueue HUD feedback."""
        health_before = self.player.health
        self.player.apply_damage(amount)
        damage_taken = health_before - self.player.health
        if damage_taken > 0:
            self.hud_bridge.queue_damage_event(damage_taken)

    def register_bot_kill(self, enemy_label: str = "Bot") -> None:
        """Queue a bot kill event for HUD notification/counter updates."""
        self.hud_bridge.queue_kill_event(enemy_label)

    def build_hud_state(self) -> HudOverlayState:
        """Build a render-ready HUD state for the current player frame."""
        return self.hud_controller.build_state(self.player)
