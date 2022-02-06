from __future__ import annotations

from enum import Enum

from typing_extensions import Literal, TypeAlias

__all__ = ('MarketWarning', 'Side', 'Change', 'OrderType', 'OrderState', 'OrderBy', 'CurrencyCode', 'DaysAgo')


class MarketWarning(str, Enum):
    CAUTION = 'CAUTION'
    NONE = 'NONE'


class Side(str, Enum):
    ASK = 'ASK'
    BID = 'BID'


class Change(str, Enum):
    EVEN = 'EVEN'
    RISE = 'RISE'
    FALL = 'FALL'


class OrderType(str, Enum):
    LIMIT = 'limit'
    PRICE = 'price'
    MARKET = 'market'


class OrderState(str, Enum):
    WAIT = 'wait'
    WATCH = 'watch'
    DONE = 'done'
    CANCEL = 'cancel'


class OrderBy(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


CurrencyCode: TypeAlias = str
DaysAgo: TypeAlias = Literal[0, 1, 2, 3, 4, 5, 6, 7]
