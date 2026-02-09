"""Game-flow controller for menu screens and glitch-driven transitions."""

from __future__ import annotations

from dataclasses import dataclass

from src.audio.sound_manager import SoundManager
from src.core.game_state import GameState, GameStateManager
from src.glitch.sequence import GlitchAudioCue, GlitchPhase, GlitchSequenceController
from src.menus.screens import MenuScreen, build_crash_ending_screen, build_main_menu_screen


@dataclass
class GameFlowController:
    """Coordinates high-level state transitions and menu screen payloads."""

    state_manager: GameStateManager

    def start_game(self) -> bool:
        if self.state_manager.current_state != GameState.MENU:
            return False
        self.state_manager.transition_to(GameState.PLAYING)
        return True

    def toggle_pause(self) -> bool:
        state = self.state_manager.current_state
        if state == GameState.PLAYING:
            self.state_manager.transition_to(GameState.PAUSED)
            return True
        if state == GameState.PAUSED:
            self.state_manager.transition_to(GameState.PLAYING)
            return True
        return False

    def open_main_menu(self) -> bool:
        if self.state_manager.current_state == GameState.MENU:
            return False
        if not self.state_manager.can_transition_to(GameState.MENU):
            return False
        self.state_manager.transition_to(GameState.MENU)
        return True

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

        if glitch_controller.phase in (
            GlitchPhase.CRASH_SCREEN,
            GlitchPhase.RECOVERING,
        ):
            if self.state_manager.current_state == GameState.PLAYING:
                self.state_manager.transition_to(GameState.CRASHED)

        recovery_complete = glitch_controller.complete_recovery_if_ready(now)
        if recovery_complete and self.state_manager.current_state == GameState.CRASHED:
            self.state_manager.transition_to(GameState.MENU)

    def get_active_screen(self, glitch_controller: GlitchSequenceController) -> MenuScreen | None:
        state = self.state_manager.current_state
        if state == GameState.MENU:
            return build_main_menu_screen()
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
