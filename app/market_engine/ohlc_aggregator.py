"""
OHLC Aggregator

Stores and aggregates OHLC candles for multiple symbols
and multiple timeframes.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any


class OHLCAggregator:
    """
    Aggregates completed candles.
    """

    def __init__(
        self,
        max_history: int = 1000,
    ) -> None:
        self.max_history = max_history

        self._history: dict[
            tuple[str, str],
            deque[dict[str, Any]]
        ] = defaultdict(
            lambda: deque(maxlen=self.max_history)
        )

    def add_candle(
        self,
        candle: dict[str, Any],
    ) -> None:
        """
        Store completed candle.
        """

        key = (
            candle["symbol"],
            candle["timeframe"],
        )

        self._history[key].append(candle)

    def latest(
        self,
        symbol: str,
        timeframe: str,
    ) -> dict[str, Any] | None:
        """
        Return latest candle.
        """

        candles = self._history.get(
            (
                symbol.upper(),
                timeframe,
            )
        )

        if not candles:
            return None

        return candles[-1]

    def history(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        """
        Return candle history.
        """

        candles = self._history.get(
            (
                symbol.upper(),
                timeframe,
            )
        )

        if candles is None:
            return []

        return list(candles)[-limit:]

    def remove_symbol(
        self,
        symbol: str,
    ) -> None:
        """
        Remove all history for a symbol.
        """

        symbol = symbol.upper()

        keys = [
            key
            for key in self._history
            if key[0] == symbol
        ]

        for key in keys:
            del self._history[key]

    def clear(self) -> None:
        """
        Clear all stored history.
        """

        self._history.clear()

    @property
    def tracked_symbols(self) -> int:
        """
        Total tracked symbol/timeframe pairs.
        """

        return len(self._history)

    @property
    def total_candles(self) -> int:
        """
        Total stored candles.
        """

        return sum(
            len(history)
            for history in self._history.values()
        )


ohlc_aggregator = OHLCAggregator()