from __future__ import annotations

import datetime
import hashlib
import uuid
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from typing import Optional, Sequence, Union, overload

import jwt
from typing_extensions import Final

from aioupbit.v1 import constants, values

__all__ = ('Client',)


class Client(metaclass=ABCMeta):
    __slots__ = ('_access_key', '_secret_key')
    BASE_URL: Final[str] = 'https://api.upbit.com'

    _access_key: Final[str]
    _secret_key: Final[str]

    def __init__(self, access_key: str, secret_key: str) -> None:
        super().__init__()

        self._access_key = access_key
        self._secret_key = secret_key

    @classmethod
    def _get_ticker_code(cls, ticker: Union[values.Ticker, str]) -> str:
        if isinstance(ticker, values.Ticker):
            return ticker.ticker
        return ticker

    @classmethod
    @abstractmethod
    async def markets(cls) -> Iterable[values.Ticker]:
        """https://docs.upbit.com/reference/%EB%A7%88%EC%BC%93-%EC%BD%94%EB%93%9C-%EC%A1%B0%ED%9A%8C"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def candles(
        cls,
        ticker: Union[values.Ticker, str],
        unit: values.MinCandle.Unit = values.MinCandle.Unit.MIN1,
        count: int = 1,
        to: Optional[datetime.datetime] = None,
    ) -> Iterable[values.MinCandle]:
        """https://docs.upbit.com/reference/%EB%B6%84minute-%EC%BA%94%EB%93%A4-1"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def candles_day(
        cls,
        ticker: Union[values.Ticker, str],
        count: int = 1,
        to: Optional[datetime.datetime] = None,
        converting_price_unit: Optional[constants.CurrencyCode] = None,
    ) -> Iterable[values.DayCandle]:
        """https://docs.upbit.com/reference/%EC%9D%BCday-%EC%BA%94%EB%93%A4-1"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def candles_week(
        cls,
        ticker: Union[values.Ticker, str],
        count: int = 1,
        to: Optional[datetime.datetime] = None,
    ) -> Iterable[values.WeekCandle]:
        """https://docs.upbit.com/reference/%EC%A3%BCweek-%EC%BA%94%EB%93%A4-1"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def candles_month(
        cls,
        ticker: Union[values.Ticker, str],
        count: int = 1,
        to: Optional[datetime.datetime] = None,
    ) -> Iterable[values.MonthCandle]:
        """https://docs.upbit.com/reference/%EC%9B%94month-%EC%BA%94%EB%93%A4-1"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def latest_trades(
        cls,
        ticker: Union[values.Ticker, str],
        to: Optional[datetime.time] = None,
        count: int = 1,
        cursor: Optional[int] = None,
        days_ago: constants.DaysAgo = 0,
    ) -> Iterable[values.Trade]:
        """https://docs.upbit.com/reference/%EC%B5%9C%EA%B7%BC-%EC%B2%B4%EA%B2%B0-%EB%82%B4%EC%97%AD"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def latest_tick(cls, markets: Union[Iterable[values.Ticker], Iterable[str]]) -> Iterable[values.Tick]:
        """https://docs.upbit.com/reference/ticker%ED%98%84%EC%9E%AC%EA%B0%80-%EB%82%B4%EC%97%AD"""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def orderbook(cls, markets: Union[Iterable[values.Ticker], Iterable[str]]) -> Iterable[values.Orderbook]:
        """https://docs.upbit.com/reference/%ED%98%B8%EA%B0%80-%EC%A0%95%EB%B3%B4-%EC%A1%B0%ED%9A%8C"""
        raise NotImplementedError

    def _gen_auth_token(self, encoded_query_string: Optional[str] = None) -> str:
        payload = dict(
            access_key=self._access_key,
            nonce=str(uuid.uuid4()),
        )
        if encoded_query_string is not None:
            m = hashlib.sha512(encoded_query_string.encode())
            payload['query_hash'] = m.hexdigest()
            payload['query_hash_alg'] = m.name.upper()

        return f'Bearer {jwt.encode(payload, self._secret_key)}'

    @abstractmethod
    async def accounts(self) -> Sequence[values.Account]:
        """https://docs.upbit.com/reference/%EC%A0%84%EC%B2%B4-%EA%B3%84%EC%A2%8C-%EC%A1%B0%ED%9A%8C"""
        raise NotImplementedError

    @abstractmethod
    async def market_with_account(self, ticker: Union[values.Ticker, str]) -> values.MarketWithAccount:
        """https://docs.upbit.com/reference/%EC%A3%BC%EB%AC%B8-%EA%B0%80%EB%8A%A5-%EC%A0%95%EB%B3%B4"""
        raise NotImplementedError

    @overload
    async def get_order(self, *, order_uuid: Union[uuid.UUID, str]) -> values.OrderWithTrades | None:
        pass

    @overload
    async def get_order(self, *, order_id: str) -> values.OrderWithTrades | None:
        pass

    @abstractmethod
    async def get_order(self, **kwargs: Union[uuid.UUID, str]) -> values.OrderWithTrades | None:
        """https://docs.upbit.com/reference/%EA%B0%9C%EB%B3%84-%EC%A3%BC%EB%AC%B8-%EC%A1%B0%ED%9A%8C"""
        raise NotImplementedError

    @overload
    async def orders(
        self,
        *,
        ticker: Union[values.Ticker, str],
        uuids: Union[Iterable[uuid.UUID], Iterable[str]],
        identifiers: Iterable[str],
        state: constants.OrderState = constants.OrderState.WAIT,
        page: int = 1,
        limit: int = 100,
        order_by: constants.OrderBy = constants.OrderBy.DESC,
    ) -> Sequence[values.Order]:
        pass

    @overload
    async def orders(
        self,
        *,
        ticker: Union[values.Ticker, str],
        uuids: Union[Iterable[uuid.UUID], Iterable[str]],
        identifiers: Iterable[str],
        states: Iterable[constants.OrderState],
        page: int = 1,
        limit: int = 100,
        order_by: constants.OrderBy = constants.OrderBy.DESC,
    ) -> Sequence[values.Order]:
        pass

    @abstractmethod
    async def orders(
        self,
        *,
        ticker: Union[values.Ticker, str],
        uuids: Union[Iterable[uuid.UUID], Iterable[str]],
        identifiers: Iterable[str],
        page: int = 1,
        limit: int = 100,
        order_by: constants.OrderBy = constants.OrderBy.DESC,
        **kwargs: Union[constants.OrderState, Iterable[constants.OrderState]],
    ) -> Sequence[values.Order]:
        """https://docs.upbit.com/reference/%EC%A3%BC%EB%AC%B8-%EB%A6%AC%EC%8A%A4%ED%8A%B8-%EC%A1%B0%ED%9A%8C"""
        raise NotImplementedError

    @overload
    async def cancel_order(self, *, order_uuid: Union[uuid.UUID, str]) -> None:
        pass

    @overload
    async def cancel_order(self, *, order_id: str) -> None:
        pass

    @abstractmethod
    async def cancel_order(self, **kwargs: Union[uuid.UUID, str]) -> None:
        """https://docs.upbit.com/reference/%EC%A3%BC%EB%AC%B8-%EC%B7%A8%EC%86%8C"""
        raise NotImplementedError
