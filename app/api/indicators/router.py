# from fastapi import APIRouter, Query

# from app.api.indicators.service import indicators_api_service

# router = APIRouter(
#     prefix="/indicators",
#     tags=["Indicators"],
# )


# @router.get("/{symbol}")
# async def get_indicators(
#     symbol: str,
#     timeframe: str = Query(default="1m"),
# ):

#     data = await indicators_api_service.get_latest_indicators(
#         symbol=symbol,
#         timeframe=timeframe,
#     )

#     return {
#         "symbol": symbol.upper(),
#         "timeframe": timeframe,
#         "indicators": data,
#     }


from fastapi import APIRouter, Query

from app.api.indicators.service import indicators_api_service

router = APIRouter(
    prefix="/indicators",
    tags=["Indicators"],
)


@router.get("/{symbol}")
async def get_indicators(
    symbol: str,
    timeframe: str = Query(default="1m"),
):
    indicators = await indicators_api_service.get_latest_indicators(
        symbol=symbol,
        timeframe=timeframe,
    )

    return {
        "symbol": symbol.upper(),
        "timeframe": timeframe,
        "indicators": indicators,
    }