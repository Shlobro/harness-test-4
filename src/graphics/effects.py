"""Simple gameplay-oriented visual effects for shooting and damage feedback."""

from __future__ import annotations

from dataclasses import dataclass


Vector3 = tuple[float, float, float]
ColorRGB = tuple[int, int, int]


@dataclass(frozen=True)
class Particle:
    """One particle sample for host-engine emitters."""

    position: Vector3
    velocity: Vector3
    color: ColorRGB
    lifetime_seconds: float
    size: float


class MuzzleFlashEffectSystem:
    """Build deterministic muzzle-flash particle bursts."""

    def spawn(self, position: Vector3, forward: Vector3) -> list[Particle]:
        return [
            Particle(position, _scaled(forward, 6.5), (255, 210, 90), 0.08, 0.18),
            Particle(position, _scaled(forward, 5.4), (255, 180, 50), 0.11, 0.14),
            Particle(position, _combine(forward, (0.08, 0.15, 0.05), 4.2), (255, 240, 150), 0.07, 0.09),
            Particle(position, _combine(forward, (-0.1, 0.07, -0.06), 3.8), (255, 230, 120), 0.07, 0.1),
        ]


@dataclass(frozen=True)
class ExplosionEffect:
    """Structured explosion payload for RPG detonations."""

    center: Vector3
    radius: float
    particles: tuple[Particle, ...]


class ExplosionEffectSystem:
    """Build deterministic radial explosion particle sets."""

    def spawn(self, center: Vector3) -> ExplosionEffect:
        velocity_offsets = (
            (0.0, 1.0, 0.0),
            (0.8, 0.6, 0.2),
            (-0.7, 0.5, 0.4),
            (0.5, 0.45, -0.8),
            (-0.4, 0.7, -0.6),
            (0.2, 0.4, 0.9),
        )
        particles = tuple(
            Particle(
                position=center,
                velocity=_scaled(offset, 7.0),
                color=(255, 140 - index * 12, 30 + index * 8),
                lifetime_seconds=0.25 + index * 0.03,
                size=0.24 - index * 0.02,
            )
            for index, offset in enumerate(velocity_offsets)
        )
        return ExplosionEffect(center=center, radius=4.5, particles=particles)


@dataclass(frozen=True)
class HitFeedbackSnapshot:
    """Transient overlay/shake payload after taking damage."""

    tint_color: ColorRGB
    intensity: float
    camera_shake: float
    is_active: bool


@dataclass
class HitFeedbackSystem:
    """Tracks and decays damage feedback values."""

    decay_per_second: float = 2.4
    _intensity: float = 0.0

    def register_hit(self, damage_amount: int) -> None:
        if damage_amount <= 0:
            raise ValueError("damage_amount must be positive.")
        self._intensity = min(1.0, self._intensity + damage_amount / 120.0)

    def step(self, delta_time: float) -> None:
        if delta_time < 0:
            raise ValueError("delta_time cannot be negative.")
        self._intensity = max(0.0, self._intensity - self.decay_per_second * delta_time)

    def snapshot(self) -> HitFeedbackSnapshot:
        return HitFeedbackSnapshot(
            tint_color=(220, 24, 24),
            intensity=self._intensity,
            camera_shake=self._intensity * 0.45,
            is_active=self._intensity > 0.0,
        )


def _scaled(vector: Vector3, scale: float) -> Vector3:
    return (vector[0] * scale, vector[1] * scale, vector[2] * scale)


def _combine(base: Vector3, offset: Vector3, scale: float) -> Vector3:
    return (
        (base[0] + offset[0]) * scale,
        (base[1] + offset[1]) * scale,
        (base[2] + offset[2]) * scale,
    )
