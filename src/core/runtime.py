"""Runtime wiring helpers that bridge gameplay events to HUD updates."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.audio.sound_manager import SoundManager
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
class AudioEventRuntimeBridge:
    """Queues gameplay audio events and flushes them inside playing-frame updates."""

    game_loop: GameLoop
    sound_manager: SoundManager
    _pending_weapon_fire_events: list[str] = field(default_factory=list)
    _pending_footstep_events: list[bool] = field(default_factory=list)
    _pending_bot_fire_events: int = 0
    _pending_bot_death_events: int = 0
    _pending_money_pickup_events: int = 0
    _pending_start_ambient: bool = False
    _pending_stop_ambient: bool = False

    def __post_init__(self) -> None:
        self.game_loop.register_update_callback(self.on_frame_update)

    def queue_weapon_fire(self, weapon_name: str) -> None:
        self._pending_weapon_fire_events.append(weapon_name)

    def queue_footstep(self, *, is_running: bool = False) -> None:
        self._pending_footstep_events.append(is_running)

    def queue_bot_fire(self) -> None:
        self._pending_bot_fire_events += 1

    def queue_bot_death(self) -> None:
        self._pending_bot_death_events += 1

    def queue_money_pickup(self) -> None:
        self._pending_money_pickup_events += 1

    def play_ui_event_immediate(self, ui_event: str) -> None:
        """Play UI audio immediately regardless of game state for responsive feedback."""
        self.sound_manager.play_ui_event(ui_event)

    def queue_start_ambient(self) -> None:
        self._pending_start_ambient = True
        self._pending_stop_ambient = False

    def queue_stop_ambient(self) -> None:
        self._pending_stop_ambient = True
        self._pending_start_ambient = False

    def on_frame_update(self, delta_time: float) -> None:
        del delta_time
        if self._pending_start_ambient:
            self.sound_manager.start_ambient_facility()
        if self._pending_stop_ambient:
            self.sound_manager.stop_ambient_facility()

        for weapon_name in self._pending_weapon_fire_events:
            self.sound_manager.play_weapon_fire(weapon_name)
        for is_running in self._pending_footstep_events:
            self.sound_manager.play_footstep(is_running=is_running)
        for _ in range(self._pending_bot_fire_events):
            self.sound_manager.play_bot_fire()
        for _ in range(self._pending_bot_death_events):
            self.sound_manager.play_bot_death()
        for _ in range(self._pending_money_pickup_events):
            self.sound_manager.play_money_pickup()

        self._pending_weapon_fire_events.clear()
        self._pending_footstep_events.clear()
        self._pending_bot_fire_events = 0
        self._pending_bot_death_events = 0
        self._pending_money_pickup_events = 0
        self._pending_start_ambient = False
        self._pending_stop_ambient = False


@dataclass
class RuntimeSession:
    """Minimal runtime composition helper for player + HUD integration."""

    player: Player
    game_loop: GameLoop
    hud_controller: HudOverlayController = field(default_factory=HudOverlayController)
    sound_manager: SoundManager | None = None
    hud_bridge: HudEventRuntimeBridge = field(init=False)
    audio_bridge: AudioEventRuntimeBridge | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.hud_bridge = HudEventRuntimeBridge(
            game_loop=self.game_loop,
            hud_controller=self.hud_controller,
        )
        if self.sound_manager is not None:
            self.audio_bridge = AudioEventRuntimeBridge(
                game_loop=self.game_loop,
                sound_manager=self.sound_manager,
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

    def register_weapon_fire_audio(self, weapon_name: str) -> None:
        """Queue weapon fire audio for playback during the next playing frame."""
        if self.audio_bridge is None:
            return
        self.audio_bridge.queue_weapon_fire(weapon_name)

    def register_player_footstep_audio(self, *, is_running: bool = False) -> None:
        """Queue footstep audio for playback during the next playing frame."""
        if self.audio_bridge is None:
            return
        self.audio_bridge.queue_footstep(is_running=is_running)

    def register_bot_fire_audio(self) -> None:
        if self.audio_bridge is None:
            return
        self.audio_bridge.queue_bot_fire()

    def register_bot_death_audio(self) -> None:
        if self.audio_bridge is None:
            return
        self.audio_bridge.queue_bot_death()

    def register_money_pickup_audio(self) -> None:
        if self.audio_bridge is None:
            return
        self.audio_bridge.queue_money_pickup()

    def register_ui_audio(self, ui_event: str) -> None:
        """Register UI audio event for immediate playback regardless of game state."""
        if self.audio_bridge is None:
            return
        self.audio_bridge.play_ui_event_immediate(ui_event)

    def start_ambient_audio(self) -> None:
        if self.audio_bridge is None:
            return
        self.audio_bridge.queue_start_ambient()

    def stop_ambient_audio(self) -> None:
        if self.audio_bridge is None:
            return
        self.audio_bridge.queue_stop_ambient()

    def build_hud_state(self) -> HudOverlayState:
        """Build a render-ready HUD state for the current player frame."""
        return self.hud_controller.build_state(self.player)
