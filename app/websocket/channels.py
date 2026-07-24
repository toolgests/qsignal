"""
WebSocket Channels

Centralized channel definitions for the Q Signals backend.
"""

from __future__ import annotations

from enum import StrEnum


class Channel(StrEnum):
    """
    Supported WebSocket channels.
    """

    ALL = "all"

    PRICES = "prices"

    CRYPTO = "crypto"

    FOREX = "forex"

    STOCKS = "stocks"

    SIGNALS = "signals"

    CHART = "chart"

    INDICATORS = "indicators"

    MARKET = "market"

    SYSTEM = "system"


ALL_CHANNELS: tuple[str, ...] = (
    Channel.ALL,
    Channel.PRICES,
    Channel.CRYPTO,
    Channel.FOREX,
    Channel.STOCKS,
    Channel.SIGNALS,
    Channel.CHART,
    Channel.INDICATORS,
    Channel.MARKET,
    Channel.SYSTEM,
)


def is_valid_channel(channel: str) -> bool:
    """
    Validate websocket channel.
    """

    return channel in ALL_CHANNELS