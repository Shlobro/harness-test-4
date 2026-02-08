"""AABB collision primitives used by movement and projectiles."""

from __future__ import annotations

from dataclasses import dataclass


Vector3 = tuple[float, float, float]


@dataclass(frozen=True)
class AABB:
    """Axis-aligned bounding box."""

    min_corner: Vector3
    max_corner: Vector3

    def intersects(self, other: "AABB") -> bool:
        return (
            self.min_corner[0] <= other.max_corner[0]
            and self.max_corner[0] >= other.min_corner[0]
            and self.min_corner[1] <= other.max_corner[1]
            and self.max_corner[1] >= other.min_corner[1]
            and self.min_corner[2] <= other.max_corner[2]
            and self.max_corner[2] >= other.min_corner[2]
        )


@dataclass
class CollisionWorld:
    """Container for static world collision volumes."""

    world_bounds: AABB
    static_walls: list[AABB]

    def collides_with_wall(self, box: AABB) -> bool:
        return any(wall.intersects(box) for wall in self.static_walls)

    def outside_world_bounds(self, box: AABB) -> bool:
        return not (
            box.min_corner[0] >= self.world_bounds.min_corner[0]
            and box.max_corner[0] <= self.world_bounds.max_corner[0]
            and box.min_corner[1] >= self.world_bounds.min_corner[1]
            and box.max_corner[1] <= self.world_bounds.max_corner[1]
            and box.min_corner[2] >= self.world_bounds.min_corner[2]
            and box.max_corner[2] <= self.world_bounds.max_corner[2]
        )
