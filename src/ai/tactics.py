"""Tactical decision-making, cover usage, and flanking helpers."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import sqrt

from src.ai.bot import Bot
from src.environment.facility import CoverObject


Vector3 = tuple[float, float, float]


class TacticalAction(str, Enum):
    """Primary tactical actions a bot can select."""

    ATTACK = "attack"
    TAKE_COVER = "take_cover"
    FLANK = "flank"


@dataclass(frozen=True)
class CoverPlan:
    """Selected cover target and movement anchor for a bot."""

    cover_id: str
    anchor_position: Vector3
    distance_from_bot: float


def _distance_2d(a: Vector3, b: Vector3) -> float:
    dx = a[0] - b[0]
    dz = a[2] - b[2]
    return sqrt((dx * dx) + (dz * dz))


def _segment_point_distance_2d(a: Vector3, b: Vector3, p: Vector3) -> float:
    ab_x = b[0] - a[0]
    ab_z = b[2] - a[2]
    ap_x = p[0] - a[0]
    ap_z = p[2] - a[2]
    ab_len_sq = (ab_x * ab_x) + (ab_z * ab_z)
    if ab_len_sq <= 1e-9:
        return _distance_2d(a, p)
    t = ((ap_x * ab_x) + (ap_z * ab_z)) / ab_len_sq
    t = max(0.0, min(1.0, t))
    closest = (a[0] + (ab_x * t), 0.0, a[2] + (ab_z * t))
    return _distance_2d(closest, p)


def _cover_blocks_line_of_fire(
    *,
    cover: CoverObject,
    from_position: Vector3,
    to_position: Vector3,
) -> bool:
    center = cover.center
    half_extent_x = (cover.max_corner[0] - cover.min_corner[0]) * 0.5
    half_extent_z = (cover.max_corner[2] - cover.min_corner[2]) * 0.5
    radius = sqrt((half_extent_x * half_extent_x) + (half_extent_z * half_extent_z))
    return _segment_point_distance_2d(from_position, to_position, center) <= (radius + 0.35)


def _cover_anchor(cover: CoverObject, player_position: Vector3, stand_off: float = 0.9) -> Vector3:
    center = cover.center
    dir_x = center[0] - player_position[0]
    dir_z = center[2] - player_position[2]
    length = sqrt((dir_x * dir_x) + (dir_z * dir_z))
    if length <= 1e-9:
        return center
    nx = dir_x / length
    nz = dir_z / length
    return (center[0] + (nx * stand_off), center[1], center[2] + (nz * stand_off))


def find_cover_plan(
    *,
    bot_position: Vector3,
    player_position: Vector3,
    cover_objects: list[CoverObject],
    max_cover_distance: float = 12.0,
) -> CoverPlan | None:
    """Pick the nearest useful cover that can break line-of-fire to player."""
    chosen: CoverPlan | None = None
    for cover in cover_objects:
        anchor = _cover_anchor(cover, player_position)
        distance = _distance_2d(bot_position, anchor)
        if distance > max_cover_distance:
            continue
        if not _cover_blocks_line_of_fire(cover=cover, from_position=anchor, to_position=player_position):
            continue
        if chosen is None or distance < chosen.distance_from_bot:
            chosen = CoverPlan(
                cover_id=cover.cover_id,
                anchor_position=anchor,
                distance_from_bot=distance,
            )
    return chosen


def choose_tactical_action(
    *,
    bot: Bot,
    player_position: Vector3,
    cover_objects: list[CoverObject],
    ally_count: int,
    low_health_threshold: int = 35,
    attack_range: float = 14.0,
) -> TacticalAction:
    """Choose attack/cover/flank based on bot state, health, and surroundings."""
    if not bot.is_alive:
        raise ValueError(f"Cannot choose tactical action for dead bot {bot.bot_id}. Callers must filter dead bots.")

    distance_to_player = _distance_2d(bot.position, player_position)
    cover = find_cover_plan(
        bot_position=bot.position,
        player_position=player_position,
        cover_objects=cover_objects,
    )
    if bot.health <= low_health_threshold and cover is not None:
        return TacticalAction.TAKE_COVER
    if ally_count >= 1 and distance_to_player <= (attack_range * 1.5):
        return TacticalAction.FLANK
    if distance_to_player <= attack_range:
        return TacticalAction.ATTACK
    if cover is not None:
        return TacticalAction.TAKE_COVER
    return TacticalAction.ATTACK


def build_flank_route(
    *,
    bot_position: Vector3,
    player_position: Vector3,
    flank_radius: float = 5.0,
) -> list[Vector3]:
    """Create a two-point flank path that approaches the player from a side angle."""
    dir_x = player_position[0] - bot_position[0]
    dir_z = player_position[2] - bot_position[2]
    length = sqrt((dir_x * dir_x) + (dir_z * dir_z))
    if length <= 1e-9:
        return [bot_position, player_position]

    nx = dir_x / length
    nz = dir_z / length
    left = (-nz, nx)
    right = (nz, -nx)
    left_candidate = (
        player_position[0] + (left[0] * flank_radius),
        player_position[1],
        player_position[2] + (left[1] * flank_radius),
    )
    right_candidate = (
        player_position[0] + (right[0] * flank_radius),
        player_position[1],
        player_position[2] + (right[1] * flank_radius),
    )
    if _distance_2d(bot_position, left_candidate) <= _distance_2d(bot_position, right_candidate):
        return [left_candidate, player_position]
    return [right_candidate, player_position]
