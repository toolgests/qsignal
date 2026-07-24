"""
WebSocket Router

Exposes the public /ws endpoint that clients connect to for
real-time market data, indicators and trading signals.
"""

from __future__ import annotations

import json
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.logging import get_logger
from app.websocket.channels import is_valid_channel
from app.websocket.client_session import ClientSession
from app.websocket.manager import connection_manager

logger = get_logger(__name__)

router = APIRouter(
    tags=["WebSocket"],
)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    Main WebSocket endpoint.

    Clients may send JSON control messages:

        {"action": "subscribe", "channel": "prices"}
        {"action": "unsubscribe", "channel": "prices"}
        {"action": "subscribe_symbol", "symbol": "BTCUSDT"}
        {"action": "unsubscribe_symbol", "symbol": "BTCUSDT"}
        {"action": "ping"}
    """

    await connection_manager.connect(websocket)

    session = ClientSession(
        client_id=str(uuid.uuid4()),
        websocket=websocket,
    )

    try:

        while True:

            raw_message = await websocket.receive_text()

            try:
                message = json.loads(raw_message)

            except json.JSONDecodeError:
                await websocket.send_json(
                    {
                        "event": "error",
                        "message": "Invalid JSON payload.",
                    }
                )
                continue

            action = message.get("action")

            if action == "ping":
                await websocket.send_json({"event": "pong"})

            elif action == "subscribe":
                channel = message.get("channel", "")

                if is_valid_channel(channel):
                    session.subscribe_channel(channel)
                    await websocket.send_json(
                        {
                            "event": "subscribed",
                            "channel": channel,
                        }
                    )
                else:
                    await websocket.send_json(
                        {
                            "event": "error",
                            "message": f"Unknown channel: {channel}",
                        }
                    )

            elif action == "unsubscribe":
                session.unsubscribe_channel(message.get("channel", ""))
                await websocket.send_json(
                    {
                        "event": "unsubscribed",
                        "channel": message.get("channel", ""),
                    }
                )

            elif action == "subscribe_symbol":
                symbol = message.get("symbol", "")
                session.subscribe_symbol(symbol)
                await websocket.send_json(
                    {
                        "event": "symbol_subscribed",
                        "symbol": symbol.upper(),
                    }
                )

            elif action == "unsubscribe_symbol":
                symbol = message.get("symbol", "")
                session.unsubscribe_symbol(symbol)
                await websocket.send_json(
                    {
                        "event": "symbol_unsubscribed",
                        "symbol": symbol.upper(),
                    }
                )

            else:
                await websocket.send_json(
                    {
                        "event": "error",
                        "message": f"Unknown action: {action}",
                    }
                )

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected", client_id=session.client_id)

    finally:
        await connection_manager.disconnect(websocket)
