"""Provider registry."""

from __future__ import annotations

from typing import Iterable

from pf.data.providers.base import DataProvider
from pf.data.providers.stooq import StooqProvider


class ProviderRegistry:

    def __init__(self) -> None:
        self._providers: dict[str, DataProvider] = {
            StooqProvider.name: StooqProvider(),
        }

    def names(self) -> Iterable[str]:
        return self._providers.keys()

    def get(self, name: str) -> DataProvider:
        return self._providers[name]


provider_registry = ProviderRegistry()
