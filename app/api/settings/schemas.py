"""
Settings API Schemas
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class PublicSettingsResponse(BaseModel):
    """
    Non-sensitive application settings exposed to clients.
    """

    model_config = ConfigDict(from_attributes=True)

    app_name: str
    app_version: str
    default_timeframe: str
    supported_timeframes: list[str]
    ws_heartbeat_interval: int
