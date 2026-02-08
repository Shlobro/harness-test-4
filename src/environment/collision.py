"""Build collision volumes from a facility layout."""

from __future__ import annotations

from src.core.collision import AABB, CollisionWorld
from src.environment.facility import FacilityLayout, Room


EPSILON = 1e-5


def _interval_subtract(start: float, end: float, cuts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Subtract opening ranges from a wall segment range."""
    segments = [(start, end)]
    for cut_min, cut_max in cuts:
        if cut_max <= cut_min:
            continue
        next_segments: list[tuple[float, float]] = []
        # Split each surviving segment around the doorway opening.
        for seg_min, seg_max in segments:
            if cut_max <= seg_min or cut_min >= seg_max:
                next_segments.append((seg_min, seg_max))
                continue
            if cut_min > seg_min:
                next_segments.append((seg_min, cut_min))
            if cut_max < seg_max:
                next_segments.append((cut_max, seg_max))
        segments = next_segments
    return [(seg_min, seg_max) for seg_min, seg_max in segments if (seg_max - seg_min) > EPSILON]


def _wall_openings_for_room(layout: FacilityLayout, room: Room, axis: str, wall_value: float) -> list[tuple[float, float]]:
    openings: list[tuple[float, float]] = []
    for doorway in layout.doorways:
        if doorway.wall_axis != axis:
            continue
        if abs(doorway.wall_value - wall_value) > EPSILON:
            continue
        if doorway.room_a != room.room_id and doorway.room_b != room.room_id:
            continue
        openings.append((doorway.span_min, doorway.span_max))
    return openings


def _build_room_wall_boxes(
    *,
    layout: FacilityLayout,
    room: Room,
    wall_thickness: float,
) -> list[AABB]:
    half_thickness = wall_thickness * 0.5
    floor_y = room.floor_y
    ceiling_y = room.floor_y + layout.wall_height
    boxes: list[AABB] = []

    def add_x_wall(x_value: float, span_min: float, span_max: float) -> None:
        openings = _wall_openings_for_room(layout, room, "x", x_value)
        for cut_min, cut_max in _interval_subtract(span_min, span_max, openings):
            boxes.append(
                AABB(
                    min_corner=(x_value - half_thickness, floor_y, cut_min),
                    max_corner=(x_value + half_thickness, ceiling_y, cut_max),
                )
            )

    def add_z_wall(z_value: float, span_min: float, span_max: float) -> None:
        openings = _wall_openings_for_room(layout, room, "z", z_value)
        for cut_min, cut_max in _interval_subtract(span_min, span_max, openings):
            boxes.append(
                AABB(
                    min_corner=(cut_min, floor_y, z_value - half_thickness),
                    max_corner=(cut_max, ceiling_y, z_value + half_thickness),
                )
            )

    add_x_wall(room.min_x, room.min_z, room.max_z)
    add_x_wall(room.max_x, room.min_z, room.max_z)
    add_z_wall(room.min_z, room.min_x, room.max_x)
    add_z_wall(room.max_z, room.min_x, room.max_x)
    return boxes


def build_collision_world(
    layout: FacilityLayout,
    *,
    world_margin: float = 2.0,
    wall_thickness: float = 0.4,
) -> CollisionWorld:
    """Convert rooms/doorways/cover into a collision world for gameplay systems."""
    if wall_thickness <= 0.0:
        raise ValueError("wall_thickness must be positive.")

    static_walls: list[AABB] = []
    min_x = float("inf")
    min_y = float("inf")
    min_z = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")
    max_z = float("-inf")

    for room in layout.rooms.values():
        min_x = min(min_x, room.min_x)
        min_y = min(min_y, room.floor_y)
        min_z = min(min_z, room.min_z)
        max_x = max(max_x, room.max_x)
        max_y = max(max_y, room.floor_y + layout.wall_height)
        max_z = max(max_z, room.max_z)
        static_walls.extend(_build_room_wall_boxes(layout=layout, room=room, wall_thickness=wall_thickness))

    for cover in layout.cover_objects:
        if cover.blocks_movement:
            static_walls.append(AABB(min_corner=cover.min_corner, max_corner=cover.max_corner))

    bounds = AABB(
        min_corner=(min_x - world_margin, min_y - 1.0, min_z - world_margin),
        max_corner=(max_x + world_margin, max_y + 2.0, max_z + world_margin),
    )
    return CollisionWorld(world_bounds=bounds, static_walls=static_walls)
