"""
Finnhub Response Parser

Parses Finnhub REST and WebSocket responses into Pydantic models.
"""

from __future__ import annotations

from decimal import Decimal

from app.providers.finnhub.models.models import (
    FinnhubCandle,
    FinnhubCompanyProfile,
    FinnhubQuote,
    FinnhubSymbol,
)


class FinnhubParser:
    """
    Parse Finnhub API responses into Pydantic models.
    """

    @staticmethod
    def parse_quote(symbol: str, data: dict) -> FinnhubQuote:
        """
        Parse quote response.
        """

        return FinnhubQuote(
            symbol=symbol,
            current_price=Decimal(str(data["c"])),
            change=Decimal(str(data["d"])),
            percent_change=Decimal(str(data["dp"])),
            high=Decimal(str(data["h"])),
            low=Decimal(str(data["l"])),
            open=Decimal(str(data["o"])),
            previous_close=Decimal(str(data["pc"])),
            timestamp=data["t"],
        )

    @staticmethod
    def parse_symbols(data: list[dict]) -> list[FinnhubSymbol]:
        """
        Parse symbol list.
        """

        symbols: list[FinnhubSymbol] = []

        for item in data:
            symbols.append(
                FinnhubSymbol(
                    symbol=item["symbol"],
                    display_symbol=item["displaySymbol"],
                    description=item["description"],
                    currency=item["currency"],
                    exchange=item["mic"],
                    type=item["type"],
                )
            )

        return symbols

    @staticmethod
    def parse_company_profile(data: dict) -> FinnhubCompanyProfile:
        """
        Parse company profile.
        """

        return FinnhubCompanyProfile(
            ticker=data["ticker"],
            name=data["name"],
            country=data["country"],
            currency=data["currency"],
            exchange=data["exchange"],
            industry=data["finnhubIndustry"],
            ipo=data["ipo"],
            logo=data["logo"],
            market_capitalization=Decimal(
                str(data["marketCapitalization"])
            ),
            share_outstanding=Decimal(
                str(data["shareOutstanding"])
            ),
            weburl=data["weburl"],
        )

    @staticmethod
    def parse_candles(
        symbol: str,
        resolution: str,
        data: dict,
    ) -> list[FinnhubCandle]:
        """
        Parse candle response.
        """

        candles: list[FinnhubCandle] = []

        opens = data.get("o", [])
        highs = data.get("h", [])
        lows = data.get("l", [])
        closes = data.get("c", [])
        volumes = data.get("v", [])
        timestamps = data.get("t", [])

        for i in range(len(timestamps)):
            candles.append(
                FinnhubCandle(
                    symbol=symbol,
                    resolution=resolution,
                    open=Decimal(str(opens[i])),
                    high=Decimal(str(highs[i])),
                    low=Decimal(str(lows[i])),
                    close=Decimal(str(closes[i])),
                    volume=Decimal(str(volumes[i])),
                    timestamp=timestamps[i],
                )
            )

        return candles


finnhub_parser = FinnhubParser()