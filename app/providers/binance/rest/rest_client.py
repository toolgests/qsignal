
# """
# Binance REST Client

# Provides access to Binance REST API endpoints.
# """

# from __future__ import annotations

# from app.providers.binance.client.client import binance_client


# class BinanceRestClient:
#     """
#     Binance REST API wrapper.
#     """

#     async def get_exchange_info(self) -> dict:
#         """
#         Get exchange information.
#         """
#         return await binance_client.get("/api/v3/exchangeInfo")

#     async def get_symbols(self) -> list[str]:
#         """
#         Get all trading symbols.
#         """
#         data = await self.get_exchange_info()

#         return [
#             symbol["symbol"]
#             for symbol in data["symbols"]
#             if symbol["status"] == "TRADING"
#         ]

#     async def get_price(self, symbol: str) -> dict:
#         """
#         Get latest market price.
#         """
#         return await binance_client.get(
#             "/api/v3/ticker/price",
#             params={
#                 "symbol": symbol.upper(),
#             },
#         )

#     async def get_24hr_ticker(self, symbol: str) -> dict:
#         """
#         Get 24-hour ticker statistics.
#         """
#         return await binance_client.get(
#             "/api/v3/ticker/24hr",
#             params={
#                 "symbol": symbol.upper(),
#             },
#         )

#     async def get_order_book(
#         self,
#         symbol: str,
#         limit: int = 100,
#     ) -> dict:
#         """
#         Get market depth.
#         """
#         return await binance_client.get(
#             "/api/v3/depth",
#             params={
#                 "symbol": symbol.upper(),
#                 "limit": limit,
#             },
#         )

#     async def get_klines(
#         self,
#         symbol: str,
#         interval: str = "1m",
#         limit: int = 500,
#     ) -> list:
#         """
#         Get OHLC candlestick data.
#         """
#         return await binance_client.get(
#             "/api/v3/klines",
#             params={
#                 "symbol": symbol.upper(),
#                 "interval": interval,
#                 "limit": limit,
#             },
#         )


# binance_rest_client = BinanceRestClient()


"""
Binance REST Client

(Internally uses Coinbase REST API while keeping the same interface.)
"""

from __future__ import annotations

from app.providers.binance.client.client import binance_client


class BinanceRestClient:
    """
    Coinbase REST API wrapper.
    """

    async def get_exchange_info(self) -> dict:
        """
        Get available Coinbase products.
        """
        return await binance_client.get("/api/v3/brokerage/products")

    async def get_symbols(self) -> list[str]:
        """
        Get all trading products.
        """
        data = await self.get_exchange_info()

        return [
            product["product_id"]
            for product in data.get("products", [])
            if not product.get("trading_disabled", False)
        ]

    async def get_price(self, symbol: str) -> dict:
        """
        Get latest market price.
        """

        return await binance_client.get(
            f"/api/v3/brokerage/products/{symbol.upper()}"
        )

    async def get_24hr_ticker(self, symbol: str) -> dict:
        """
        Get 24-hour market statistics.
        """

        return await binance_client.get(
            f"/api/v3/brokerage/products/{symbol.upper()}"
        )

    async def get_order_book(
        self,
        symbol: str,
        limit: int = 100,
    ) -> dict:
        """
        Get order book.
        """

        return await binance_client.get(
            f"/api/v3/brokerage/product_book",
            params={
                "product_id": symbol.upper(),
                "limit": limit,
            },
        )

    async def get_klines(
        self,
        symbol: str,
        interval: str = "ONE_MINUTE",
        limit: int = 350,
    ) -> dict:
        """
        Get candle data.
        """

        return await binance_client.get(
            "/api/v3/brokerage/products/{}/candles".format(
                symbol.upper()
            ),
            params={
                "granularity": interval,
                "limit": limit,
            },
        )


binance_rest_client = BinanceRestClient()