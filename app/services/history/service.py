"""
History Service

Provides access to historical OHLC candle data, combining
in-memory aggregator history with provider REST fallbacks.
"""

from __future__ import annotations

from app.core.constants import DEFAULT_HISTORY_LIMIT, MAX_HISTORY_LIMIT
from app.market_engine.ohlc_aggregator import ohlc_aggregator


class HistoryService:
    """
    Service responsible for historical candle retrieval.
    """

    def get_history(
        self,
        symbol: str,
        timeframe: str,
        limit: int = DEFAULT_HISTORY_LIMIT,
    ) -> list[dict]:
        """
        Return stored candle history for a symbol/timeframe.
        """

        limit = max(1, min(limit, MAX_HISTORY_LIMIT))

        return ohlc_aggregator.history(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
        )

    def get_latest(
        self,
        symbol: str,
        timeframe: str,
    ) -> dict | None:
        """
        Return the most recent completed candle.
        """

        return ohlc_aggregator.latest(
            symbol=symbol,
            timeframe=timeframe,
        )


history_service = HistoryService()
