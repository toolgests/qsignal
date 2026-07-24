"""
WebSocket Client Session

Represents a connected WebSocket client session.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from fastapi import WebSocket


@dataclass(slots=True)
class ClientSession:
    """
    Represents a single connected client.
    """

    client_id: str

    websocket: WebSocket

    connected_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    last_heartbeat: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    subscribed_symbols: set[str] = field(
        default_factory=set
    )

    subscribed_channels: set[str] = field(
        default_factory=set
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )

    def subscribe_symbol(
        self,
        symbol: str,
    ) -> None:
        """
        Subscribe to a trading symbol.
        """

        self.subscribed_symbols.add(symbol.upper())

    def unsubscribe_symbol(
        self,
        symbol: str,
    ) -> None:
        """
        Remove subscribed symbol.
        """

        self.subscribed_symbols.discard(symbol.upper())

    def subscribe_channel(
        self,
        channel: str,
    ) -> None:
        """
        Subscribe to a websocket channel.
        """

        self.subscribed_channels.add(channel)

    def unsubscribe_channel(
        self,
        channel: str,
    ) -> None:
        """
        Remove subscribed channel.
        """

        self.subscribed_channels.discard(channel)

    def update_heartbeat(self) -> None:
        """
        Update heartbeat timestamp.
        """

        self.last_heartbeat = datetime.now(UTC)

    @property
    def uptime_seconds(self) -> float:
        """
        Return connection uptime.
        """

        return (
            datetime.now(UTC) - self.connected_at
        ).total_seconds()

    def to_dict(self) -> dict:
        """
        Serialize client session.
        """

        return {
            "client_id": self.client_id,
            "connected_at": self.connected_at.isoformat(),
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "symbols": sorted(self.subscribed_symbols),
            "channels": sorted(self.subscribed_channels),
            "metadata": self.metadata,
            "uptime": self.uptime_seconds,
        }