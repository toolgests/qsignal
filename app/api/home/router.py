"""
Home API Router
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.home.schemas import HomeResponse
from app.api.home.service import home_service

router = APIRouter(
    prefix="/home",
    tags=["Home"],
)


@router.get(
    "",
    response_model=HomeResponse,
    summary="Homepage Market Snapshot",
    description="""
Returns latest market data required for homepage.

Includes:
- Crypto
- Stocks
- Forex

Each symbol contains:
- Latest live price
- Last 200 candles
    - 1m
    - 5m
    - 15m
    - 60m
""",
)
async def get_home():
    """
    Homepage API

    Response Example

    {
        "crypto": [...],
        "stocks": [...],
        "forex": [...]
    }
    """

    return await home_service.get_home()


@router.get(
    "/health",
    tags=["Home"],
)
async def health():
    """
    Health check endpoint.
    """

    return JSONResponse(
        {
            "success": True,
            "message": "Home API Working"
        }
    )


@router.get(
    "/redis-test",
    tags=["Debug"],
)
async def redis_test():
    """
    Debug endpoint.

    Verify Redis contains homepage data.
    """

    return await home_service.redis_test()