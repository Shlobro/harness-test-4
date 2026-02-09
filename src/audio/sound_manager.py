"""Sound mapping for gameplay events."""

from __future__ import annotations

from dataclasses import dataclass

from src.audio.engine import AudioEngine


@dataclass(frozen=True)
class ProceduralSoundProfile:
    """Placeholder procedural profile used before final audio assets are added."""

    sound_name: str
    waveform: str
    base_frequency_hz: float
    duration_seconds: float
    attack_seconds: float
    decay_seconds: float
    noise_mix: float
    volume: float


class SoundManager:
    """Maps gameplay events to audio engine calls."""

    def __init__(self, engine: AudioEngine) -> None:
        self.engine = engine
        self.weapon_shot_profiles: dict[str, ProceduralSoundProfile] = (
            self._build_default_weapon_profiles()
        )
        self.footstep_walk_profile = ProceduralSoundProfile(
            sound_name="footstep_walk",
            waveform="noise",
            base_frequency_hz=120.0,
            duration_seconds=0.12,
            attack_seconds=0.002,
            decay_seconds=0.10,
            noise_mix=0.88,
            volume=0.35,
        )
        self.footstep_run_profile = ProceduralSoundProfile(
            sound_name="footstep_run",
            waveform="noise",
            base_frequency_hz=145.0,
            duration_seconds=0.09,
            attack_seconds=0.002,
            decay_seconds=0.08,
            noise_mix=0.90,
            volume=0.45,
        )
        self.bot_fire_profile = ProceduralSoundProfile(
            sound_name="bot_shot",
            waveform="square",
            base_frequency_hz=210.0,
            duration_seconds=0.10,
            attack_seconds=0.003,
            decay_seconds=0.09,
            noise_mix=0.36,
            volume=0.66,
        )
        self.bot_death_profile = ProceduralSoundProfile(
            sound_name="bot_death",
            waveform="saw",
            base_frequency_hz=95.0,
            duration_seconds=0.25,
            attack_seconds=0.01,
            decay_seconds=0.21,
            noise_mix=0.42,
            volume=0.72,
        )
        self.money_pickup_profile = ProceduralSoundProfile(
            sound_name="money_pickup",
            waveform="triangle",
            base_frequency_hz=660.0,
            duration_seconds=0.11,
            attack_seconds=0.002,
            decay_seconds=0.10,
            noise_mix=0.08,
            volume=0.55,
        )
        self.ui_profiles: dict[str, ProceduralSoundProfile] = {
            "shop_open": ProceduralSoundProfile(
                sound_name="ui_shop_open",
                waveform="sine",
                base_frequency_hz=420.0,
                duration_seconds=0.10,
                attack_seconds=0.004,
                decay_seconds=0.08,
                noise_mix=0.03,
                volume=0.40,
            ),
            "shop_close": ProceduralSoundProfile(
                sound_name="ui_shop_close",
                waveform="sine",
                base_frequency_hz=340.0,
                duration_seconds=0.09,
                attack_seconds=0.004,
                decay_seconds=0.08,
                noise_mix=0.03,
                volume=0.38,
            ),
            "purchase_success": ProceduralSoundProfile(
                sound_name="ui_purchase_success",
                waveform="triangle",
                base_frequency_hz=520.0,
                duration_seconds=0.12,
                attack_seconds=0.003,
                decay_seconds=0.11,
                noise_mix=0.06,
                volume=0.52,
            ),
            "purchase_fail": ProceduralSoundProfile(
                sound_name="ui_purchase_fail",
                waveform="square",
                base_frequency_hz=180.0,
                duration_seconds=0.10,
                attack_seconds=0.003,
                decay_seconds=0.09,
                noise_mix=0.18,
                volume=0.48,
            ),
        }
        self.ambient_facility_profile = ProceduralSoundProfile(
            sound_name="ambient_facility_hum",
            waveform="sine",
            base_frequency_hz=62.0,
            duration_seconds=2.0,
            attack_seconds=0.3,
            decay_seconds=0.4,
            noise_mix=0.15,
            volume=0.22,
        )
        self.rpg_pre_crash_profile = ProceduralSoundProfile(
            sound_name="rpg_pre_crash_warning",
            waveform="saw",
            base_frequency_hz=310.0,
            duration_seconds=0.18,
            attack_seconds=0.004,
            decay_seconds=0.16,
            noise_mix=0.35,
            volume=0.78,
        )
        self.glitch_transition_profile = ProceduralSoundProfile(
            sound_name="glitch_transition_ramp",
            waveform="saw",
            base_frequency_hz=145.0,
            duration_seconds=0.35,
            attack_seconds=0.01,
            decay_seconds=0.22,
            noise_mix=0.46,
            volume=0.82,
        )
        self.glitch_crash_impact_profile = ProceduralSoundProfile(
            sound_name="glitch_crash_impact",
            waveform="noise",
            base_frequency_hz=58.0,
            duration_seconds=0.48,
            attack_seconds=0.002,
            decay_seconds=0.38,
            noise_mix=0.86,
            volume=1.0,
        )
        self.glitch_recovery_profile = ProceduralSoundProfile(
            sound_name="glitch_recovery_confirm",
            waveform="triangle",
            base_frequency_hz=390.0,
            duration_seconds=0.16,
            attack_seconds=0.002,
            decay_seconds=0.12,
            noise_mix=0.1,
            volume=0.64,
        )
        self._ambient_event_id: str | None = None

    def _build_default_weapon_profiles(self) -> dict[str, ProceduralSoundProfile]:
        return {
            "Pistol": ProceduralSoundProfile(
                sound_name="shot_pistol",
                waveform="square",
                base_frequency_hz=190.0,
                duration_seconds=0.10,
                attack_seconds=0.005,
                decay_seconds=0.09,
                noise_mix=0.32,
                volume=0.72,
            ),
            "Shotgun": ProceduralSoundProfile(
                sound_name="shot_shotgun",
                waveform="noise",
                base_frequency_hz=110.0,
                duration_seconds=0.22,
                attack_seconds=0.003,
                decay_seconds=0.20,
                noise_mix=0.75,
                volume=0.95,
            ),
            "AssaultRifle": ProceduralSoundProfile(
                sound_name="shot_assault_rifle",
                waveform="saw",
                base_frequency_hz=240.0,
                duration_seconds=0.08,
                attack_seconds=0.002,
                decay_seconds=0.07,
                noise_mix=0.40,
                volume=0.68,
            ),
            "RPG": ProceduralSoundProfile(
                sound_name="shot_rpg",
                waveform="sine",
                base_frequency_hz=70.0,
                duration_seconds=0.45,
                attack_seconds=0.01,
                decay_seconds=0.35,
                noise_mix=0.62,
                volume=1.0,
            ),
        }

    def get_weapon_shot_profile(self, weapon_name: str) -> ProceduralSoundProfile | None:
        return self.weapon_shot_profiles.get(weapon_name)

    def get_ui_profile(self, ui_event: str) -> ProceduralSoundProfile | None:
        return self.ui_profiles.get(ui_event)

    def play_weapon_fire(self, weapon_name: str) -> str | None:
        profile = self.get_weapon_shot_profile(weapon_name)
        if profile is None:
            return None
        if weapon_name == "RPG":
            self.play_rpg_pre_crash_cue()
        return self.engine.play(sound_name=profile.sound_name, channel="weapon", loop=False)

    def play_footstep(self, *, is_running: bool = False) -> str:
        profile = self.footstep_run_profile if is_running else self.footstep_walk_profile
        return self.engine.play(sound_name=profile.sound_name, channel="movement", loop=False)

    def play_bot_fire(self) -> str:
        return self.engine.play(sound_name=self.bot_fire_profile.sound_name, channel="enemy", loop=False)

    def play_bot_death(self) -> str:
        return self.engine.play(sound_name=self.bot_death_profile.sound_name, channel="enemy", loop=False)

    def play_money_pickup(self) -> str:
        return self.engine.play(sound_name=self.money_pickup_profile.sound_name, channel="economy", loop=False)

    def play_ui_event(self, ui_event: str) -> str | None:
        profile = self.get_ui_profile(ui_event)
        if profile is None:
            return None
        return self.engine.play(sound_name=profile.sound_name, channel="ui", loop=False)

    def start_ambient_facility(self) -> str:
        if self._ambient_event_id is not None:
            return self._ambient_event_id
        self._ambient_event_id = self.engine.play(
            sound_name=self.ambient_facility_profile.sound_name,
            channel="ambient",
            loop=True,
        )
        return self._ambient_event_id

    def stop_ambient_facility(self) -> bool:
        if self._ambient_event_id is None:
            return False
        stopped = self.engine.stop(self._ambient_event_id)
        self._ambient_event_id = None
        return stopped

    def play_rpg_pre_crash_cue(self) -> str:
        return self.engine.play(sound_name=self.rpg_pre_crash_profile.sound_name, channel="weapon", loop=False)

    def play_glitch_transition_cue(self) -> str:
        return self.engine.play(
            sound_name=self.glitch_transition_profile.sound_name,
            channel="glitch",
            loop=False,
        )

    def play_glitch_crash_impact_cue(self) -> str:
        return self.engine.play(
            sound_name=self.glitch_crash_impact_profile.sound_name,
            channel="glitch",
            loop=False,
        )

    def play_glitch_recovery_cue(self) -> str:
        return self.engine.play(
            sound_name=self.glitch_recovery_profile.sound_name,
            channel="glitch",
            loop=False,
        )
