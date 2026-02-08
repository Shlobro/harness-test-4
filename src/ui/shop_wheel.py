"""Shop wheel layout and interaction logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import cos, radians, sin
from typing import Callable

from config.config import ECONOMY_CONFIG
from src.core.game_clock import GameClock
from src.core.game_state import GameState, GameStateManager
from src.player.player import Player
from src.weapons.assault_rifle import AssaultRifle
from src.weapons.rpg import RPG
from src.weapons.shotgun import Shotgun
from src.weapons.weapon import Weapon


WeaponFactory = Callable[[], Weapon]


@dataclass(frozen=True)
class ShopCatalogItem:
    """Store-facing weapon metadata and constructor."""

    weapon_name: str
    price: int
    factory: WeaponFactory


@dataclass(frozen=True)
class ShopWheelEntry:
    """Derived UI entry consumed by rendering/HUD layer."""

    weapon_name: str
    price: int
    slot_index: int
    angle_degrees: float
    anchor_x: float
    anchor_y: float
    is_owned: bool
    is_equipped: bool
    can_afford: bool
    is_affordable_to_buy: bool


@dataclass(frozen=True)
class ShopActionResult:
    """Outcome of a shop interaction request."""

    success: bool
    action: str
    weapon_name: str | None = None
    reason: str | None = None
    amount_spent: int = 0


@dataclass
class ShopWheelLayout:
    """Generate radial placement for shop entries."""

    radius: float = 0.82
    center_x: float = 0.0
    center_y: float = 0.0
    start_angle_degrees: float = -90.0

    def build_entries(
        self,
        *,
        player: Player,
        catalog_items: list[ShopCatalogItem],
    ) -> list[ShopWheelEntry]:
        if not catalog_items:
            return []
        slot_count = len(catalog_items)
        angle_step = 360.0 / slot_count
        entries: list[ShopWheelEntry] = []
        for index, item in enumerate(catalog_items):
            angle = self.start_angle_degrees + (index * angle_step)
            theta = radians(angle)
            anchor_x = self.center_x + (self.radius * cos(theta))
            anchor_y = self.center_y + (self.radius * sin(theta))
            is_owned = item.weapon_name in player.inventory
            is_equipped = player.equipped_weapon_name == item.weapon_name
            can_afford = player.money >= item.price
            entries.append(
                ShopWheelEntry(
                    weapon_name=item.weapon_name,
                    price=item.price,
                    slot_index=index,
                    angle_degrees=angle,
                    anchor_x=anchor_x,
                    anchor_y=anchor_y,
                    is_owned=is_owned,
                    is_equipped=is_equipped,
                    can_afford=can_afford,
                    is_affordable_to_buy=(not is_owned) and can_afford,
                )
            )
        return entries


def default_shop_catalog() -> list[ShopCatalogItem]:
    """Return progression-aligned store inventory."""
    return [
        ShopCatalogItem("Shotgun", ECONOMY_CONFIG.shotgun_price, Shotgun),
        ShopCatalogItem("AssaultRifle", ECONOMY_CONFIG.assault_rifle_price, AssaultRifle),
        ShopCatalogItem("RPG", ECONOMY_CONFIG.rpg_price, RPG),
    ]


@dataclass
class ShopWheelController:
    """Manage shop open state and purchase/equip interactions."""

    catalog_items: list[ShopCatalogItem] = field(default_factory=default_shop_catalog)
    layout: ShopWheelLayout = field(default_factory=ShopWheelLayout)
    is_open: bool = False

    def __post_init__(self) -> None:
        self._catalog_by_name = {item.weapon_name: item for item in self.catalog_items}

    def handle_shop_toggle(
        self,
        *,
        game_state_manager: GameStateManager,
        game_clock: GameClock,
    ) -> bool:
        """Toggle wheel visibility and synchronize pause state."""
        self.is_open = not self.is_open
        self._sync_pause_state(game_state_manager=game_state_manager, game_clock=game_clock)
        return self.is_open

    def handle_input_frame(
        self,
        *,
        toggle_shop_requested: bool,
        game_state_manager: GameStateManager,
        game_clock: GameClock,
    ) -> bool:
        """Consume normalized input and return whether wheel is open."""
        if toggle_shop_requested:
            return self.handle_shop_toggle(
                game_state_manager=game_state_manager,
                game_clock=game_clock,
            )
        return self.is_open

    def close(
        self,
        *,
        game_state_manager: GameStateManager,
        game_clock: GameClock,
    ) -> None:
        if not self.is_open:
            return
        self.is_open = False
        self._sync_pause_state(game_state_manager=game_state_manager, game_clock=game_clock)

    def get_entries(self, player: Player) -> list[ShopWheelEntry]:
        """Return render-ready entries with affordability/ownership status."""
        return self.layout.build_entries(player=player, catalog_items=self.catalog_items)

    def purchase_or_equip(
        self,
        *,
        player: Player,
        weapon_name: str,
    ) -> ShopActionResult:
        """Buy unavailable weapon or equip owned one."""
        catalog_item = self._catalog_by_name.get(weapon_name)
        if catalog_item is None:
            return ShopActionResult(
                success=False,
                action="rejected",
                weapon_name=weapon_name,
                reason="unknown_weapon",
            )

        if weapon_name in player.inventory:
            player.equip_weapon(weapon_name)
            return ShopActionResult(
                success=True,
                action="equipped",
                weapon_name=weapon_name,
            )

        if not player.spend_money(catalog_item.price):
            return ShopActionResult(
                success=False,
                action="rejected",
                weapon_name=weapon_name,
                reason="insufficient_funds",
            )

        player.add_weapon(catalog_item.factory(), auto_equip=True)
        return ShopActionResult(
            success=True,
            action="purchased",
            weapon_name=weapon_name,
            amount_spent=catalog_item.price,
        )

    def _sync_pause_state(
        self,
        *,
        game_state_manager: GameStateManager,
        game_clock: GameClock,
    ) -> None:
        game_clock.set_paused(self.is_open)
        if self.is_open and game_state_manager.current_state == GameState.PLAYING:
            game_state_manager.transition_to(GameState.PAUSED)
        elif (not self.is_open) and game_state_manager.current_state == GameState.PAUSED:
            game_state_manager.transition_to(GameState.PLAYING)
