"""
Settings Service

Exposes a safe, non-sensitive subset of application settings.
"""

from __future__ import annotations

from app.core.config import config


class SettingsService:
    """
    Service responsible for public settings.
    """

    async def get_public_settings(self) -> dict:
        """
        Return non-sensitive application settings.
        """

        return {
            "app_name": config.APP_NAME,
            "app_version": config.APP_VERSION,
            "default_timeframe": config.DEFAULT_TIMEFRAME,
            "supported_timeframes": config.SUPPORTED_TIMEFRAMES,
            "ws_heartbeat_interval": config.WS_HEARTBEAT_INTERVAL,
        }


settings_service = SettingsService()
