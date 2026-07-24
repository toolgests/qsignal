"""
Signal Confidence Calculator

Calculates confidence score for generated trading signals.
"""

from __future__ import annotations


class ConfidenceCalculator:
    """
    Calculates signal confidence based on indicator votes.
    """

    def calculate(
        self,
        buy_votes: int,
        sell_votes: int,
        total_votes: int,
    ) -> dict:
        """
        Calculate confidence percentage.

        Returns:
            {
                "confidence": 87.5,
                "strength": "HIGH"
            }
        """

        if total_votes <= 0:
            return {
                "confidence": 0.0,
                "strength": "NONE",
            }

        dominant = max(buy_votes, sell_votes)

        confidence = round(
            (dominant / total_votes) * 100,
            2,
        )

        if confidence >= 90:
            strength = "VERY HIGH"

        elif confidence >= 75:
            strength = "HIGH"

        elif confidence >= 60:
            strength = "MEDIUM"

        elif confidence >= 50:
            strength = "LOW"

        else:
            strength = "VERY LOW"

        return {
            "confidence": confidence,
            "strength": strength,
        }


confidence_calculator = ConfidenceCalculator()