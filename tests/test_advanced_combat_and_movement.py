from src.core.camera import FirstPersonCamera
from src.core.collision import AABB, CollisionWorld
from src.core.input_handler import InputHandler, InputSnapshot
from src.core.movement import PlayerMovementController
from src.core.raycasting import RaycastingSystem, RaycastTarget
from src.player.player import Player
from src.projectiles.physics import ProjectilePhysicsSystem
from src.weapons.assault_rifle import AssaultRifle
from src.weapons.rpg import RPG
from src.weapons.shotgun import Shotgun
from src.weapons.visuals import get_weapon_visual


def test_camera_mouse_look_uses_input_handler_and_clamps_pitch():
    handler = InputHandler(mouse_sensitivity=1.0)
    camera = FirstPersonCamera()
    frame = handler.build_frame(
        InputSnapshot(pressed_keys=set(), mouse_delta_x=12.0, mouse_delta_y=-200.0)
    )
    yaw, pitch = camera.apply_look_delta(frame.look_yaw, frame.look_pitch)
    assert yaw == 12.0
    assert pitch == 89.0


def test_player_movement_resolves_wall_collision_with_slide():
    world = CollisionWorld(
        world_bounds=AABB(min_corner=(-5.0, 0.0, -5.0), max_corner=(5.0, 3.0, 5.0)),
        static_walls=[AABB(min_corner=(0.8, 0.0, 1.0), max_corner=(1.8, 3.0, 2.5))],
    )
    movement = PlayerMovementController(walk_speed=4.0)
    next_pos = movement.move(
        player_position=(0.0, 1.8, 0.3),
        player_yaw_degrees=0.0,
        move_x=1.0,
        move_z=1.0,
        delta_time=0.5,
        collision_world=world,
    )
    assert next_pos[0] > 0.0
    assert next_pos[2] == 0.3


def test_player_weapon_switch_reload_and_game_over_respawn():
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    player.add_weapon(Shotgun())
    player.add_weapon(AssaultRifle())
    assert player.cycle_weapon(1) == "Shotgun"
    assert player.cycle_weapon(1) == "AssaultRifle"
    assert player.cycle_weapon(-1) == "Shotgun"

    player.equipped_weapon.ammo_in_magazine = 2
    player.equipped_weapon.reserve_ammo = 10
    loaded = player.reload_weapon()
    assert loaded == 6
    assert player.equipped_weapon.ammo_in_magazine == 8
    assert player.equipped_weapon.reserve_ammo == 4

    player.apply_damage(999)
    assert player.is_game_over is True
    assert player.shoot(10.0) is False
    player.respawn((1.0, 1.8, 2.0))
    assert player.is_game_over is False
    assert player.health == 100
    assert player.position == (1.0, 1.8, 2.0)


def test_smooth_weapon_switch_transition_flow():
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    player.add_weapon(Shotgun())
    started = player.start_smooth_weapon_switch("Shotgun", now=1.0)
    assert started is True
    assert player.is_weapon_switching is True
    assert player.equipped_weapon_name == "Pistol"
    assert player.update_weapon_switch(1.1) is None
    equipped = player.update_weapon_switch(1.21)
    assert equipped == "Shotgun"
    assert player.equipped_weapon_name == "Shotgun"
    assert player.is_weapon_switching is False


def test_player_hitscan_shooting_uses_raycasting():
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    raycasting = RaycastingSystem()
    hit = player.shoot_hitscan(
        now=1.0,
        origin=(0.0, 0.0, 0.0),
        direction=(1.0, 0.0, 0.0),
        max_distance=30.0,
        raycasting_system=raycasting,
        targets=[
            RaycastTarget(target_id="bot-a", center=(5.0, 0.0, 0.0), radius=0.6),
            RaycastTarget(target_id="bot-b", center=(12.0, 0.0, 0.0), radius=1.0),
        ],
    )
    assert hit is not None
    assert hit.target_id == "bot-a"
    assert player.equipped_weapon.ammo_in_magazine == 11


def test_shotgun_assault_rifle_and_rpg_behaviors():
    shotgun = Shotgun()
    payload = shotgun.create_projectile_payload(
        origin=(0.0, 0.0, 0.0),
        direction=(0.0, 0.0, 1.0),
    )
    assert len(payload) == shotgun.pellet_count
    assert payload[0]["kind"] == "pellet"

    rifle = AssaultRifle()
    assert rifle.fire(1.0) is True
    assert rifle.fire(1.05) is False
    assert rifle.fire(1.12) is True

    rpg = RPG()
    assert rpg.crash_triggered is False
    assert rpg.fire(2.0) is True
    assert rpg.crash_triggered is True


def test_weapon_visual_definitions_exist_for_progression_weapons():
    for weapon_name in ("Pistol", "Shotgun", "AssaultRifle", "RPG"):
        visual = get_weapon_visual(weapon_name)
        assert visual.weapon_name == weapon_name
        assert len(visual.primitives) > 0


def test_projectile_system_and_collision_physics():
    world = CollisionWorld(
        world_bounds=AABB(min_corner=(-2.0, -2.0, -2.0), max_corner=(2.0, 2.0, 2.0)),
        static_walls=[AABB(min_corner=(0.9, -1.0, -1.0), max_corner=(1.1, 1.0, 1.0))],
    )
    player = Player.with_starter_loadout(start_health=100, start_money=0)
    projectiles = player.shoot_projectiles(
        now=1.0,
        origin=(0.0, 0.0, 0.0),
        direction=(1.0, 0.0, 0.0),
    )
    assert len(projectiles) == 1
    physics = ProjectilePhysicsSystem()
    collisions = physics.step(projectiles, delta_time=0.05, world=world)
    assert collisions == 1
    assert projectiles[0].is_active is False
