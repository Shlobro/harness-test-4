import pytest

from src.core.game_clock import GameClock
from src.core.game_loop import GameLoop
from src.core.game_state import GameState, GameStateManager
from src.core.input_handler import InputHandler, InputSnapshot


def test_game_clock_tracks_delta_and_elapsed_time():
    clock = GameClock()

    assert clock.tick(10.0) == 0.0
    assert clock.elapsed_time == 0.0
    assert clock.frame_count == 0

    assert clock.tick(10.25) == 0.25
    assert clock.tick(10.75) == 0.5
    assert clock.elapsed_time == 0.75
    assert clock.frame_count == 2


def test_state_manager_validates_transitions():
    manager = GameStateManager()

    manager.transition_to(GameState.PLAYING)
    manager.transition_to(GameState.PAUSED)
    manager.transition_to(GameState.PLAYING)
    manager.transition_to(GameState.CRASHED)
    manager.transition_to(GameState.MENU)

    assert manager.transition_history == [
        GameState.MENU,
        GameState.PLAYING,
        GameState.PAUSED,
        GameState.PLAYING,
        GameState.CRASHED,
        GameState.MENU,
    ]

    with pytest.raises(ValueError):
        manager.transition_to(GameState.PAUSED)


def test_input_handler_maps_wasd_and_mouse_look():
    handler = InputHandler(mouse_sensitivity=2.0)
    snapshot = InputSnapshot(
        pressed_keys={"w", "d"},
        mouse_delta_x=3.0,
        mouse_delta_y=-4.0,
    )

    frame = handler.build_frame(snapshot)
    assert frame.move_x == 1.0
    assert frame.move_z == 1.0
    assert frame.look_yaw == 6.0
    assert frame.look_pitch == 8.0


def test_game_loop_updates_only_while_playing():
    manager = GameStateManager()
    loop = GameLoop(state_manager=manager)
    deltas = []
    loop.register_update_callback(deltas.append)

    loop.step(1.0)
    loop.step(1.1)
    assert deltas == []

    manager.transition_to(GameState.PLAYING)
    loop.step(1.4)
    loop.step(1.8)
    assert deltas == pytest.approx([0.3, 0.4])
