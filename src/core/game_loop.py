"""Main game loop orchestration with delta-time updates."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable

from src.core.game_clock import GameClock
from src.core.game_state import GameState, GameStateManager

logger = logging.getLogger(__name__)


FrameCallback = Callable[[float], None]


@dataclass
class GameLoop:
    """Owns frame stepping and update dispatch for active gameplay."""

    state_manager: GameStateManager
    clock: GameClock = field(default_factory=GameClock)
    _callbacks: list[FrameCallback] = field(default_factory=list)

    def register_update_callback(self, callback: FrameCallback) -> None:
        """Add a callback invoked each PLAYING frame with delta-time."""
        self._callbacks.append(callback)

    def step(self, now: float) -> float:
        """Run one frame step and return frame delta-time."""
        delta_time = self.clock.tick(now)
        if self.state_manager.current_state != GameState.PLAYING:
            return delta_time

        for callback in self._callbacks:
            try:
                callback(delta_time)
            except Exception as e:
                logger.error(f"Error in update callback {callback.__name__}: {e}", exc_info=True)
        return delta_time

