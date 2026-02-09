"""Fake crash screen content for the RPG endgame glitch sequence."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FakeCrashScreen:
    """Structured payload used by the renderer to display a fake BSOD."""

    background_hex: str
    text_hex: str
    support_url: str
    headline: str
    summary: str
    stop_code: str
    fault_module: str
    diagnostic_text: str
    completion_text: str
    restart_hint: str
    simulation_notice: str

    def to_lines(self) -> list[str]:
        """Return text lines in display order for a crash screen renderer."""
        return [
            self.headline,
            "",
            self.summary,
            f"Stop code: {self.stop_code}",
            f"What failed: {self.fault_module}",
            "",
            self.diagnostic_text,
            self.completion_text,
            "",
            f"For more information visit: {self.support_url}",
            self.restart_hint,
            self.simulation_notice,
        ]


def build_fake_bsod_screen() -> FakeCrashScreen:
    """Build a realistic but recoverable fake crash screen message."""
    return FakeCrashScreen(
        background_hex="#0078D7",
        text_hex="#FFFFFF",
        support_url="https://arena.help/crash-stopcode",
        headline="Your device ran into a problem and needs to restart.",
        summary="We're just collecting some error info, and then we'll restart for you.",
        stop_code="CRITICAL_PROCESS_DIED",
        fault_module="arena_rpg_payload.sys",
        diagnostic_text=(
            "If you call a support person, give them this info: "
            "Exception 0x000000EF at kernel frame 0xFFFFA304."
        ),
        completion_text="82% complete",
        restart_hint="Press ENTER, ESC, or R to safely return to the main menu.",
        simulation_notice="Simulation notice: this is an in-game effect and is fully recoverable.",
    )
