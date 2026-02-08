"""Player movement with collision detection against world geometry."""

from __future__ import annotations

import math
from dataclasses import dataclass

from src.core.collision import AABB, CollisionWorld


@dataclass
class PlayerMovementController:
    """Moves a player in local-space input while resolving collisions."""

    walk_speed: float
    collider_half_size: tuple[float, float, float] = (0.35, 0.9, 0.35)

    def move(
        self,
        *,
        player_position: tuple[float, float, float],
        player_yaw_degrees: float,
        move_x: float,
        move_z: float,
        delta_time: float,
        collision_world: CollisionWorld,
    ) -> tuple[float, float, float]:
        if delta_time <= 0.0:
            return player_position

        yaw_rad = math.radians(player_yaw_degrees)
        forward = (math.sin(yaw_rad), 0.0, math.cos(yaw_rad))
        right = (math.cos(yaw_rad), 0.0, -math.sin(yaw_rad))
        move_dir = (
            (right[0] * move_x) + (forward[0] * move_z),
            0.0,
            (right[2] * move_x) + (forward[2] * move_z),
        )
        length = math.sqrt((move_dir[0] * move_dir[0]) + (move_dir[2] * move_dir[2]))
        if length > 0:
            move_dir = (move_dir[0] / length, 0.0, move_dir[2] / length)

        displacement = (
            move_dir[0] * self.walk_speed * delta_time,
            0.0,
            move_dir[2] * self.walk_speed * delta_time,
        )
        proposed = (
            player_position[0] + displacement[0],
            player_position[1],
            player_position[2] + displacement[2],
        )

        if self._is_valid_position(proposed, collision_world):
            return proposed

        slide_x = (
            player_position[0] + displacement[0],
            player_position[1],
            player_position[2],
        )
        if self._is_valid_position(slide_x, collision_world):
            return slide_x

        slide_z = (
            player_position[0],
            player_position[1],
            player_position[2] + displacement[2],
        )
        if self._is_valid_position(slide_z, collision_world):
            return slide_z
        return player_position

    def _is_valid_position(self, position: tuple[float, float, float], world: CollisionWorld) -> bool:
        half_x, half_y, half_z = self.collider_half_size
        box = AABB(
            min_corner=(position[0] - half_x, position[1] - half_y, position[2] - half_z),
            max_corner=(position[0] + half_x, position[1] + half_y, position[2] + half_z),
        )
        if world.outside_world_bounds(box):
            return False
        return not world.collides_with_wall(box)
