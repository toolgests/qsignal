"""
Binance Response Parser

Parses Binance REST and WebSocket responses into Pydantic models.
"""

from decimal import Decimal

from app.providers.binance.models.models import (
    Binance24HrTicker,
    BinanceKline,
    BinanceTicker,
    BinanceTrade,
)


class BinanceParser:
    """
    Parse Binance API responses into domain models.
    """

    @staticmethod
    def parse_ticker(data: dict) -> BinanceTicker:
        """
        Parse ticker price response.
        """
        return BinanceTicker(
            symbol=data["symbol"],
            price=Decimal(data["price"]),
        )

    @staticmethod
    def parse_24hr_ticker(data: dict) -> Binance24HrTicker:
        """
        Parse 24-hour ticker response.
        """
        return Binance24HrTicker(
            symbol=data["symbol"],
            last_price=Decimal(data["lastPrice"]),
            price_change=Decimal(data["priceChange"]),
            price_change_percent=Decimal(data["priceChangePercent"]),
            high_price=Decimal(data["highPrice"]),
            low_price=Decimal(data["lowPrice"]),
            open_price=Decimal(data["openPrice"]),
            volume=Decimal(data["volume"]),
        )

    @staticmethod
    def parse_kline(symbol: str, interval: str, data: list) -> BinanceKline:
        """
        Parse Binance kline response.
        """
        return BinanceKline(
            symbol=symbol,
            interval=interval,
            open_time=data[0],
            open=Decimal(data[1]),
            high=Decimal(data[2]),
            low=Decimal(data[3]),
            close=Decimal(data[4]),
            volume=Decimal(data[5]),
            close_time=data[6],
            closed=True,
        )

    @staticmethod
    def parse_trade(data: dict) -> BinanceTrade:
        """
        Parse WebSocket trade event.
        """
        return BinanceTrade(
            symbol=data["s"],
            trade_id=data["t"],
            price=Decimal(data["p"]),
            quantity=Decimal(data["q"]),
            trade_time=data["T"],
            is_buyer_maker=data["m"],
        )


binance_parser = BinanceParser()