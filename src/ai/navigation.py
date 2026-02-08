"""Waypoint-based pathfinding helpers for bots."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from math import sqrt


Vector3 = tuple[float, float, float]


def _distance(a: Vector3, b: Vector3) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return sqrt((dx * dx) + (dy * dy) + (dz * dz))


@dataclass
class WaypointPathfinder:
    """Graph pathfinding over named waypoints using shortest hop count."""

    waypoints: dict[str, Vector3]
    links: dict[str, list[str]]

    def nearest_waypoint(self, position: Vector3) -> str:
        if not self.waypoints:
            raise ValueError("No waypoints configured.")
        return min(
            self.waypoints.keys(),
            key=lambda waypoint_id: _distance(position, self.waypoints[waypoint_id]),
        )

    def find_path(self, start_position: Vector3, goal_position: Vector3) -> list[Vector3]:
        """Find a path between nearest start/goal waypoints via BFS."""
        start_id = self.nearest_waypoint(start_position)
        goal_id = self.nearest_waypoint(goal_position)
        if start_id == goal_id:
            return [self.waypoints[start_id]]

        frontier: deque[str] = deque([start_id])
        came_from: dict[str, str | None] = {start_id: None}

        while frontier:
            current = frontier.popleft()
            if current == goal_id:
                break
            for neighbor in self.links.get(current, []):
                if neighbor in came_from:
                    continue
                came_from[neighbor] = current
                frontier.append(neighbor)

        if goal_id not in came_from:
            return []

        waypoint_ids: list[str] = []
        crawl: str | None = goal_id
        while crawl is not None:
            waypoint_ids.append(crawl)
            crawl = came_from[crawl]
        waypoint_ids.reverse()
        return [self.waypoints[waypoint_id] for waypoint_id in waypoint_ids]
