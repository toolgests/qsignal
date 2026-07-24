# """
# Forex API Schemas
# """

# from __future__ import annotations

# from decimal import Decimal

# from pydantic import BaseModel, ConfigDict


# class ForexQuoteResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     symbol: str
#     current_price: Decimal
#     change: Decimal
#     percent_change: Decimal
#     high: Decimal
#     low: Decimal
#     open: Decimal
#     previous_close: Decimal
#     timestamp: int


# class ForexCandleResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     symbol: str
#     resolution: str
#     open: Decimal
#     high: Decimal
#     low: Decimal
#     close: Decimal
#     volume: Decimal
#     timestamp: int


from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ForexQuoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    market: str
    price: Decimal
    volume: Decimal
    timestamp: str


class ForexCandleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    resolution: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    timestamp: int