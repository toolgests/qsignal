# """
# Binance Data Models

# Pydantic models for Binance REST and WebSocket payloads.
# """

# from decimal import Decimal

# from pydantic import BaseModel, ConfigDict


# class BinanceTicker(BaseModel):
#     """
#     Binance ticker price.
#     """

#     model_config = ConfigDict(from_attributes=True)

#     symbol: str
#     price: Decimal


# class Binance24HrTicker(BaseModel):
#     """
#     Binance 24-hour ticker statistics.
#     """

#     model_config = ConfigDict(from_attributes=True)

#     symbol: str

#     last_price: Decimal

#     price_change: Decimal

#     price_change_percent: Decimal

#     high_price: Decimal

#     low_price: Decimal

#     open_price: Decimal

#     volume: Decimal


# class BinanceKline(BaseModel):
#     """
#     Binance OHLC Candle.
#     """

#     model_config = ConfigDict(from_attributes=True)

#     symbol: str

#     interval: str

#     open_time: int

#     close_time: int

#     open: Decimal

#     high: Decimal

#     low: Decimal

#     close: Decimal

#     volume: Decimal

#     closed: bool


# class BinanceTrade(BaseModel):
#     """
#     Binance trade event.
#     """

#     model_config = ConfigDict(from_attributes=True)

#     symbol: str

#     trade_id: int

#     price: Decimal

#     quantity: Decimal

#     trade_time: int

#     is_buyer_maker: bool


"""
Binance Data Models

(Powered by Coinbase WebSocket)
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BinanceTicker(BaseModel):
    """
    Generic ticker price.
    """

    model_config = ConfigDict(from_attributes=True)

    symbol: str
    price: Decimal


class Binance24HrTicker(BaseModel):
    """
    Generic 24-hour ticker statistics.
    """

    model_config = ConfigDict(from_attributes=True)

    symbol: str

    last_price: Decimal

    price_change: Decimal

    price_change_percent: Decimal

    high_price: Decimal

    low_price: Decimal

    open_price: Decimal

    volume: Decimal


class BinanceKline(BaseModel):
    """
    Generic OHLC Candle.
    """

    model_config = ConfigDict(from_attributes=True)

    symbol: str

    interval: str

    open_time: int

    close_time: int

    open: Decimal

    high: Decimal

    low: Decimal

    close: Decimal

    volume: Decimal

    closed: bool


class BinanceTrade(BaseModel):
    """
    Coinbase trade event (using Binance model name
    to avoid changing the rest of the project).
    """

    model_config = ConfigDict(from_attributes=True)

    symbol: str

    # Coinbase trade_id may not always be available
    trade_id: str | int | None = None

    price: Decimal

    quantity: Decimal

    # Unix timestamp in milliseconds
    trade_time: int

    # Not provided by Coinbase market_trades
    is_buyer_maker: bool | None = None