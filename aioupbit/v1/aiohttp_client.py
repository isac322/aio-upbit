from __future__ import annotations

import datetime
import uuid
from typing import ClassVar, Iterable, Optional, Sequence, Union, overload

import aiohttp.connector
import orjson

from aioupbit.v1 import constants, values
from aioupbit.v1.client import Client

__all__ = ('AioHTTPRestClient',)


class AioHTTPRestClient(Client):
    __slots__ = ('_session',)

    _connector: ClassVar[Optional[aiohttp.BaseConnector]] = None

    _session: aiohttp.ClientSession

    def __init__(self, access_key: str, secret_key: str, connector: Optional[aiohttp.BaseConnector] = None) -> None:
        super().__init__(access_key, secret_key)

        if connector is None:
            connector = self._connector

        self._session = aiohttp.ClientSession(
            self.BASE_URL,
            connector=connector,
            connector_owner=connector is None,
        )

    @classmethod
    async def set_class_level_connector(cls, connector: aiohttp.BaseConnector) -> None:
        cls._connector = connector

    @classmethod
    def _get_class_level_session(cls) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            cls.BASE_URL,
            connector=cls._connector,
            connector_owner=cls._connector is None,
        )

    @classmethod
    async def markets(cls) -> Iterable[values.Ticker]:
        async with cls._get_class_level_session() as session:
            async with session.get('/v1/market/all?isDetails=true') as res:
                return map(values.Ticker.from_json, await res.json(loads=orjson.loads))

    @classmethod
    async def candles(
        cls,
        ticker: Union[values.Ticker, str],
        unit: values.MinCandle.Unit = values.MinCandle.Unit.MIN1,
        count: int = 1,
        to: Optional[datetime.datetime] = None,
    ) -> Iterable[values.MinCandle]:
        """
        If `to` exists and naive, it treated as UTC. (note. datetime.utcnow() returns naive datetime object)
        """
        async with cls._get_class_level_session() as session:
            params = dict(market=cls._get_ticker_code(ticker), count=count)
            if to is not None:
                params['to'] = to.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            async with session.get(f'/v1/candles/minutes/{unit.value}', params=params) as res:
                return map(values.MinCandle.from_json, await res.json(loads=orjson.loads))

    @classmethod
    async def candles_day(
        cls,
        ticker: Union[values.Ticker, str],
        count: int = 1,
        to: Optional[datetime.datetime] = None,
        converting_price_unit: Optional[constants.CurrencyCode] = None,
    ) -> Iterable[values.DayCandle]:
        """
        If `to` exists and naive, it treated as UTC. (note. datetime.utcnow() returns naive datetime object)
        """
        async with cls._get_class_level_session() as session:
            params = dict(market=cls._get_ticker_code(ticker), count=count)
            if to is not None:
                params['to'] = to.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            if converting_price_unit is not None:
                params['convertingPriceUnit'] = converting_price_unit
            async with session.get('/v1/candles/days', params=params) as res:
                return map(values.DayCandle.from_json, await res.json(loads=orjson.loads))

    @classmethod
    async def candles_week(
        cls,
        ticker: Union[values.Ticker, str],
        count: int = 1,
        to: Optional[datetime.datetime] = None,
    ) -> Iterable[values.WeekCandle]:
        """
        If `to` exists and naive, it treated as UTC. (note. datetime.utcnow() returns naive datetime object)
        """
        async with cls._get_class_level_session() as session:
            params = dict(market=cls._get_ticker_code(ticker), count=count)
            if to is not None:
                params['to'] = to.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            async with session.get('/v1/candles/weeks', params=params) as res:
                return map(values.WeekCandle.from_json, await res.json(loads=orjson.loads))

    @classmethod
    async def candles_month(
        cls,
        ticker: Union[values.Ticker, str],
        count: int = 1,
        to: Optional[datetime.datetime] = None,
    ) -> Iterable[values.MonthCandle]:
        """
        If `to` exists and naive, it treated as UTC. (note. datetime.utcnow() returns naive datetime object)
        """
        async with cls._get_class_level_session() as session:
            params = dict(market=cls._get_ticker_code(ticker), count=count)
            if to is not None:
                params['to'] = to.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            async with session.get('/v1/candles/months', params=params) as res:
                return map(values.MonthCandle.from_json, await res.json(loads=orjson.loads))

    @classmethod
    async def latest_trades(
        cls,
        ticker: Union[values.Ticker, str],
        to: Optional[datetime.time] = None,
        count: int = 1,
        cursor: Optional[int] = None,
        days_ago: constants.DaysAgo = 0,
    ) -> Iterable[values.Trade]:
        """
        If `to` exists and naive, it treated as UTC. (note. datetime.utcnow() returns naive datetime object)
        """
        async with cls._get_class_level_session() as session:
            params = dict(market=cls._get_ticker_code(ticker), count=count)
            if days_ago > 0:
                params['daysAgo'] = days_ago
            if cursor is not None:
                params['cursor'] = cursor
            if to is not None:
                params['to'] = to.isoformat()
            async with session.get('/v1/trades/ticks', params=params) as res:
                return map(values.Trade.from_json, await res.json(loads=orjson.loads))

    @classmethod
    async def latest_tick(cls, markets: Union[Iterable[values.Ticker], Iterable[str]]) -> Iterable[values.Tick]:
        async with cls._get_class_level_session() as session:
            params = dict(markets=','.join(map(cls._get_ticker_code, markets)))
            async with session.get('/v1/ticker', params=params) as res:
                return map(values.Tick.from_json, await res.json(loads=orjson.loads))

    @classmethod
    async def orderbook(cls, markets: Union[Iterable[values.Ticker], Iterable[str]]) -> Iterable[values.Orderbook]:
        async with cls._get_class_level_session() as session:
            params = dict(markets=','.join(map(cls._get_ticker_code, markets)))
            async with session.get('/v1/orderbook', params=params) as res:
                return map(values.Orderbook.from_json, await res.json(loads=orjson.loads))

    async def accounts(self) -> Sequence[values.Account]:
        pass

    async def market_with_account(self, ticker: Union[values.Ticker, str]) -> values.MarketWithAccount:
        pass

    @overload
    async def get_order(self, *, order_uuid: Union[uuid.UUID, str]) -> values.OrderWithTrades | None:
        pass

    @overload
    async def get_order(self, *, order_id: str) -> values.OrderWithTrades | None:
        pass

    async def get_order(self, **kwargs: Union[uuid.UUID, str]) -> values.OrderWithTrades | None:
        pass

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
        pass

    @overload
    async def cancel_order(self, *, order_uuid: Union[uuid.UUID, str]) -> None:
        pass

    @overload
    async def cancel_order(self, *, order_id: str) -> None:
        pass

    async def cancel_order(self, **kwargs: Union[uuid.UUID, str]) -> None:
        pass
