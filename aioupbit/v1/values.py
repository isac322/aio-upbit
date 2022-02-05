from __future__ import annotations

import datetime
from abc import ABCMeta
from dataclasses import dataclass
from decimal import Decimal
from enum import IntEnum
from typing import AbstractSet, Optional, Sequence
from uuid import UUID

from aioupbit.v1 import constants


@dataclass(frozen=True)
class Ticker:
    ticker: str
    korean_name: str
    english_name: str
    warning: constants.MarketWarning


@dataclass(frozen=True)
class BaseCandle(metaclass=ABCMeta):
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


@dataclass(frozen=True)
class DayCandle(BaseCandle):
    prev_closing_price: Decimal
    change_price: Decimal
    change_rate: Decimal
    converted_trade_price: Optional[Decimal]


@dataclass(frozen=True)
class WeekCandle(BaseCandle):
    first_day_of_period: datetime.date


@dataclass(frozen=True)
class MonthCandle(BaseCandle):
    first_day_of_period: datetime.date


@dataclass(frozen=True)
class Trade:
    ticker: str
    timestamp: datetime.datetime
    trade_price: Decimal
    trade_volume: Decimal
    prev_closing_price: Decimal
    change_price: Decimal
    side: constants.Side
    sequential_id: int


@dataclass(frozen=True)
class Tick:
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


@dataclass(frozen=True)
class Orderbook:
    @dataclass(frozen=True)
    class Unit:
        ask_price: Decimal
        bid_price: Decimal
        ask_size: Decimal
        bid_size: Decimal

    ticker: str
    timestamp: datetime.datetime
    total_ask_size: Decimal
    total_bid_size: Decimal
    orderbook_units: Sequence[Unit]


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
