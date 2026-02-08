"""Input translation for keyboard movement and mouse look."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InputSnapshot:
    """Raw frame input values from platform layer."""

    pressed_keys: set[str]
    mouse_delta_x: float = 0.0
    mouse_delta_y: float = 0.0


@dataclass(frozen=True)
class InputFrame:
    """Normalized input values consumed by gameplay systems."""

    move_x: float
    move_z: float
    look_yaw: float
    look_pitch: float


class InputHandler:
    """Normalizes raw control inputs into movement/look values."""

    def __init__(self, mouse_sensitivity: float) -> None:
        self.mouse_sensitivity = mouse_sensitivity

    def build_frame(self, snapshot: InputSnapshot) -> InputFrame:
        """Compute movement axis values and scaled look deltas."""
        move_x = self._axis(snapshot.pressed_keys, positive="d", negative="a")
        move_z = self._axis(snapshot.pressed_keys, positive="w", negative="s")
        look_yaw = snapshot.mouse_delta_x * self.mouse_sensitivity
        look_pitch = -snapshot.mouse_delta_y * self.mouse_sensitivity

        return InputFrame(
            move_x=move_x,
            move_z=move_z,
            look_yaw=look_yaw,
            look_pitch=look_pitch,
        )

    @staticmethod
    def _axis(keys: set[str], positive: str, negative: str) -> float:
        if positive in keys and negative in keys:
            return 0.0
        if positive in keys:
            return 1.0
        if negative in keys:
            return -1.0
        return 0.0

