"""Rendering context configuration for 3D runtime integration."""

from __future__ import annotations

from dataclasses import dataclass


ColorRGB = tuple[int, int, int]


@dataclass(frozen=True)
class RenderSettings:
    """Engine-facing rendering setup values."""

    width: int = 1280
    height: int = 720
    title: str = "FPS Bot Arena"
    field_of_view_degrees: float = 85.0
    near_plane: float = 0.05
    far_plane: float = 300.0
    clear_color: ColorRGB = (14, 16, 20)


@dataclass
class RenderingContext:
    """Mutable rendering lifecycle state."""

    settings: RenderSettings
    is_initialized: bool = False
    active_scene_id: str | None = None

    def initialize(self) -> None:
        """Mark the context initialized by the host engine layer."""
        self.is_initialized = True

    def bind_scene(self, scene_id: str) -> None:
        """Set the active scene used for rendering."""
        if not self.is_initialized:
            raise RuntimeError("Rendering context must be initialized before binding a scene.")
        self.active_scene_id = scene_id


def setup_default_rendering_context() -> RenderingContext:
    """Create and initialize the baseline FPS rendering context."""
    context = RenderingContext(settings=RenderSettings())
    context.initialize()
    context.bind_scene("arena_facility")
    return context
