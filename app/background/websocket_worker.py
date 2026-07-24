"""
WebSocket Worker

Continuously broadcasts live market data to all connected
WebSocket clients.
"""

from __future__ import annotations

import asyncio

from structlog import get_logger

from app.market_engine.tick_processor import tick_processor
from app.websocket.broadcast import broadcast_manager
from app.websocket.events import PriceEvent

logger = get_logger(__name__)


class WebSocketWorker:
    """
    Background worker responsible for broadcasting
    live market data.
    """

    def __init__(
        self,
        interval: float = 0.10,
    ) -> None:
        self.interval = interval

        self._running = False

        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        """
        Start websocket broadcaster.
        """

        if self._running:
            return

        logger.info(
            "Starting WebSocket Worker..."
        )

        self._running = True

        self._task = asyncio.create_task(
            self._run()
        )

    async def stop(self) -> None:
        """
        Stop broadcaster.
        """

        self._running = False

        if self._task:

            self._task.cancel()

            try:

                await self._task

            except asyncio.CancelledError:
                pass

        logger.info(
            "WebSocket Worker stopped."
        )

    async def _run(self) -> None:
        """
        Broadcast latest ticks.
        """

        while self._running:

            try:

                for tick in tick_processor._latest_ticks.values():

                    event = PriceEvent(
                        event="price",
                        symbol=tick["symbol"],
                        market=tick["market"],
                        price=tick["price"],
                        change=0.0,
                        change_percent=0.0,
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
                    "WebSocket Worker Error",
                    error=str(exc),
                )

                await asyncio.sleep(1)


websocket_worker = WebSocketWorker()