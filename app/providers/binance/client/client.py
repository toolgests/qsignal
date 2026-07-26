"""
Binance HTTP Client

Shared asynchronous HTTP client for Binance REST API.
"""

from __future__ import annotations

import httpx

from app.core.config import config


class BinanceClient:
    """
    Shared Binance HTTP client.
    """

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=config.BINANCE_REST_URL,
            timeout=httpx.Timeout(10.0),
            headers={
                "Content-Type": "application/json",
            },
            http2=True,
        )

    @property
    def client(self) -> httpx.AsyncClient:
        """
        Return AsyncClient instance.
        """
        return self._client

    async def get(self, url: str, params: dict | None = None):
        """
        Execute GET request.
        """

        response = await self._client.get(
            url,
            params=params,
        )

        response.raise_for_status()

        return response.json()

    async def close(self) -> None:
        """
        Close HTTP connection pool.
        """

        await self._client.aclose()


binance_client = BinanceClient()



"""
Coinbase WebSocket Client

Production-ready asynchronous Coinbase Advanced Trade WebSocket client.
"""

# 