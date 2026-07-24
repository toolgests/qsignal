"""
Streaming Service

Exposes the current state of live market streaming for
diagnostics and health/status endpoints.
"""

from __future__ import annotations

from app.market_engine.ohlc_aggregator import ohlc_aggregator
from app.market_engine.tick_processor import tick_processor
from app.websocket.manager import connection_manager


class StreamingService:
    """
    Service responsible for streaming diagnostics.
    """

    async def get_status(self) -> dict:
        """
        Return current streaming/engine statistics.
        """

        return {
            "connected_clients": connection_manager.total_connections,
            "tracked_symbols": tick_processor.total_symbols,
            "tracked_series": ohlc_aggregator.tracked_symbols,
            "stored_candles": ohlc_aggregator.total_candles,
        }


streaming_service = StreamingService()
