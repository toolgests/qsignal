"""
WebSocket Broadcast Manager

High-performance asynchronous broadcast manager for WebSocket clients.
"""

from __future__ import annotations

import asyncio

from structlog import get_logger

from app.websocket.manager import connection_manager

logger = get_logger(__name__)


class BroadcastManager:
    """
    Queue-based broadcast manager.
    """

    def __init__(self) -> None:
        self._queue: asyncio.Queue[dict] = asyncio.Queue()
        self._worker: asyncio.Task | None = None
        self._running = False

    async def start(self) -> None:
        """
        Start broadcast worker.
        """

        if self._running:
            return

        self._running = True

        self._worker = asyncio.create_task(
            self._broadcast_worker()
        )

        logger.info("Broadcast manager started")

    async def stop(self) -> None:
        """
        Stop broadcast worker.
        """

        self._running = False

        if self._worker:

            self._worker.cancel()

            try:
                await self._worker

            except asyncio.CancelledError:
                pass

        logger.info("Broadcast manager stopped")

    async def publish(
        self,
        message: dict,
    ) -> None:
        """
        Publish a message to the broadcast queue.
        """

        await self._queue.put(message)

    async def _broadcast_worker(self) -> None:
        """
        Background broadcast worker.
        """

        while self._running:

            try:

                message = await self._queue.get()

                await connection_manager.broadcast(message)

                self._queue.task_done()

            except asyncio.CancelledError:

                break

            except Exception as exc:

                logger.exception(
                    "Broadcast worker error",
                    error=str(exc),
                )


broadcast_manager = BroadcastManager()