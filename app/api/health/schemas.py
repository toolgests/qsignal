
"""
Health API Schemas

Response models for Health endpoints.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """
    Health response model.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    success: bool
    application: str
    version: str
    status: str
    environment: str
    timestamp: datetime


class StatusResponse(BaseModel):
    """
    Simple status response.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    status: str

