# """
# Background Scheduler

# Starts and stops all background workers together, keeping the
# application lifespan (app.main) simple.
# """

# from __future__ import annotations

# from app.background.indicator_worker import indicator_worker
# from app.background.market_stream import market_stream
# from app.background.signal_worker import signal_worker
# from app.background.websocket_worker import websocket_worker
# from app.logging import get_logger

# logger = get_logger(__name__)


# class BackgroundScheduler:
#     """
#     Coordinates all background workers.
#     """

#     async def start_all(self) -> None:
#         """
#         Start every background worker.
#         """

#         logger.info("Starting background workers...")

#         await market_stream.start()
#         await websocket_worker.start()
#         await indicator_worker.start()
#         await signal_worker.start()

#         logger.info("All background workers started.")

#     async def stop_all(self) -> None:
#         """
#         Stop every background worker.
#         """

#         logger.info("Stopping background workers...")

#         await signal_worker.stop()
#         await indicator_worker.stop()
#         await websocket_worker.stop()
#         await market_stream.stop()

#         logger.info("All background workers stopped.")


# scheduler = BackgroundScheduler()





"""
Background Scheduler

Starts and stops all background workers.
"""

from __future__ import annotations

import asyncio

from app.background.indicator_worker import indicator_worker
from app.background.market_stream import market_stream
from app.background.signal_worker import signal_worker
from app.background.websocket_worker import websocket_worker
from app.logging import get_logger

logger = get_logger(__name__)


class BackgroundScheduler:

    def __init__(self):
        self.tasks: list[asyncio.Task] = []

    async def start_all(self) -> None:

        logger.info("Starting background workers...")

        self.tasks.append(
            asyncio.create_task(
                market_stream.start()
            )
        )

        self.tasks.append(
            asyncio.create_task(
                websocket_worker.start()
            )
        )

        self.tasks.append(
            asyncio.create_task(
                indicator_worker.start()
            )
        )

        self.tasks.append(
            asyncio.create_task(
                signal_worker.start()
            )
        )

        logger.info("All background workers started.")

    async def stop_all(self) -> None:

        logger.info("Stopping background workers...")

        await market_stream.stop()
        await websocket_worker.stop()
        await indicator_worker.stop()
        await signal_worker.stop()

        for task in self.tasks:
            task.cancel()

        await asyncio.gather(
            *self.tasks,
            return_exceptions=True,
        )

        self.tasks.clear()

        logger.info("All background workers stopped.")


scheduler = BackgroundScheduler()