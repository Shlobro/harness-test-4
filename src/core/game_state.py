"""Game state management for high-level flow transitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class GameState(str, Enum):
    """Allowed top-level game states."""

    MENU = "menu"
    CONTROLS = "controls"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    CRASHED = "crashed"


@dataclass
class GameStateManager:
    """Controls current state and validates state transitions."""

    current_state: GameState = GameState.MENU
    transition_history: list[GameState] = field(default_factory=lambda: [GameState.MENU])

    _ALLOWED_TRANSITIONS = {
        GameState.MENU: {GameState.PLAYING, GameState.CONTROLS},
        GameState.CONTROLS: {GameState.MENU},
        GameState.PLAYING: {GameState.PAUSED, GameState.CRASHED, GameState.GAME_OVER, GameState.MENU},
        GameState.PAUSED: {GameState.PLAYING, GameState.GAME_OVER, GameState.MENU},
        GameState.GAME_OVER: {GameState.MENU, GameState.PLAYING},
        GameState.CRASHED: {GameState.MENU},
    }

    def can_transition_to(self, next_state: GameState) -> bool:
        """Return True when a transition is allowed from the current state."""
        return next_state in self._ALLOWED_TRANSITIONS[self.current_state]

    def transition_to(self, next_state: GameState) -> None:
        """Move to a new valid state or raise ValueError."""
        if not self.can_transition_to(next_state):
            raise ValueError(
                f"Invalid transition: {self.current_state.value} -> {next_state.value}"
            )
        self.current_state = next_state
        self.transition_history.append(next_state)

