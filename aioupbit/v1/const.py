from __future__ import annotations

from enum import Enum, IntEnum


class MarketWarning(str, Enum):
    CAUTION = 'CAUTION'
    NONE = 'NONE'


class CandleUnit(IntEnum):
    MIN1 = 1
    MIN3 = 3
    MIN5 = 5
    MIN10 = 10
    MIN15 = 15
    MIN30 = 30
    MIN60 = 60
    MIN240 = 240


class Side(str, Enum):
    ASK = 'ASK'
    BID = 'BID'


class Change(str, Enum):
    EVEN = 'EVEN'
    RISE = 'RISE'
    FALL = 'FALL'
