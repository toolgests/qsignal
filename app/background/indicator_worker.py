"""
Indicator Worker

Continuously calculates technical indicators from the latest
OHLC candles and broadcasts them to WebSocket clients.
"""

from __future__ import annotations

import asyncio

import pandas as pd
from structlog import get_logger

from app.market_engine.ohlc_aggregator import ohlc_aggregator
from app.services.indicator.service import indicator_service
from app.websocket.broadcast import broadcast_manager
from app.websocket.events import IndicatorEvent

logger = get_logger(__name__)


class IndicatorWorker:
    """
    Background worker for technical indicators.
    """

    def __init__(
        self,
        timeframe: str = "1m",
        interval: float = 1.0,
    ) -> None:

        self.timeframe = timeframe

        self.interval = interval

        self._running = False

        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        """
        Start indicator worker.
        """

        if self._running:
            return

        logger.info(
            "Starting Indicator Worker..."
        )

        self._running = True

        self._task = asyncio.create_task(
            self._run()
        )

    async def stop(self) -> None:
        """
        Stop indicator worker.
        """

        self._running = False

        if self._task:

            self._task.cancel()

            try:

                await self._task

            except asyncio.CancelledError:
                pass

        logger.info(
            "Indicator Worker stopped."
        )

    async def _run(self) -> None:
        """
        Main worker loop.
        """

        while self._running:

            try:

                symbols = {
                    key[0]
                    for key in ohlc_aggregator._history.keys()
                }

                for symbol in symbols:

                    candles = ohlc_aggregator.history(
                        symbol=symbol,
                        timeframe=self.timeframe,
                        limit=300,
                    )

                    if len(candles) < 30:
                        continue

                    dataframe = pd.DataFrame(
                        candles
                    )

                    indicators = (
                        indicator_service.latest(
                            dataframe
                        )
                    )

                    event = IndicatorEvent(
                        event="indicator",
                        symbol=symbol,
                        timeframe=self.timeframe,
                        indicators=indicators,
                    )

                    await broadcast_manager.publish(
                        event.model_dump(
                            mode="json"
                        )
                    )

                await asyncio.sleep(
                    self.interval
                )

            except asyncio.CancelledError:

                break

            except Exception as exc:

                logger.exception(
                    "Indicator Worker Error",
                    error=str(exc),
                )

                await asyncio.sleep(2)


indicator_worker = IndicatorWorker()