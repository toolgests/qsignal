"""
Settings API Router
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.settings.schemas import PublicSettingsResponse
from app.api.settings.service import settings_service

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


@router.get("/", response_model=PublicSettingsResponse)
async def get_settings():
    """
    Return public application settings.
    """

    return await settings_service.get_public_settings()
