"""
Indicators API Schemas
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class IndicatorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    timeframe: str
    indicators: dict[str, Any]
