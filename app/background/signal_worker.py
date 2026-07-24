"""
Signal Worker

Continuously generates trading signals from the latest OHLC
candles and broadcasts them to WebSocket clients.
"""

from __future__ import annotations

import asyncio

from structlog import get_logger

from app.core.exceptions import InsufficientDataError, QSignalsException
from app.market_engine.ohlc_aggregator import ohlc_aggregator
from app.services.signal.service import signal_service
from app.websocket.broadcast import broadcast_manager
from app.websocket.events import SignalEvent

logger = get_logger(__name__)


class SignalWorker:
    """
    Background worker for trading signal generation.
    """

    def __init__(
        self,
        timeframe: str = "1m",
        market: str = "crypto",
        interval: float = 5.0,
    ) -> None:

        self.timeframe = timeframe

        self.market = market

        self.interval = interval

        self._running = False

        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        """
        Start signal worker.
        """

        if self._running:
            return

        logger.info("Starting Signal Worker...")

        self._running = True

        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        """
        Stop signal worker.
        """

        self._running = False

        if self._task:

            self._task.cancel()

            try:
                await self._task

            except asyncio.CancelledError:
                pass

        logger.info("Signal Worker stopped.")

    async def _run(self) -> None:
        """
        Main worker loop.
        """

        while self._running:

            try:

                symbols = {
                    key[0] for key in ohlc_aggregator._history.keys()
                }

                for symbol in symbols:

                    try:

                        signal = signal_service.generate_signal(
                            symbol=symbol,
                            market=self.market,
                            timeframe=self.timeframe,
                        )

                    except InsufficientDataError:
                        continue

                    event = SignalEvent(
                        event="signal",
                        symbol=signal.symbol,
                        market=signal.market,
                        timeframe=signal.timeframe,
                        signal=signal.signal,
                        confidence=signal.confidence,
                        strength=signal.strength,
                    )

                    await broadcast_manager.publish(
                        event.model_dump(mode="json")
                    )

                await asyncio.sleep(self.interval)

            except asyncio.CancelledError:

                break

            except QSignalsException as exc:

                logger.warning("Signal Worker Warning", error=exc.message)

                await asyncio.sleep(2)

            except Exception as exc:

                logger.exception("Signal Worker Error", error=str(exc))

                await asyncio.sleep(2)


signal_worker = SignalWorker()
