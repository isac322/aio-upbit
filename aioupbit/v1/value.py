from __future__ import annotations

import datetime
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Sequence

from aioupbit.v1 import const


@dataclass(frozen=True)
class Market:
    ticker: str
    korean_name: str
    english_name: str
    warning: Optional[const.MarketWarning]


@dataclass(frozen=True)
class Candle:
    ticker: str
    date_time: datetime.datetime
    opening_price: Decimal
    high_price: Decimal
    low_price: Decimal
    trade_price: Decimal
    timestamp: datetime.datetime
    acc_trade_price: Decimal
    acc_trade_volume: Decimal
    unit: const.CandleUnit


@dataclass(frozen=True)
class Tick:
    ticker: str
    trade_date_time: datetime.datetime
    opening_price: Decimal
    high_price: Decimal
    low_price: Decimal
    trade_price: Decimal
    prev_closing_price: Decimal
    change: const.Change
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
