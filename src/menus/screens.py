"""Menu and ending screen payload models."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.glitch.bsod import FakeCrashScreen


@dataclass(frozen=True)
class ScreenAction:
    """A selectable action rendered on a menu-like screen."""

    action_id: str
    label: str
    hint: str
    is_primary: bool = False


@dataclass(frozen=True)
class MenuScreen:
    """Render-facing menu payload for UI layers."""

    screen_id: str
    title: str
    subtitle: str
    body_lines: list[str] = field(default_factory=list)
    actions: list[ScreenAction] = field(default_factory=list)


def build_main_menu_screen() -> MenuScreen:
    """Build the default entry menu with a clear start action."""
    return MenuScreen(
        screen_id="main_menu",
        title="FPS Bot Arena",
        subtitle="Eliminate tactical bot waves and survive until the RPG endgame.",
        body_lines=[
            "Controls: WASD + Mouse to move and look.",
            "Press B to open shop wheel and buy upgrades.",
        ],
        actions=[
            ScreenAction(
                action_id="start_game",
                label="Start Arena Run",
                hint="Begin a new run from wave 1.",
                is_primary=True,
            ),
            ScreenAction(
                action_id="controls",
                label="Controls",
                hint="View detailed controls.",
            ),
            ScreenAction(
                action_id="quit",
                label="Quit",
                hint="Exit the session.",
            ),
        ],
    )


def build_controls_screen() -> MenuScreen:
    """Build the controls instruction screen."""
    return MenuScreen(
        screen_id="controls",
        title="Controls",
        subtitle="Master the arena mechanics.",
        body_lines=[
            "Movement: W, A, S, D",
            "Look: Mouse",
            "Fire: Left Mouse Button",
            "Reload: R",
            "Shop / Inventory: B (Hold)",
            "Weapon Switch: 1, 2, 3, 4",
            "Jump: Space",
        ],
        actions=[
            ScreenAction(
                action_id="back_to_menu",
                label="Back",
                hint="Return to main menu.",
                is_primary=True,
            ),
        ],
    )


def build_pause_menu_screen() -> MenuScreen:
    """Build the pause menu payload."""
    return MenuScreen(
        screen_id="pause_menu",
        title="Paused",
        subtitle="Game simulation suspended.",
        actions=[
            ScreenAction(
                action_id="resume_game",
                label="Resume",
                hint="Return to the fight.",
                is_primary=True,
            ),
            ScreenAction(
                action_id="quit_to_menu",
                label="Quit to Menu",
                hint="Abandon current run.",
            ),
        ],
    )


def build_game_over_screen(score: int, waves_cleared: int) -> MenuScreen:
    """Build the game over screen with stats."""
    return MenuScreen(
        screen_id="game_over",
        title="Mission Failed",
        subtitle=f"You survived {waves_cleared} waves with a score of {score}.",
        actions=[
            ScreenAction(
                action_id="restart_game",
                label="Try Again",
                hint="Start a new run.",
                is_primary=True,
            ),
            ScreenAction(
                action_id="quit_to_menu",
                label="Main Menu",
                hint="Return to title screen.",
            ),
        ],
    )


def build_crash_ending_screen(crash_screen: FakeCrashScreen) -> MenuScreen:
    """Build the RPG ending screen payload using fake BSOD content."""
    return MenuScreen(
        screen_id="crash_ending",
        title="System Failure Detected",
        subtitle="RPG payload destabilized the simulation.",
        body_lines=crash_screen.to_lines(),
        actions=[
            ScreenAction(
                action_id="restart_to_menu",
                label="Restart Simulation",
                hint="Press ENTER, ESC, or R to recover.",
                is_primary=True,
            ),
        ],
    )
