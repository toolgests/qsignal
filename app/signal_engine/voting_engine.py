"""
Signal Voting Engine

Generates BUY / SELL signals using indicator voting.
"""

from __future__ import annotations

from collections import Counter


class VotingEngine:
    """
    Indicator voting engine.
    """

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    STRONG_BUY = "STRONG BUY"
    STRONG_SELL = "STRONG SELL"

    def vote(self, indicators: dict) -> dict:
        """
        Generate final trading signal.
        """

        votes: list[str] = []

        # RSI
        rsi = indicators.get("rsi_14")

        if rsi is not None:
            if rsi < 30:
                votes.append(self.BUY)
            elif rsi > 70:
                votes.append(self.SELL)

        # EMA
        ema = indicators.get("ema_20")
        sma = indicators.get("sma_20")
        close = indicators.get("close")

        if close and ema:
            votes.append(
                self.BUY if close > ema else self.SELL
            )

        if close and sma:
            votes.append(
                self.BUY if close > sma else self.SELL
            )

        # MACD
        macd = indicators.get("macd")
        signal = indicators.get("macd_signal")

        if macd is not None and signal is not None:
            votes.append(
                self.BUY if macd > signal else self.SELL
            )

        # ADX
        adx = indicators.get("adx_14")

        if adx is not None:
            if adx >= 25:
                votes.append(self.BUY)
            else:
                votes.append(self.HOLD)

        # Bollinger
        upper = indicators.get("bb_upper")
        lower = indicators.get("bb_lower")

        if (
            upper is not None
            and lower is not None
            and close is not None
        ):
            if close <= lower:
                votes.append(self.BUY)
            elif close >= upper:
                votes.append(self.SELL)

        # VWAP
        vwap = indicators.get("vwap")

        if vwap is not None and close is not None:
            votes.append(
                self.BUY if close > vwap else self.SELL
            )

        counter = Counter(votes)

        buy = counter[self.BUY]
        sell = counter[self.SELL]

        if buy >= 6:
            signal = self.STRONG_BUY
        elif sell >= 6:
            signal = self.STRONG_SELL
        elif buy > sell:
            signal = self.BUY
        elif sell > buy:
            signal = self.SELL
        else:
            signal = self.HOLD

        return {
            "signal": signal,
            "buy_votes": buy,
            "sell_votes": sell,
            "votes": dict(counter),
        }


voting_engine = VotingEngine()