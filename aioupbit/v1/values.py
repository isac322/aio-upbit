from __future__ import annotations

import datetime
from abc import ABCMeta
from dataclasses import dataclass
from decimal import Decimal
from enum import IntEnum
from typing import AbstractSet, Any, Mapping, Optional, Sequence, Type, TypeVar
from uuid import UUID

try:
    from zoneinfo import ZoneInfo  # type: ignore[import]
except ImportError:
    from backports.zoneinfo import ZoneInfo  # type: ignore[import]

from aioupbit.v1 import constants

__all__ = (
    'Ticker',
    'BaseCandle',
    'MinCandle',
    'DayCandle',
    'WeekCandle',
    'MonthCandle',
    'Trade',
    'Tick',
    'Orderbook',
    'Account',
    'OrderConfig',
    'Market',
    'MarketWithAccount',
    'Order',
    'OrderWithTrades',
)


@dataclass(frozen=True)
class Ticker:
    __slots__ = ('ticker', 'korean_name', 'english_name', 'warning')

    ticker: str
    korean_name: str
    english_name: str
    warning: constants.MarketWarning

    @classmethod
    def from_json(cls, json: Mapping[str, Any]) -> Ticker:
        return cls(
            ticker=json['market'],
            korean_name=json['korean_name'],
            english_name=json['english_name'],
            warning=constants.MarketWarning(json['market_warning']),
        )


@dataclass(frozen=True)
class BaseCandle(metaclass=ABCMeta):
    __slots__ = (
        'ticker',
        'date_time',
        'opening_price',
        'high_price',
        'low_price',
        'trade_price',
        'latest_tick_timestamp',
        'acc_trade_price',
        'acc_trade_volume',
    )

    ticker: str
    date_time: datetime.datetime
    opening_price: Decimal
    high_price: Decimal
    low_price: Decimal
    trade_price: Decimal
    latest_tick_timestamp: datetime.datetime
    acc_trade_price: Decimal
    acc_trade_volume: Decimal


@dataclass(frozen=True)
class MinCandle(BaseCandle):
    __slots__ = ('unit',)

    class Unit(IntEnum):
        MIN1 = 1
        MIN3 = 3
        MIN5 = 5
        MIN10 = 10
        MIN15 = 15
        MIN30 = 30
        MIN60 = 60
        MIN240 = 240

    unit: Unit

    @classmethod
    def from_json(cls, json: Mapping[str, Any]) -> MinCandle:
        return cls(
            ticker=json['market'],
            date_time=json['candle_date_time_utc'],
            opening_price=json['opening_price'],
            high_price=json['high_price'],
            low_price=json['low_price'],
            trade_price=json['trade_price'],
            latest_tick_timestamp=datetime.datetime.fromtimestamp(json['timestamp'] / 1000, datetime.timezone.utc),
            acc_trade_price=json['candle_acc_trade_price'],
            acc_trade_volume=json['candle_acc_trade_volume'],
            unit=cls.Unit(json['unit']),
        )


@dataclass(frozen=True)
class DayCandle(BaseCandle):
    __slots__ = ('prev_closing_price', 'change_price', 'change_rate', 'converted_trade_price')

    prev_closing_price: Decimal
    change_price: Decimal
    change_rate: Decimal
    converted_trade_price: Optional[Decimal]

    @classmethod
    def from_json(cls, json: Mapping[str, Any]) -> DayCandle:
        return cls(
            ticker=json['market'],
            date_time=json['candle_date_time_utc'],
            opening_price=json['opening_price'],
            high_price=json['high_price'],
            low_price=json['low_price'],
            trade_price=json['trade_price'],
            latest_tick_timestamp=datetime.datetime.fromtimestamp(json['timestamp'] / 1000, datetime.timezone.utc),
            acc_trade_price=json['candle_acc_trade_price'],
            acc_trade_volume=json['candle_acc_trade_volume'],
            prev_closing_price=json['prev_closing_price'],
            change_price=json['change_price'],
            change_rate=json['change_rate'],
            converted_trade_price=json.get('converted_trade_price'),
        )


_SelfWeekCandle = TypeVar('_SelfWeekCandle', bound='WeekCandle')


@dataclass(frozen=True)
class WeekCandle(BaseCandle):
    __slots__ = ('first_day_of_period',)

    first_day_of_period: datetime.date

    @classmethod
    def from_json(cls: Type[_SelfWeekCandle], json: Mapping[str, Any]) -> _SelfWeekCandle:
        return cls(
            ticker=json['market'],
            date_time=json['candle_date_time_utc'],
            opening_price=json['opening_price'],
            high_price=json['high_price'],
            low_price=json['low_price'],
            trade_price=json['trade_price'],
            latest_tick_timestamp=datetime.datetime.fromtimestamp(json['timestamp'] / 1000, datetime.timezone.utc),
            acc_trade_price=json['candle_acc_trade_price'],
            acc_trade_volume=json['candle_acc_trade_volume'],
            first_day_of_period=json['first_day_of_period'],
        )


@dataclass(frozen=True)
class MonthCandle(WeekCandle):
    pass


@dataclass(frozen=True)
class Trade:
    __slots__ = (
        'ticker',
        'timestamp',
        'trade_price',
        'trade_volume',
        'prev_closing_price',
        'change_price',
        'side',
        'sequential_id',
    )

    ticker: str
    timestamp: datetime.datetime
    trade_price: Decimal
    trade_volume: Decimal
    prev_closing_price: Decimal
    change_price: Decimal
    side: constants.Side
    sequential_id: int

    @classmethod
    def from_json(cls, json: Mapping[str, Any]) -> Trade:
        return cls(
            ticker=json['market'],
            timestamp=datetime.datetime.fromtimestamp(json['timestamp'] / 1000, datetime.timezone.utc),
            trade_price=json['trade_price'],
            trade_volume=json['trade_volume'],
            prev_closing_price=json['prev_closing_price'],
            change_price=json['change_price'],
            side=constants.Side(json['ask_bid']),
            sequential_id=json['sequential_id'],
        )


@dataclass(frozen=True)
class Tick:
    __slots__ = (
        'ticker',
        'trade_date_time',
        'opening_price',
        'high_price',
        'low_price',
        'trade_price',
        'prev_closing_price',
        'change',
        'change_price',
        'change_rate',
        'signed_change_price',
        'signed_change_rate',
        'trade_volume',
        'acc_trade_price',
        'acc_trade_price_24h',
        'acc_trade_volume',
        'acc_trade_volume_24h',
        'highest_52_week_price',
        'highest_52_week_date',
        'lowest_52_week_price',
        'lowest_52_week_date',
        'timestamp',
    )

    ticker: str
    trade_date_time: datetime.datetime
    opening_price: Decimal
    high_price: Decimal
    low_price: Decimal
    trade_price: Decimal
    prev_closing_price: Decimal
    change: constants.Change
    change_price: Decimal
    change_rate: Decimal
    signed_change_price: Decimal
    signed_change_rate: Decimal
    trade_volume: Decimal
    acc_trade_price: Decimal
    acc_trade_price_24h: Decimal
    acc_trade_volume: Decimal
    acc_trade_volume_24h: Decimal
    highest_52_week_price: Decimal
    highest_52_week_date: datetime.date
    lowest_52_week_price: Decimal
    lowest_52_week_date: datetime.date
    timestamp: datetime.datetime

    @classmethod
    def from_json(cls, json: Mapping[str, Any]) -> Tick:
        return cls(
            ticker=json['market'],
            trade_date_time=datetime.datetime.fromtimestamp(json['trade_timestamp'] / 1000, ZoneInfo('Asia/Seoul')),
            opening_price=json['opening_price'],
            high_price=json['high_price'],
            low_price=json['low_price'],
            trade_price=json['trade_price'],
            prev_closing_price=json['prev_closing_price'],
            change=constants.Change(json['change']),
            change_price=json['change_price'],
            change_rate=json['change_rate'],
            signed_change_price=json['signed_change_price'],
            signed_change_rate=json['signed_change_rate'],
            trade_volume=json['trade_volume'],
            acc_trade_price=json['acc_trade_price'],
            acc_trade_price_24h=json['acc_trade_price_24h'],
            acc_trade_volume=json['acc_trade_volume'],
            acc_trade_volume_24h=json['acc_trade_volume_24h'],
            highest_52_week_price=json['highest_52_week_price'],
            highest_52_week_date=json['highest_52_week_date'],
            lowest_52_week_price=json['lowest_52_week_price'],
            lowest_52_week_date=json['lowest_52_week_date'],
            timestamp=datetime.datetime.fromtimestamp(json['timestamp'] / 1000, datetime.timezone.utc),
        )


@dataclass(frozen=True)
class Orderbook:
    __slots__ = ('ticker', 'timestamp', 'total_ask_size', 'total_bid_size', 'orderbook_units')

    @dataclass(frozen=True)
    class Unit:
        __slots__ = ('ask_price', 'bid_price', 'ask_size', 'bid_size')

        ask_price: Decimal
        bid_price: Decimal
        ask_size: Decimal
        bid_size: Decimal

        @classmethod
        def from_json(cls, json: Mapping[str, Any]) -> Orderbook.Unit:
            return cls(
                ask_price=json['ask_price'],
                bid_price=json['bid_price'],
                ask_size=json['ask_size'],
                bid_size=json['bid_size'],
            )

    ticker: str
    timestamp: datetime.datetime
    total_ask_size: Decimal
    total_bid_size: Decimal
    orderbook_units: Sequence[Unit]

    @classmethod
    def from_json(cls, json: Mapping[str, Any]) -> Orderbook:
        return cls(
            ticker=json['market'],
            timestamp=datetime.datetime.fromtimestamp(json['timestamp'] / 1000, ZoneInfo('Asia/Seoul')),
            total_ask_size=json['total_ask_size'],
            total_bid_size=json['total_bid_size'],
            orderbook_units=tuple(map(cls.Unit.from_json, json['orderbook_units'])),
        )


@dataclass(frozen=True)
class Account:
    currency: constants.CurrencyCode
    balance: Decimal
    locked: Decimal
    avg_buy_price: Decimal
    avg_buy_price_modified: bool
    unit_currency: constants.CurrencyCode


@dataclass(frozen=True)
class OrderConfig:
    fee: Decimal
    minimum: Decimal
    maximum: Decimal
    unit_price: Decimal
    currency: str


@dataclass(frozen=True)
class Market:
    ticker: str
    sell: OrderConfig
    buy: OrderConfig
    order_types: AbstractSet[constants.OrderType]
    order_sides: AbstractSet[constants.Side]


@dataclass(frozen=True)
class MarketWithAccount:
    market: Market
    bid_account: Account
    ask_account: Account


@dataclass(frozen=True)
class Order:
    order_uuid: UUID
    side: constants.Side
    order_type: constants.OrderType
    price: Decimal
    state: constants.OrderState
    ticker: str
    created_at: datetime.datetime
    volume: Decimal
    remaining_volume: Decimal
    reserved_fee: Decimal
    remaining_fee: Decimal
    paid_fee: Decimal
    locked: Decimal
    executed_volume: Decimal
    trade_count: int


@dataclass(frozen=True)
class OrderWithTrades(Order):
    @dataclass(frozen=True)
    class Trade:
        ticker: str
        trade_uuid: UUID
        price: Decimal
        volume: Decimal
        funds: Decimal
        side: constants.Side
        created_at: datetime.datetime

    trades: Sequence[Trade]
