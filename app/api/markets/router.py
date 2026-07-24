"""
Markets API Router

Provides market information and supported symbols.
"""

from fastapi import APIRouter

from app.api.markets.schemas import (
    MarketListResponse,
    SymbolsResponse,
)
from app.api.markets.service import market_service

router = APIRouter(
    prefix="/markets",
    tags=["Markets"],
)


@router.get(
    "/",
    response_model=MarketListResponse,
    summary="Get Supported Markets",
)
async def get_markets():
    """
    Return available market types.
    """

    markets = await market_service.get_markets()

    return {
        "markets": markets
    }


@router.get(
    "/symbols",
    response_model=dict,
    summary="Get All Symbols",
)
async def get_symbols():
    """
    Return all supported symbols.
    """

    return await market_service.get_all_symbols()


@router.get(
    "/crypto",
    response_model=list[str],
    summary="Get Crypto Symbols",
)
async def get_crypto_symbols():
    """
    Return crypto symbols.
    """

    return await market_service.get_crypto_symbols()


@router.get(
    "/forex",
    response_model=list[str],
    summary="Get Forex Symbols",
)
async def get_forex_symbols():
    """
    Return forex symbols.
    """

    return await market_service.get_forex_symbols()


@router.get(
    "/stocks",
    response_model=list[str],
    summary="Get Stock Symbols",
)
async def get_stock_symbols():
    """
    Return stock symbols.
    """

    return await market_service.get_stock_symbols()