"""Transition logic and visual effect state for the glitch/crash sequence."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from src.glitch.bsod import FakeCrashScreen, build_fake_bsod_screen


class GlitchPhase(str, Enum):
    """Top-level phases for the glitch sequence timeline."""

    IDLE = "idle"
    TRANSITION = "transition"
    CRASH_SCREEN = "crash_screen"
    RECOVERING = "recovering"


class GlitchAudioCue(str, Enum):
    """Discrete audio cues emitted during glitch sequence progression."""

    TRANSITION_RAMP = "transition_ramp"
    CRASH_IMPACT = "crash_impact"
    RECOVERY_CONFIRM = "recovery_confirm"


@dataclass(frozen=True)
class GlitchVisualEffects:
    """Render-facing values for pre-crash visual disruption."""

    shake_strength: float = 0.0
    distortion_amount: float = 0.0
    static_amount: float = 0.0
    chromatic_aberration: float = 0.0
    brightness_pulse: float = 0.0


@dataclass(frozen=True)
class GlitchSequenceConfig:
    """Timing controls for transition and recovery behavior."""

    transition_seconds: float = 1.2
    recovery_seconds: float = 0.25


@dataclass
class GlitchSequenceController:
    """Controls RPG-triggered transition into and out of the fake crash state."""

    config: GlitchSequenceConfig = field(default_factory=GlitchSequenceConfig)
    phase: GlitchPhase = GlitchPhase.IDLE
    crash_screen: FakeCrashScreen = field(default_factory=build_fake_bsod_screen)
    started_at: float | None = None
    recovering_at: float | None = None
    _pending_audio_cues: list[GlitchAudioCue] = field(default_factory=list)

    @property
    def is_crash_screen_visible(self) -> bool:
        return self.phase == GlitchPhase.CRASH_SCREEN

    @property
    def should_lock_gameplay(self) -> bool:
        return self.phase in (GlitchPhase.TRANSITION, GlitchPhase.CRASH_SCREEN, GlitchPhase.RECOVERING)

    def start_transition(self, now: float) -> bool:
        """Start pre-crash transition if currently idle."""
        if self.phase != GlitchPhase.IDLE:
            return False
        self.phase = GlitchPhase.TRANSITION
        self.started_at = now
        self.recovering_at = None
        self._pending_audio_cues.append(GlitchAudioCue.TRANSITION_RAMP)
        return True

    def trigger_from_weapon(self, weapon: object, now: float) -> bool:
        """Consume RPG crash trigger flag from weapon-like objects."""
        if not getattr(weapon, "crash_triggered", False):
            return False
        started = self.start_transition(now)
        if started and hasattr(weapon, "crash_triggered"):
            weapon.crash_triggered = False
        return started

    def update(self, now: float) -> GlitchVisualEffects:
        """Advance timeline and return current transition effects."""
        if self.phase == GlitchPhase.IDLE:
            return GlitchVisualEffects()
        if self.phase == GlitchPhase.RECOVERING:
            return GlitchVisualEffects()
        if self.phase == GlitchPhase.CRASH_SCREEN:
            return GlitchVisualEffects(
                shake_strength=1.0,
                distortion_amount=1.0,
                static_amount=1.0,
                chromatic_aberration=0.8,
                brightness_pulse=0.25,
            )
        if self.started_at is None:
            self.started_at = now
        elapsed = max(0.0, now - self.started_at)
        progress = min(1.0, elapsed / self.config.transition_seconds)
        if progress >= 1.0:
            self.phase = GlitchPhase.CRASH_SCREEN
            self._pending_audio_cues.append(GlitchAudioCue.CRASH_IMPACT)
            return self.update(now)
        ramp = progress * progress
        return GlitchVisualEffects(
            shake_strength=ramp,
            distortion_amount=min(1.0, ramp * 1.15),
            static_amount=min(1.0, progress * 0.9),
            chromatic_aberration=min(1.0, ramp * 0.85),
            brightness_pulse=progress * 0.2,
        )

    def request_recover(self, now: float, pressed_keys: set[str]) -> bool:
        """Begin recovery after crash screen when accepted keys are pressed."""
        normalized = {key.lower() for key in pressed_keys}
        if self.phase != GlitchPhase.CRASH_SCREEN:
            return False
        if not normalized.intersection({"enter", "escape", "esc", "r"}):
            return False
        self.phase = GlitchPhase.RECOVERING
        self.recovering_at = now
        self._pending_audio_cues.append(GlitchAudioCue.RECOVERY_CONFIRM)
        return True

    def complete_recovery_if_ready(self, now: float) -> bool:
        """Reset sequence back to idle once recovery cooldown has elapsed."""
        if self.phase != GlitchPhase.RECOVERING:
            return False
        if self.recovering_at is None:
            self.recovering_at = now
        if (now - self.recovering_at) < self.config.recovery_seconds:
            return False
        self.phase = GlitchPhase.IDLE
        self.started_at = None
        self.recovering_at = None
        return True

    def consume_audio_cues(self) -> list[GlitchAudioCue]:
        """Return pending sequence cues and clear queue."""
        cues = list(self._pending_audio_cues)
        self._pending_audio_cues.clear()
        return cues
