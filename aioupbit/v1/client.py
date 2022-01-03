from __future__ import annotations

import datetime
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from typing import Optional, Union

from aioupbit.v1 import const, value


class Client(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    async def markets(cls) -> Iterable[value.Market]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def candles(
        cls,
        market: Union[value.Market, str],
        unit: const.CandleUnit = const.CandleUnit.MIN1,
        count: int = 1,
        to: Optional[datetime.datetime] = None,
    ) -> Iterable[value.Market]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def latest_tick(cls, markets: Union[Iterable[value.Market], Iterable[str]]) -> Iterable[value.Tick]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def orderbook(cls, markets: Union[Iterable[value.Market], Iterable[str]]) -> Iterable[value.Orderbook]:
        raise NotImplementedError
