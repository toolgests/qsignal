"""
Timeframe Manager

Centralized timeframe configuration and conversion utilities.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta


class TimeframeManager:
    """
    Manages supported trading timeframes.
    """

    _TIMEFRAMES: dict[str, int] = {
        "1m": 1,
        "5m": 5,
        "15m": 15,
        "30m": 30,
        "1h": 60,
        "4h": 240,
        "1d": 1440,
    }

    def supported(self) -> list[str]:
        """
        Return supported timeframes.
        """

        return list(self._TIMEFRAMES.keys())

    def exists(
        self,
        timeframe: str,
    ) -> bool:
        """
        Check if timeframe exists.
        """

        return timeframe in self._TIMEFRAMES

    def to_minutes(
        self,
        timeframe: str,
    ) -> int:
        """
        Convert timeframe string to minutes.
        """

        if timeframe not in self._TIMEFRAMES:
            raise ValueError(
                f"Unsupported timeframe: {timeframe}"
            )

        return self._TIMEFRAMES[timeframe]

    def from_minutes(
        self,
        minutes: int,
    ) -> str:
        """
        Convert minutes to timeframe string.
        """

        for tf, value in self._TIMEFRAMES.items():

            if value == minutes:
                return tf

        raise ValueError(
            f"No timeframe for {minutes} minutes."
        )

    def candle_start(
        self,
        timestamp: datetime,
        timeframe: str,
    ) -> datetime:
        """
        Calculate candle opening time.
        """

        timestamp = timestamp.astimezone(UTC)

        minutes = self.to_minutes(timeframe)

        if minutes < 60:

            minute = (
                timestamp.minute // minutes
            ) * minutes

            return timestamp.replace(
                minute=minute,
                second=0,
                microsecond=0,
            )

        if timeframe == "1h":

            return timestamp.replace(
                minute=0,
                second=0,
                microsecond=0,
            )

        if timeframe == "4h":

            hour = (
                timestamp.hour // 4
            ) * 4

            return timestamp.replace(
                hour=hour,
                minute=0,
                second=0,
                microsecond=0,
            )

        return timestamp.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

    def candle_close(
        self,
        timestamp: datetime,
        timeframe: str,
    ) -> datetime:
        """
        Calculate candle closing time.
        """

        start = self.candle_start(
            timestamp,
            timeframe,
        )

        minutes = self.to_minutes(
            timeframe,
        )

        return start + timedelta(
            minutes=minutes,
        )

    def next_candle(
        self,
        timeframe: str,
    ) -> datetime:
        """
        Return next candle opening time.
        """

        now = datetime.now(UTC)

        return self.candle_close(
            now,
            timeframe,
        )


timeframe_manager = TimeframeManager()