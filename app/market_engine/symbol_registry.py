"""
Symbol Registry

Central registry for all supported trading symbols.

Responsibilities:
    • Register symbols
    • Validate symbols
    • Group symbols by market
    • Fast lookup
"""

from __future__ import annotations

from collections import defaultdict


class SymbolRegistry:
    """
    Registry for trading symbols.
    """

    def __init__(self) -> None:
        self._symbols: dict[str, set[str]] = defaultdict(set)

    def register(
        self,
        market: str,
        symbol: str,
    ) -> None:
        """
        Register a trading symbol.
        """

        self._symbols[market.lower()].add(
            symbol.upper()
        )

    def register_many(
        self,
        market: str,
        symbols: list[str],
    ) -> None:
        """
        Register multiple symbols.
        """

        for symbol in symbols:
            self.register(
                market=market,
                symbol=symbol,
            )

    def unregister(
        self,
        market: str,
        symbol: str,
    ) -> None:
        """
        Remove a symbol.
        """

        self._symbols[
            market.lower()
        ].discard(symbol.upper())

    def exists(
        self,
        symbol: str,
    ) -> bool:
        """
        Check if symbol exists.
        """

        symbol = symbol.upper()

        return any(
            symbol in symbols
            for symbols in self._symbols.values()
        )

    def exists_in_market(
        self,
        market: str,
        symbol: str,
    ) -> bool:
        """
        Check if symbol exists in a market.
        """

        return (
            symbol.upper()
            in self._symbols.get(
                market.lower(),
                set(),
            )
        )

    def get_market(
        self,
        symbol: str,
    ) -> str | None:
        """
        Return market for a symbol.
        """

        symbol = symbol.upper()

        for market, symbols in self._symbols.items():

            if symbol in symbols:
                return market

        return None

    def get_symbols(
        self,
        market: str,
    ) -> list[str]:
        """
        Return symbols for a market.
        """

        return sorted(
            self._symbols.get(
                market.lower(),
                set(),
            )
        )

    def all(self) -> dict[str, list[str]]:
        """
        Return all registered symbols.
        """

        return {
            market: sorted(symbols)
            for market, symbols in self._symbols.items()
        }

    def clear_market(
        self,
        market: str,
    ) -> None:
        """
        Remove all symbols for a market.
        """

        self._symbols.pop(
            market.lower(),
            None,
        )

    def clear(self) -> None:
        """
        Clear registry.
        """

        self._symbols.clear()

    @property
    def total_markets(self) -> int:
        """
        Total registered markets.
        """

        return len(self._symbols)

    @property
    def total_symbols(self) -> int:
        """
        Total registered symbols.
        """

        return sum(
            len(symbols)
            for symbols in self._symbols.values()
        )


symbol_registry = SymbolRegistry()