"""Indoor facility layout primitives used by environment and AI systems."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Literal


Vector3 = tuple[float, float, float]


@dataclass(frozen=True)
class Room:
    """Axis-aligned rectangular room footprint."""

    room_id: str
    min_x: float
    max_x: float
    min_z: float
    max_z: float
    floor_y: float = 0.0

    @property
    def center(self) -> Vector3:
        return (
            (self.min_x + self.max_x) * 0.5,
            self.floor_y,
            (self.min_z + self.max_z) * 0.5,
        )


@dataclass(frozen=True)
class Doorway:
    """Opening between two rooms along a shared wall."""

    doorway_id: str
    room_a: str
    room_b: str
    wall_axis: Literal["x", "z"]
    wall_value: float
    center: float
    width: float

    @property
    def span_min(self) -> float:
        return self.center - (self.width * 0.5)

    @property
    def span_max(self) -> float:
        return self.center + (self.width * 0.5)


@dataclass(frozen=True)
class CoverObject:
    """Simple geometric cover object represented as an AABB prism."""

    cover_id: str
    kind: Literal["crate", "pillar", "barrier"]
    min_corner: Vector3
    max_corner: Vector3
    blocks_movement: bool = True

    @property
    def center(self) -> Vector3:
        return (
            (self.min_corner[0] + self.max_corner[0]) * 0.5,
            (self.min_corner[1] + self.max_corner[1]) * 0.5,
            (self.min_corner[2] + self.max_corner[2]) * 0.5,
        )


@dataclass(frozen=True)
class SpawnPoint:
    """Named spawn point for player or bots."""

    spawn_id: str
    position: Vector3
    team: Literal["player", "bot"]


@dataclass(frozen=True)
class LightingSetup:
    """Engine-agnostic lighting profile for the facility."""

    ambient_color: tuple[float, float, float]
    ambient_intensity: float
    directional_color: tuple[float, float, float]
    directional_intensity: float
    directional_direction: Vector3


@dataclass(frozen=True)
class FacilityLayout:
    """Complete facility definition used by environment and AI systems."""

    rooms: dict[str, Room]
    doorways: list[Doorway]
    cover_objects: list[CoverObject]
    waypoints: dict[str, Vector3]
    waypoint_links: dict[str, list[str]]
    spawn_points: list[SpawnPoint]
    lighting: LightingSetup
    wall_height: float = 3.0

    def room_ids(self) -> set[str]:
        return set(self.rooms.keys())

    def doorway_graph(self) -> dict[str, set[str]]:
        graph: dict[str, set[str]] = {room_id: set() for room_id in self.rooms}
        for doorway in self.doorways:
            graph.setdefault(doorway.room_a, set()).add(doorway.room_b)
            graph.setdefault(doorway.room_b, set()).add(doorway.room_a)
        return graph

    def connected_room_ids(self, start_room_id: str) -> set[str]:
        """Return every room reachable from a starting room through doorways."""
        if start_room_id not in self.rooms:
            raise ValueError(f"Unknown room_id '{start_room_id}'.")
        graph = self.doorway_graph()
        visited: set[str] = set()
        frontier = [start_room_id]
        while frontier:
            room_id = frontier.pop()
            if room_id in visited:
                continue
            visited.add(room_id)
            for neighbor in graph.get(room_id, set()):
                if neighbor not in visited:
                    frontier.append(neighbor)
        return visited

    def find_room_for_position(self, position: Vector3) -> str | None:
        x, _, z = position
        for room in self.rooms.values():
            if room.min_x <= x <= room.max_x and room.min_z <= z <= room.max_z:
                return room.room_id
        return None

    def bot_spawn_positions(self) -> list[Vector3]:
        return [spawn.position for spawn in self.spawn_points if spawn.team == "bot"]

    def player_spawn_position(self) -> Vector3:
        for spawn in self.spawn_points:
            if spawn.team == "player":
                return spawn.position
        raise ValueError("Facility layout must define one player spawn point.")

    def lighting_direction_length(self) -> float:
        direction = self.lighting.directional_direction
        return sqrt(
            (direction[0] * direction[0])
            + (direction[1] * direction[1])
            + (direction[2] * direction[2])
        )

    def validate(self) -> None:
        """Validate doorway/spawn/lighting integrity for runtime safety."""
        room_ids = self.room_ids()
        for doorway in self.doorways:
            if doorway.room_a not in room_ids or doorway.room_b not in room_ids:
                raise ValueError(f"Doorway '{doorway.doorway_id}' links undefined rooms.")
            if doorway.width <= 0.0:
                raise ValueError(f"Doorway '{doorway.doorway_id}' width must be positive.")

        player_spawns = [spawn for spawn in self.spawn_points if spawn.team == "player"]
        if len(player_spawns) != 1:
            raise ValueError("Facility layout must define exactly one player spawn.")
        bot_spawns = [spawn for spawn in self.spawn_points if spawn.team == "bot"]
        if not bot_spawns:
            raise ValueError("Facility layout must define at least one bot spawn.")
        for spawn in self.spawn_points:
            if self.find_room_for_position(spawn.position) is None:
                raise ValueError(f"Spawn point '{spawn.spawn_id}' is outside all rooms.")

        if self.lighting.ambient_intensity < 0.0 or self.lighting.directional_intensity < 0.0:
            raise ValueError("Lighting intensities must be non-negative.")
        if self.lighting_direction_length() <= 0.0:
            raise ValueError("Directional lighting direction must be non-zero.")

        # Distinct-room requirement for tactical variety.
        if len(self.rooms) < 3:
            raise ValueError("Facility layout must define at least three rooms.")
        for room in self.rooms.values():
            if room.max_x <= room.min_x or room.max_z <= room.min_z:
                raise ValueError(f"Room '{room.room_id}' has invalid dimensions.")


def create_default_facility_layout() -> FacilityLayout:
    """Return a 5-room tactical facility with doorways, cover, and nav data."""
    rooms = {
        "lobby": Room("lobby", min_x=-12.0, max_x=-4.0, min_z=-8.0, max_z=8.0),
        "central_hall": Room("central_hall", min_x=-4.0, max_x=4.0, min_z=-10.0, max_z=10.0),
        "storage": Room("storage", min_x=4.0, max_x=12.0, min_z=-10.0, max_z=-2.0),
        "lab": Room("lab", min_x=4.0, max_x=12.0, min_z=2.0, max_z=10.0),
        "security": Room("security", min_x=-12.0, max_x=-4.0, min_z=-14.0, max_z=-8.0),
    }

    doorways = [
        Doorway(
            doorway_id="lobby_to_central",
            room_a="lobby",
            room_b="central_hall",
            wall_axis="x",
            wall_value=-4.0,
            center=0.0,
            width=3.0,
        ),
        Doorway(
            doorway_id="central_to_storage",
            room_a="central_hall",
            room_b="storage",
            wall_axis="x",
            wall_value=4.0,
            center=-6.0,
            width=3.0,
        ),
        Doorway(
            doorway_id="central_to_lab",
            room_a="central_hall",
            room_b="lab",
            wall_axis="x",
            wall_value=4.0,
            center=6.0,
            width=3.0,
        ),
        Doorway(
            doorway_id="lobby_to_security",
            room_a="lobby",
            room_b="security",
            wall_axis="z",
            wall_value=-8.0,
            center=-8.0,
            width=3.0,
        ),
    ]

    cover_objects = [
        CoverObject(
            cover_id="lobby_crates",
            kind="crate",
            min_corner=(-10.5, 0.0, -1.8),
            max_corner=(-8.8, 1.5, -0.1),
        ),
        CoverObject(
            cover_id="hall_pillar",
            kind="pillar",
            min_corner=(-0.9, 0.0, -0.9),
            max_corner=(0.9, 2.8, 0.9),
        ),
        CoverObject(
            cover_id="storage_barrier",
            kind="barrier",
            min_corner=(6.0, 0.0, -6.9),
            max_corner=(9.8, 1.3, -5.8),
        ),
        CoverObject(
            cover_id="lab_crates",
            kind="crate",
            min_corner=(7.2, 0.0, 5.0),
            max_corner=(9.0, 1.6, 6.8),
        ),
        CoverObject(
            cover_id="security_barrier",
            kind="barrier",
            min_corner=(-9.6, 0.0, -11.2),
            max_corner=(-6.4, 1.4, -10.1),
        ),
    ]

    waypoints = {
        "wp_lobby": (-8.0, 0.0, 0.0),
        "wp_lobby_door": (-4.2, 0.0, 0.0),
        "wp_central": (0.0, 0.0, 0.0),
        "wp_storage_door": (4.2, 0.0, -6.0),
        "wp_storage": (8.0, 0.0, -6.0),
        "wp_lab_door": (4.2, 0.0, 6.0),
        "wp_lab": (8.0, 0.0, 6.0),
        "wp_security_door": (-8.0, 0.0, -8.2),
        "wp_security": (-8.0, 0.0, -11.0),
    }
    waypoint_links = {
        "wp_lobby": ["wp_lobby_door", "wp_security_door"],
        "wp_lobby_door": ["wp_lobby", "wp_central"],
        "wp_central": ["wp_lobby_door", "wp_storage_door", "wp_lab_door"],
        "wp_storage_door": ["wp_central", "wp_storage"],
        "wp_storage": ["wp_storage_door"],
        "wp_lab_door": ["wp_central", "wp_lab"],
        "wp_lab": ["wp_lab_door"],
        "wp_security_door": ["wp_lobby", "wp_security"],
        "wp_security": ["wp_security_door"],
    }

    spawn_points = [
        SpawnPoint("spawn_player", position=(-9.0, 0.0, 3.0), team="player"),
        SpawnPoint("spawn_bot_lobby", position=(-9.5, 0.0, -3.0), team="bot"),
        SpawnPoint("spawn_bot_storage", position=(9.0, 0.0, -7.8), team="bot"),
        SpawnPoint("spawn_bot_lab", position=(8.7, 0.0, 7.8), team="bot"),
        SpawnPoint("spawn_bot_security", position=(-8.0, 0.0, -12.0), team="bot"),
        SpawnPoint("spawn_bot_central", position=(0.0, 0.0, 8.0), team="bot"),
    ]

    lighting = LightingSetup(
        ambient_color=(0.68, 0.72, 0.78),
        ambient_intensity=0.42,
        directional_color=(1.0, 0.96, 0.9),
        directional_intensity=0.82,
        directional_direction=(-0.6, -1.0, -0.3),
    )

    layout = FacilityLayout(
        rooms=rooms,
        doorways=doorways,
        cover_objects=cover_objects,
        waypoints=waypoints,
        waypoint_links=waypoint_links,
        spawn_points=spawn_points,
        lighting=lighting,
    )
    layout.validate()
    return layout
