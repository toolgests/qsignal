"""
Finnhub HTTP Client

Shared asynchronous HTTP client for Finnhub REST API.
"""

from __future__ import annotations

import httpx

from app.core.config import config


class FinnhubClient:
    """
    Shared HTTP client for Finnhub API.
    """

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=config.FINNHUB_REST_URL,
            timeout=httpx.Timeout(10.0),
            headers={
                "X-Finnhub-Token": config.FINNHUB_API_KEY,
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

    async def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ):
        """
        Execute GET request.
        """

        params = params or {}

        response = await self._client.get(
            endpoint,
            params=params,
        )

        response.raise_for_status()

        return response.json()

    async def close(self) -> None:
        """
        Close HTTP connection pool.
        """

        await self._client.aclose()


finnhub_client = FinnhubClient()