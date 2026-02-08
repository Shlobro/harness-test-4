"""Projectile simulation with world collision detection."""

from __future__ import annotations

from dataclasses import dataclass

from src.core.collision import AABB, CollisionWorld
from src.projectiles.projectile import Projectile


@dataclass
class ProjectilePhysicsSystem:
    """Advances projectiles and deactivates on world collision."""

    def step(self, projectiles: list[Projectile], delta_time: float, world: CollisionWorld) -> int:
        collision_count = 0
        for projectile in projectiles:
            if not projectile.is_active:
                continue
            projectile.advance(delta_time)
            if not projectile.is_active:
                continue
            projectile_box = AABB(
                min_corner=(
                    projectile.position[0] - projectile.radius,
                    projectile.position[1] - projectile.radius,
                    projectile.position[2] - projectile.radius,
                ),
                max_corner=(
                    projectile.position[0] + projectile.radius,
                    projectile.position[1] + projectile.radius,
                    projectile.position[2] + projectile.radius,
                ),
            )
            if world.outside_world_bounds(projectile_box) or world.collides_with_wall(projectile_box):
                projectile.is_active = False
                collision_count += 1
        return collision_count
