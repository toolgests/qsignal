
"""
Health Service

Provides health and readiness information for the application.
"""

from datetime import UTC, datetime

from app.core.config import config


class HealthService:
    """
    Service responsible for application health information.
    """

    @staticmethod
    async def get_health() -> dict:
        """
        Return application health information.
        """

        return {
            "success": True,
            "application": config.APP_NAME,
            "version": config.APP_VERSION,
            "status": "healthy",
            "environment": "development" if config.DEBUG else "production",
            "timestamp": datetime.now(UTC).isoformat(),
        }

    @staticmethod
    async def get_liveness() -> dict:
        """
        Liveness probe.
        """

        return {
            "status": "alive"
        }

    @staticmethod
    async def get_readiness() -> dict:
        """
        Readiness probe.
        """

        return {
            "status": "ready"
        }


health_service = HealthService()

