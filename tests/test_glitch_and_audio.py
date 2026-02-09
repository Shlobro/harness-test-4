from src.audio.engine import AudioEngine
from src.audio.sound_manager import SoundManager
from src.glitch.bsod import build_fake_bsod_screen
from src.glitch.sequence import (
    GlitchAudioCue,
    GlitchPhase,
    GlitchSequenceConfig,
    GlitchSequenceController,
)
from src.weapons.rpg import RPG


def test_fake_bsod_content_is_realistic_and_explicitly_recoverable():
    screen = build_fake_bsod_screen()
    lines = screen.to_lines()
    rendered = "\n".join(lines).lower()

    assert screen.background_hex == "#0078D7"
    assert screen.text_hex == "#FFFFFF"
    assert "stop code" in rendered
    assert "critical_process_died" in rendered
    assert "what failed" in rendered
    assert "82% complete" in rendered
    assert "arena.help/crash-stopcode" in rendered
    assert "press enter or esc" in rendered
    assert "simulation notice" in rendered
    assert "recoverable" in rendered


def test_glitch_sequence_triggers_from_rpg_and_reaches_crash_phase():
    controller = GlitchSequenceController(config=GlitchSequenceConfig(transition_seconds=1.0))
    rpg = RPG()

    assert rpg.fire(1.0) is True
    assert rpg.crash_triggered is True
    assert controller.trigger_from_weapon(rpg, now=1.0) is True
    assert rpg.crash_triggered is False
    assert controller.phase == GlitchPhase.TRANSITION

    mid_effects = controller.update(now=1.5)
    assert mid_effects.shake_strength > 0.0
    assert mid_effects.distortion_amount > 0.0
    assert mid_effects.static_amount > 0.0
    assert controller.phase == GlitchPhase.TRANSITION

    full_effects = controller.update(now=2.0)
    assert controller.phase == GlitchPhase.CRASH_SCREEN
    assert full_effects.shake_strength == 1.0
    assert controller.should_lock_gameplay is True


def test_glitch_sequence_recovery_path_returns_to_idle():
    controller = GlitchSequenceController(
        config=GlitchSequenceConfig(transition_seconds=0.5, recovery_seconds=0.2)
    )
    controller.start_transition(now=0.0)
    controller.update(now=0.6)
    assert controller.phase == GlitchPhase.CRASH_SCREEN
    assert controller.is_crash_screen_visible is True

    assert controller.request_recover(now=0.6, pressed_keys={"Enter"}) is True
    assert controller.phase == GlitchPhase.RECOVERING
    assert controller.complete_recovery_if_ready(now=0.75) is False
    assert controller.complete_recovery_if_ready(now=0.81) is True
    assert controller.phase == GlitchPhase.IDLE
    assert controller.should_lock_gameplay is False


def test_glitch_sequence_emits_audio_cues_in_order_for_crash_lifecycle():
    controller = GlitchSequenceController(
        config=GlitchSequenceConfig(transition_seconds=0.5, recovery_seconds=0.2)
    )

    controller.start_transition(now=1.0)
    assert controller.consume_audio_cues() == [GlitchAudioCue.TRANSITION_RAMP]

    controller.update(now=1.5)
    assert controller.consume_audio_cues() == [GlitchAudioCue.CRASH_IMPACT]

    recovered = controller.request_recover(now=1.5, pressed_keys={"r"})
    assert recovered is True
    assert controller.consume_audio_cues() == [GlitchAudioCue.RECOVERY_CONFIRM]

    assert controller.complete_recovery_if_ready(now=1.71) is True
    assert controller.phase == GlitchPhase.IDLE


def test_audio_engine_tracks_and_stops_sound_events():
    engine = AudioEngine()
    first = engine.play(sound_name="shot_pistol", channel="weapon")
    second = engine.play(sound_name="ui_open", channel="ui")

    assert len(engine.active_events) == 2
    assert engine.stop(first) is True
    assert engine.stop("missing") is False
    assert len(engine.active_events) == 1
    assert engine.stop_channel("ui") == 1
    assert engine.active_events == []
    assert second != first


def test_sound_manager_provides_weapon_fire_profiles_and_playback():
    engine = AudioEngine()
    manager = SoundManager(engine=engine)

    for weapon_name in ("Pistol", "Shotgun", "AssaultRifle", "RPG"):
        profile = manager.get_weapon_shot_profile(weapon_name)
        assert profile is not None
        assert profile.sound_name.startswith("shot_")
        assert manager.play_weapon_fire(weapon_name) is not None

    assert manager.get_weapon_shot_profile("Laser") is None
    assert manager.play_weapon_fire("Laser") is None


def test_sound_manager_supports_movement_enemy_ui_economy_and_ambient_events():
    engine = AudioEngine()
    manager = SoundManager(engine=engine)

    footstep_walk = manager.play_footstep(is_running=False)
    footstep_run = manager.play_footstep(is_running=True)
    bot_fire = manager.play_bot_fire()
    bot_death = manager.play_bot_death()
    pickup = manager.play_money_pickup()
    ui_open = manager.play_ui_event("shop_open")
    ui_bad = manager.play_ui_event("missing_event")
    ambient = manager.start_ambient_facility()
    ambient_same = manager.start_ambient_facility()
    stopped = manager.stop_ambient_facility()
    stopped_again = manager.stop_ambient_facility()

    active_sound_names = {evt.sound_name for evt in engine.active_events}
    assert footstep_walk != footstep_run
    assert bot_fire != bot_death
    assert pickup is not None
    assert ui_open is not None
    assert ui_bad is None
    assert ambient == ambient_same
    assert stopped is True
    assert stopped_again is False
    assert "footstep_walk" in active_sound_names
    assert "footstep_run" in active_sound_names
    assert "bot_shot" in active_sound_names
    assert "bot_death" in active_sound_names
    assert "money_pickup" in active_sound_names
    assert "ui_shop_open" in active_sound_names


def test_sound_manager_rpg_fire_plays_pre_crash_cue_before_main_shot():
    engine = AudioEngine()
    manager = SoundManager(engine=engine)

    manager.play_weapon_fire("RPG")

    weapon_events = [evt for evt in engine.active_events if evt.channel == "weapon"]
    assert len(weapon_events) == 2
    assert weapon_events[0].sound_name == "rpg_pre_crash_warning"
    assert weapon_events[1].sound_name == "shot_rpg"


def test_sound_manager_supports_glitch_sequence_cues():
    engine = AudioEngine()
    manager = SoundManager(engine=engine)

    manager.play_glitch_transition_cue()
    manager.play_glitch_crash_impact_cue()
    manager.play_glitch_recovery_cue()

    glitch_events = [evt.sound_name for evt in engine.active_events if evt.channel == "glitch"]
    assert glitch_events == [
        "glitch_transition_ramp",
        "glitch_crash_impact",
        "glitch_recovery_confirm",
    ]
