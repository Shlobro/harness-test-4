"""Backend-agnostic audio event engine."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ActiveSoundEvent:
    """Tracks a currently active audio event."""

    event_id: str
    sound_name: str
    channel: str
    loop: bool


class AudioEngine:
    """Simple sound event registry used by gameplay systems and tests."""

    def __init__(self) -> None:
        self._next_event_id = 1
        self._active_events: dict[str, ActiveSoundEvent] = {}

    @property
    def active_events(self) -> list[ActiveSoundEvent]:
        return list(self._active_events.values())

    def play(self, *, sound_name: str, channel: str = "sfx", loop: bool = False) -> str:
        event_id = f"evt_{self._next_event_id}"
        self._next_event_id += 1
        self._active_events[event_id] = ActiveSoundEvent(
            event_id=event_id,
            sound_name=sound_name,
            channel=channel,
            loop=loop,
        )
        return event_id

    def stop(self, event_id: str) -> bool:
        return self._active_events.pop(event_id, None) is not None

    def stop_channel(self, channel: str) -> int:
        to_remove = [event_id for event_id, evt in self._active_events.items() if evt.channel == channel]
        for event_id in to_remove:
            self._active_events.pop(event_id, None)
        return len(to_remove)
