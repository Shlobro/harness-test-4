"""First-person camera state and mouse-look handling."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FirstPersonCamera:
    """Tracks first-person yaw/pitch with clamped vertical look."""

    yaw: float = 0.0
    pitch: float = 0.0
    min_pitch: float = -89.0
    max_pitch: float = 89.0
    eye_height: float = 1.8

    def apply_look_delta(self, look_yaw: float, look_pitch: float) -> tuple[float, float]:
        self.yaw += look_yaw
        self.pitch += look_pitch
        self.pitch = max(self.min_pitch, min(self.max_pitch, self.pitch))
        return self.yaw, self.pitch
