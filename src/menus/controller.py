"""Game-flow controller for menu screens and glitch-driven transitions."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.audio.sound_manager import SoundManager
from src.core.game_state import GameState, GameStateManager
from src.glitch.sequence import GlitchAudioCue, GlitchSequenceController
from src.menus.screens import (
    MenuScreen,
    build_controls_screen,
    build_crash_ending_screen,
    build_game_over_screen,
    build_main_menu_screen,
    build_pause_menu_screen,
)


@dataclass
class GameFlowController:
    """Coordinates high-level state transitions and menu screen payloads."""

    state_manager: GameStateManager
    _game_over_stats: tuple[int, int] = field(default=(0, 0))

    def start_game(self) -> bool:
        """Start a new game session."""
        if self.state_manager.current_state in (
            GameState.MENU,
            GameState.GAME_OVER,
            GameState.PAUSED,
        ):
            if self.state_manager.can_transition_to(GameState.PLAYING):
                self.state_manager.transition_to(GameState.PLAYING)
                return True
        return False

    def toggle_pause(self) -> bool:
        """Toggle between PLAYING and PAUSED states."""
        state = self.state_manager.current_state
        if state == GameState.PLAYING:
            self.state_manager.transition_to(GameState.PAUSED)
            return True
        if state == GameState.PAUSED:
            self.state_manager.transition_to(GameState.PLAYING)
            return True
        return False

    def open_main_menu(self) -> bool:
        """Return to the main menu from any compatible state."""
        if self.state_manager.current_state == GameState.MENU:
            return False
        if self.state_manager.can_transition_to(GameState.MENU):
            self.state_manager.transition_to(GameState.MENU)
            return True
        return False

    def trigger_game_over(self, score: int, waves_cleared: int) -> bool:
        """Transition to game over state with provided session stats."""
        if self.state_manager.can_transition_to(GameState.GAME_OVER):
            self._game_over_stats = (score, waves_cleared)
            self.state_manager.transition_to(GameState.GAME_OVER)
            return True
        return False

    def handle_menu_action(self, action_id: str) -> bool:
        """Process a generic menu action ID. Returns True if handled."""
        if action_id == "start_game":
            return self.start_game()
        if action_id == "controls":
            if self.state_manager.can_transition_to(GameState.CONTROLS):
                self.state_manager.transition_to(GameState.CONTROLS)
                return True
        if action_id == "back_to_menu":
            return self.open_main_menu()
        if action_id == "resume_game":
            return self.toggle_pause()
        if action_id == "quit_to_menu":
            return self.open_main_menu()
        if action_id == "restart_game":
            return self.start_game()
        # "quit" is typically handled by the platform layer
        return False

    def handle_crash_recovery_input(
        self,
        *,
        now: float,
        pressed_keys: set[str],
        glitch_controller: GlitchSequenceController,
    ) -> bool:
        return glitch_controller.request_recover(now=now, pressed_keys=pressed_keys)

    def update(
        self,
        *,
        now: float,
        glitch_controller: GlitchSequenceController,
        sound_manager: SoundManager | None = None,
    ) -> None:
        glitch_controller.update(now)
        self._flush_glitch_audio(glitch_controller=glitch_controller, sound_manager=sound_manager)

        if glitch_controller.is_crash_screen_visible:
            if self.state_manager.current_state == GameState.PLAYING:
                self.state_manager.transition_to(GameState.CRASHED)

        recovery_complete = glitch_controller.complete_recovery_if_ready(now)
        if recovery_complete and self.state_manager.current_state == GameState.CRASHED:
            self.state_manager.transition_to(GameState.MENU)

    def get_active_screen(self, glitch_controller: GlitchSequenceController) -> MenuScreen | None:
        state = self.state_manager.current_state
        if state == GameState.MENU:
            return build_main_menu_screen()
        if state == GameState.CONTROLS:
            return build_controls_screen()
        if state == GameState.PAUSED:
            return build_pause_menu_screen()
        if state == GameState.GAME_OVER:
            score, waves = self._game_over_stats
            return build_game_over_screen(score=score, waves_cleared=waves)
        if state == GameState.CRASHED:
            return build_crash_ending_screen(glitch_controller.crash_screen)
        return None

    def _flush_glitch_audio(
        self,
        *,
        glitch_controller: GlitchSequenceController,
        sound_manager: SoundManager | None,
    ) -> None:
        if sound_manager is None:
            glitch_controller.consume_audio_cues()
            return

        for cue in glitch_controller.consume_audio_cues():
            if cue == GlitchAudioCue.TRANSITION_RAMP:
                sound_manager.play_glitch_transition_cue()
            elif cue == GlitchAudioCue.CRASH_IMPACT:
                sound_manager.play_glitch_crash_impact_cue()
            elif cue == GlitchAudioCue.RECOVERY_CONFIRM:
                sound_manager.play_glitch_recovery_cue()
