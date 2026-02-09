import pytest

from src.audio.engine import AudioEngine
from src.audio.sound_manager import SoundManager
from src.core.game_clock import GameClock
from src.core.game_loop import GameLoop
from src.core.raycasting import RaycastingSystem, RaycastTarget
from src.core.runtime import RuntimeSession
from src.core.game_state import GameState, GameStateManager
from src.core.input_handler import InputHandler, InputSnapshot
from src.glitch.sequence import GlitchSequenceConfig, GlitchSequenceController
from src.menus.controller import GameFlowController
from src.player.player import Player


def test_game_clock_tracks_delta_and_elapsed_time():
    clock = GameClock()

    assert clock.tick(10.0) == 0.0
    assert clock.elapsed_time == 0.0
    assert clock.frame_count == 0

    assert clock.tick(10.25) == 0.25
    assert clock.tick(10.75) == 0.5
    assert clock.elapsed_time == 0.75
    assert clock.frame_count == 2


def test_game_clock_pause_and_time_scale_controls():
    clock = GameClock()
    clock.tick(0.0)

    clock.set_time_scale(0.5)
    assert clock.tick(2.0) == 1.0
    assert clock.elapsed_time == 1.0
    assert clock.unscaled_elapsed_time == 2.0

    clock.set_paused(True)
    assert clock.tick(3.0) == 0.0
    assert clock.elapsed_time == 1.0
    assert clock.unscaled_elapsed_time == 3.0

    clock.set_paused(False)
    assert clock.tick(5.0) == 1.0
    assert clock.elapsed_time == 2.0
    assert clock.frame_count == 2

    with pytest.raises(ValueError):
        clock.set_time_scale(0.0)


def test_raycasting_system_returns_closest_valid_target():
    system = RaycastingSystem()
    hit = system.cast_ray(
        origin=(0.0, 0.0, 0.0),
        direction=(1.0, 0.0, 0.0),
        max_distance=20.0,
        targets=[
            RaycastTarget(target_id="far", center=(10.0, 0.0, 0.0), radius=1.0),
            RaycastTarget(target_id="near", center=(4.0, 0.0, 0.0), radius=0.5),
            RaycastTarget(target_id="inactive", center=(2.0, 0.0, 0.0), radius=0.5, is_active=False),
        ],
    )
    assert hit is not None
    assert hit.target_id == "near"
    assert hit.distance == pytest.approx(3.5)


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


def test_runtime_session_routes_damage_and_kill_events_to_hud_during_playing_frames():
    manager = GameStateManager()
    loop = GameLoop(state_manager=manager)
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    session = RuntimeSession(player=player, game_loop=loop)

    session.apply_player_damage(25)
    session.register_bot_kill("Bot Delta")
    not_playing_state = session.build_hud_state()
    assert not_playing_state.damage_indicator.is_visible is False
    assert not_playing_state.kill_count == 0

    manager.transition_to(GameState.PLAYING)
    loop.step(10.0)
    playing_state = session.build_hud_state()
    assert playing_state.health.current_health == 75
    assert playing_state.damage_indicator.is_visible is True
    assert playing_state.kill_count == 1
    assert [note.message for note in playing_state.kill_notifications] == ["Bot Delta eliminated"]


def test_runtime_session_routes_audio_events_during_playing_frames():
    manager = GameStateManager()
    loop = GameLoop(state_manager=manager)
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    audio_engine = AudioEngine()
    sound_manager = SoundManager(engine=audio_engine)
    session = RuntimeSession(player=player, game_loop=loop, sound_manager=sound_manager)

    session.register_weapon_fire_audio("Pistol")
    session.register_weapon_fire_audio("RPG")
    session.register_player_footstep_audio(is_running=True)
    session.register_bot_fire_audio()
    session.register_bot_death_audio()
    session.register_money_pickup_audio()
    session.start_ambient_audio()
    assert audio_engine.active_events == []

    session.register_ui_audio("shop_open")
    ui_sound_names = [evt.sound_name for evt in audio_engine.active_events]
    assert "ui_shop_open" in ui_sound_names

    manager.transition_to(GameState.PLAYING)
    loop.step(2.0)
    active_sound_names = [evt.sound_name for evt in audio_engine.active_events]
    assert "shot_pistol" in active_sound_names
    assert "rpg_pre_crash_warning" in active_sound_names
    assert "shot_rpg" in active_sound_names
    assert "footstep_run" in active_sound_names
    assert "bot_shot" in active_sound_names
    assert "bot_death" in active_sound_names
    assert "money_pickup" in active_sound_names
    assert "ui_shop_open" in active_sound_names
    assert "ambient_facility_hum" in active_sound_names

    session.stop_ambient_audio()
    loop.step(2.1)
    assert all(evt.sound_name != "ambient_facility_hum" for evt in audio_engine.active_events)


def test_game_flow_main_menu_screen_has_start_action():
    manager = GameStateManager()
    flow = GameFlowController(state_manager=manager)
    glitch = GlitchSequenceController()

    screen = flow.get_active_screen(glitch)
    assert screen is not None
    assert screen.screen_id == "main_menu"
    assert screen.title == "FPS Bot Arena"
    assert any(action.action_id == "start_game" and action.is_primary for action in screen.actions)


def test_game_flow_transitions_to_crashed_and_back_to_menu_after_recovery():
    manager = GameStateManager()
    flow = GameFlowController(state_manager=manager)
    glitch = GlitchSequenceController(
        config=GlitchSequenceConfig(transition_seconds=0.5, recovery_seconds=0.2)
    )
    engine = AudioEngine()
    sound_manager = SoundManager(engine=engine)

    assert flow.start_game() is True
    assert manager.current_state == GameState.PLAYING

    glitch.start_transition(now=0.0)
    flow.update(now=0.1, glitch_controller=glitch, sound_manager=sound_manager)
    assert manager.current_state == GameState.PLAYING  # Still playing during transition
    assert any(evt.sound_name == "glitch_transition_ramp" for evt in engine.active_events)

    flow.update(now=0.6, glitch_controller=glitch, sound_manager=sound_manager)
    assert manager.current_state == GameState.CRASHED  # Now crashed after transition completes
    crash_screen = flow.get_active_screen(glitch)
    assert crash_screen is not None
    assert crash_screen.screen_id == "crash_ending"
    assert any(action.action_id == "restart_to_menu" for action in crash_screen.actions)
    assert any(evt.sound_name == "glitch_crash_impact" for evt in engine.active_events)

    restarted = flow.handle_crash_recovery_input(
        now=0.6,
        pressed_keys={"Enter"},
        glitch_controller=glitch,
    )
    assert restarted is True
    flow.update(now=0.81, glitch_controller=glitch, sound_manager=sound_manager)
    assert manager.current_state == GameState.MENU
    assert any(evt.sound_name == "glitch_recovery_confirm" for evt in engine.active_events)


def test_game_flow_manages_controls_pause_and_game_over_screens():
    manager = GameStateManager()
    flow = GameFlowController(state_manager=manager)
    glitch = GlitchSequenceController()

    # Menu -> Controls -> Menu
    assert manager.current_state == GameState.MENU
    assert flow.handle_menu_action("controls") is True
    assert manager.current_state == GameState.CONTROLS
    controls_screen = flow.get_active_screen(glitch)
    assert controls_screen.screen_id == "controls"

    assert flow.handle_menu_action("back_to_menu") is True
    assert manager.current_state == GameState.MENU

    # Menu -> Playing -> Paused -> Playing
    assert flow.handle_menu_action("start_game") is True
    assert manager.current_state == GameState.PLAYING

    # Simulate hitting pause (toggle)
    assert flow.toggle_pause() is True
    assert manager.current_state == GameState.PAUSED
    pause_screen = flow.get_active_screen(glitch)
    assert pause_screen.screen_id == "pause_menu"

    # Simulate clicking "Resume"
    assert flow.handle_menu_action("resume_game") is True
    assert manager.current_state == GameState.PLAYING

    # Playing -> Game Over -> Menu
    assert flow.trigger_game_over(score=500, waves_cleared=3) is True
    assert manager.current_state == GameState.GAME_OVER
    game_over_screen = flow.get_active_screen(glitch)
    assert game_over_screen.screen_id == "game_over"
    assert "survived 3 waves" in game_over_screen.subtitle
    assert "score of 500" in game_over_screen.subtitle

    assert flow.handle_menu_action("quit_to_menu") is True
    assert manager.current_state == GameState.MENU
