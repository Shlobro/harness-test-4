# Environment Developer Guide

## Purpose
`src/environment/` defines the indoor facility layout and turns that layout into reusable collision and navigation data.

## Files
- `facility.py`: dataclasses for rooms, doorways, cover objects, spawn points, and lighting; includes `create_default_facility_layout()` with a 5-room tactical facility.
- `collision.py`: converts room boundaries + doorway openings + blocking cover into a `CollisionWorld` for player and projectile collision.
- `navigation.py`: validates layout waypoint links and creates a `WaypointPathfinder`.
- `__init__.py`: package exports for facility, collision, and navigation helpers.

## Layout Contents
- Five distinct rooms: `lobby`, `central_hall`, `storage`, `lab`, and `security`.
- Doorway connectivity between rooms via explicit `Doorway` records.
- Distributed cover objects (`crate`, `pillar`, `barrier`) represented as AABB prisms.
- Waypoint graph and links for AI route planning.
- Spawn point records for player and bots.
- Engine-agnostic ambient + directional lighting profile.

## Integration Notes
- Build runtime collision data with `build_collision_world(layout)` and pass it to movement/projectile systems.
- Build AI pathfinding with `build_waypoint_pathfinder(layout)` to keep navigation synced with room geometry.
- Keep room and doorway geometry in `facility.py` as the single source of truth for environment updates.
