"""
Q Signals - Main API Router

Central router for all API modules.
"""

from fastapi import APIRouter

from app.api.crypto.router import router as crypto_router
from app.api.forex.router import router as forex_router
from app.api.health.router import router as health_router
from app.api.indicators.router import router as indicators_router
from app.api.markets.router import router as markets_router
from app.api.settings.router import router as settings_router
from app.api.home.router import router as home_router
from app.api.signals.router import router as signals_router
from app.api.stocks.router import router as stocks_router
from app.core.constants import API_PREFIX


# ---------------------------------------------------------------------
# Main API Router
# ---------------------------------------------------------------------

api_router = APIRouter(
    prefix=API_PREFIX,
)
api_router.include_router(health_router)
api_router.include_router(markets_router)
api_router.include_router(crypto_router)
api_router.include_router(forex_router)
api_router.include_router(stocks_router)
api_router.include_router(indicators_router)
api_router.include_router(home_router)
api_router.include_router(signals_router)
api_router.include_router(settings_router)




