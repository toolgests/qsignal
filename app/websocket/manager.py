"""
WebSocket Connection Manager

Manages all active WebSocket client connections.
"""

from __future__ import annotations

import asyncio

from fastapi import WebSocket
from structlog import get_logger

logger = get_logger(__name__)


class ConnectionManager:
    """
    Manage active WebSocket connections.
    """

    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    @property
    def total_connections(self) -> int:
        """
        Return total active connections.
        """
        return len(self._connections)

    async def connect(
        self,
        websocket: WebSocket,
    ) -> None:
        """
        Accept and register a WebSocket connection.
        """

        await websocket.accept()

        async with self._lock:
            self._connections.add(websocket)

        logger.info(
            "WebSocket connected",
            total=self.total_connections,
        )

    async def disconnect(
        self,
        websocket: WebSocket,
    ) -> None:
        """
        Remove a WebSocket connection.
        """

        async with self._lock:
            self._connections.discard(websocket)

        logger.info(
            "WebSocket disconnected",
            total=self.total_connections,
        )

    async def send(
        self,
        websocket: WebSocket,
        message: dict,
    ) -> None:
        """
        Send message to a single client.
        """

        try:
            await websocket.send_json(message)

        except Exception as exc:

            logger.error(
                "Send failed",
                error=str(exc),
            )

            await self.disconnect(websocket)

    async def broadcast(
        self,
        message: dict,
    ) -> None:

#         logger.info(
#     "WS BROADCAST",
#     clients=len(self._connections),
#     message=message,
# )
        """
        Broadcast message to all connected clients.
        """

        disconnected: list[WebSocket] = []

        async with self._lock:

            for websocket in self._connections:

                try:
                    await websocket.send_json(message)

                except Exception:

                    disconnected.append(websocket)

            for websocket in disconnected:
                self._connections.discard(websocket)

        if disconnected:

            logger.warning(
                "Removed disconnected clients",
                count=len(disconnected),
            )


connection_manager = ConnectionManager()