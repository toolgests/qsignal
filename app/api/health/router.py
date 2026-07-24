from fastapi import APIRouter

from app.api.health.schemas import (
    HealthResponse,
    StatusResponse,
)
from app.api.health.service import health_service

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "/",
    response_model=HealthResponse,
)
async def health():
    return await health_service.get_health()


@router.get(
    "/live",
    response_model=StatusResponse,
)
async def live():
    return await health_service.get_liveness()


@router.get(
    "/ready",
    response_model=StatusResponse,
)
async def ready():
    return await health_service.get_readiness()