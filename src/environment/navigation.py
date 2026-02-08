"""Environment navigation helpers."""

from __future__ import annotations

from src.ai.navigation import WaypointPathfinder
from src.environment.facility import FacilityLayout


def build_waypoint_pathfinder(layout: FacilityLayout) -> WaypointPathfinder:
    """Create a validated waypoint pathfinder from facility data."""
    for node_id, neighbors in layout.waypoint_links.items():
        if node_id not in layout.waypoints:
            raise ValueError(f"Waypoint link source '{node_id}' is undefined.")
        for neighbor in neighbors:
            if neighbor not in layout.waypoints:
                raise ValueError(f"Waypoint link target '{neighbor}' is undefined.")
    return WaypointPathfinder(
        waypoints=dict(layout.waypoints),
        links={node_id: list(neighbors) for node_id, neighbors in layout.waypoint_links.items()},
    )
