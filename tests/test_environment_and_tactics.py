from random import Random

from src.ai.bot import Bot
from src.ai.tactics import TacticalAction, build_flank_route, choose_tactical_action, find_cover_plan
from src.ai.waves import WaveDirector
from src.core.collision import AABB
from src.environment import build_collision_world, build_waypoint_pathfinder, create_default_facility_layout


def test_default_facility_has_five_rooms_and_doorway_connectivity():
    layout = create_default_facility_layout()
    assert len(layout.rooms) == 5
    room_ids = layout.room_ids()
    assert {"lobby", "central_hall", "storage", "lab", "security"} <= room_ids
    for doorway in layout.doorways:
        assert doorway.room_a in room_ids
        assert doorway.room_b in room_ids
    assert layout.connected_room_ids("lobby") == room_ids


def test_layout_has_spawn_points_inside_rooms_and_valid_lighting_profile():
    layout = create_default_facility_layout()
    assert layout.player_spawn_position() in [spawn.position for spawn in layout.spawn_points if spawn.team == "player"]
    assert len(layout.bot_spawn_positions()) >= 1
    for spawn in layout.spawn_points:
        assert layout.find_room_for_position(spawn.position) is not None

    assert layout.lighting.ambient_intensity >= 0.0
    assert layout.lighting.directional_intensity > 0.0
    assert layout.lighting_direction_length() > 0.0


def test_collision_world_from_layout_respects_doorway_openings_and_cover():
    layout = create_default_facility_layout()
    world = build_collision_world(layout)
    collider_half_size = (0.35, 0.9, 0.35)

    def player_box(position: tuple[float, float, float]) -> AABB:
        return AABB(
            min_corner=(
                position[0] - collider_half_size[0],
                position[1] - collider_half_size[1],
                position[2] - collider_half_size[2],
            ),
            max_corner=(
                position[0] + collider_half_size[0],
                position[1] + collider_half_size[1],
                position[2] + collider_half_size[2],
            ),
        )

    doorway_box = player_box(position=(-4.0, 0.9, 0.0))
    blocked_wall_box = player_box(position=(-4.0, 0.9, 6.0))
    cover_box = player_box(position=(0.0, 0.9, 0.0))

    assert world.collides_with_wall(doorway_box) is False
    assert world.collides_with_wall(blocked_wall_box) is True
    assert world.collides_with_wall(cover_box) is True


def test_layout_navigation_data_builds_pathfinder_with_connected_path():
    layout = create_default_facility_layout()
    pathfinder = build_waypoint_pathfinder(layout)
    path = pathfinder.find_path(start_position=(-8.0, 0.0, 0.0), goal_position=(8.0, 0.0, 6.0))
    assert len(path) >= 3
    assert path[0] == layout.waypoints["wp_lobby"]
    assert path[-1] == layout.waypoints["wp_lab"]


def test_cover_selection_and_tactical_action_choice():
    layout = create_default_facility_layout()
    ai_bot = Bot.create_default(bot_id="tactical-bot", position=(-7.5, 0.0, -1.0))
    ai_bot.health = 25
    player_position = (-2.0, 0.0, -1.0)
    plan = find_cover_plan(
        bot_position=ai_bot.position,
        player_position=player_position,
        cover_objects=layout.cover_objects,
    )
    assert plan is not None
    action = choose_tactical_action(
        bot=ai_bot,
        player_position=player_position,
        cover_objects=layout.cover_objects,
        ally_count=0,
    )
    assert action == TacticalAction.TAKE_COVER


def test_flank_route_and_wave_scaling_behavior():
    flank_route = build_flank_route(
        bot_position=(-10.0, 0.0, 0.0),
        player_position=(0.0, 0.0, 0.0),
        flank_radius=4.0,
    )
    assert len(flank_route) == 2
    assert flank_route[-1] == (0.0, 0.0, 0.0)
    assert flank_route[0][2] != 0.0

    layout = create_default_facility_layout()
    director = WaveDirector()
    wave1 = director.spawn_wave(
        wave_number=1,
        spawn_positions=layout.bot_spawn_positions(),
        rng=Random(42),
    )
    wave4 = director.spawn_wave(
        wave_number=4,
        spawn_positions=layout.bot_spawn_positions(),
        rng=Random(42),
    )
    assert len(wave4) > len(wave1)
    assert wave4[0].max_health > wave1[0].max_health
    assert wave4[0].weapon.fire_rate > wave1[0].weapon.fire_rate
