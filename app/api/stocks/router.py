# """
# Stocks API Router
# """

# from __future__ import annotations

# import time

# from fastapi import APIRouter, Query

# from app.api.stocks.schemas import (
#     CompanyProfileResponse,
#     StockCandleResponse,
#     StockQuoteResponse,
# )
# from app.api.stocks.service import stock_service
# from app.utils.validators import validate_stock_symbol

# router = APIRouter(
#     prefix="/stocks",
#     tags=["Stocks"],
# )


# @router.get("/{symbol}/quote", response_model=StockQuoteResponse)
# async def get_quote(symbol: str):
#     """
#     Get real-time stock quote.
#     """
#     symbol = validate_stock_symbol(symbol)
#     return await stock_service.get_quote(symbol)


# @router.get("/{symbol}/candles", response_model=list[StockCandleResponse])
# async def get_candles(
#     symbol: str,
#     resolution: str = Query(default="1"),
#     from_timestamp: int = Query(
#         default_factory=lambda: int(time.time()) - 86400
#     ),
#     to_timestamp: int = Query(default_factory=lambda: int(time.time())),
# ):
#     """
#     Get OHLC stock candles.
#     """
#     symbol = validate_stock_symbol(symbol)
#     return await stock_service.get_candles(
#         symbol,
#         resolution,
#         from_timestamp,
#         to_timestamp,
#     )


# @router.get("/{symbol}/profile", response_model=CompanyProfileResponse)
# async def get_company_profile(symbol: str):
#     """
#     Get company profile.
#     """
#     symbol = validate_stock_symbol(symbol)
#     return await stock_service.get_company_profile(symbol)


"""
Stocks API Router
"""

from __future__ import annotations

import time

from fastapi import APIRouter, Query

from app.api.stocks.schemas import (
    CompanyProfileResponse,
    StockCandleResponse,
    StockQuoteResponse,
)

from app.api.stocks.service import stock_service
from app.utils.validators import validate_stock_symbol


router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"],
)



@router.get(
    "/{symbol}/quote",
    response_model=StockQuoteResponse,
)
async def get_quote(
    symbol: str,
):
    """
    Get real-time stock quote from Redis.
    """

    symbol = validate_stock_symbol(
        symbol
    )

    return await stock_service.get_quote(
        symbol
    )



@router.get(
    "/{symbol}/candles",
    response_model=list[StockCandleResponse],
)
async def get_candles(
    symbol: str,

    resolution: str = Query(
        default="1"
    ),

    from_timestamp: int = Query(
        default_factory=lambda:
            int(time.time()) - 86400
    ),

    to_timestamp: int = Query(
        default_factory=lambda:
            int(time.time())
    ),
):
    """
    Get OHLC stock candles from Redis.
    """


    symbol = validate_stock_symbol(
        symbol
    )


    return await stock_service.get_candles(
        symbol=symbol,
        resolution=resolution,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
    )



@router.get(
    "/{symbol}/profile",
    response_model=CompanyProfileResponse,
)
async def get_company_profile(
    symbol: str,
):
    """
    Get company profile.
    """

    symbol = validate_stock_symbol(
        symbol
    )


    return await stock_service.get_company_profile(
        symbol
    )