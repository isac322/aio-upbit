from __future__ import annotations

from datetime import date, datetime, time, timezone
from decimal import Decimal

import pytest

try:
    from zoneinfo import ZoneInfo  # type: ignore[import]
except ImportError:
    from backports.zoneinfo import ZoneInfo  # type: ignore[import]

from aioupbit.v1.constants import Change, MarketWarning, Side
from aioupbit.v1.values import DayCandle, MinCandle, MonthCandle, Orderbook, Tick, Ticker, Trade, WeekCandle


class TestTicker:
    @pytest.mark.parametrize(
        ('json', 'expected'),
        (
            (
                dict(market='KRW-BTC', korean_name='비트코인', english_name='Bitcoin', market_warning='NONE'),
                Ticker(ticker='KRW-BTC', korean_name='비트코인', english_name='Bitcoin', warning=MarketWarning.NONE),
            ),
            (
                dict(market='BTC-GRT', korean_name='그래프', english_name='The Graph', market_warning='NONE'),
                Ticker(ticker='BTC-GRT', korean_name='그래프', english_name='The Graph', warning=MarketWarning.NONE),
            ),
        ),
    )
    def test_from_json(self, json, expected) -> None:
        assert expected == Ticker.from_json(json)


class TestMinCandle:
    @pytest.mark.parametrize(
        ('json', 'expected'),
        (
            (
                dict(
                    market='KRW-BTC',
                    candle_date_time_utc=datetime(2022, 2, 6, 9, 22, tzinfo=timezone.utc),
                    opening_price=Decimal('51031000.00000000'),
                    high_price=Decimal('51031000.00000000'),
                    low_price=Decimal('51016000.00000000'),
                    trade_price=Decimal('51016000.00000000'),
                    timestamp=1644139333892,
                    candle_acc_trade_price=Decimal('6425464.41727000'),
                    candle_acc_trade_volume=Decimal('0.12593089'),
                    unit=1,
                ),
                MinCandle(
                    ticker='KRW-BTC',
                    date_time=datetime(2022, 2, 6, 9, 22, tzinfo=timezone.utc),
                    opening_price=Decimal('51031000.00000000'),
                    high_price=Decimal('51031000.00000000'),
                    low_price=Decimal('51016000.00000000'),
                    trade_price=Decimal('51016000.00000000'),
                    latest_tick_timestamp=datetime(2022, 2, 6, 9, 22, 13, 892000, tzinfo=timezone.utc),
                    acc_trade_price=Decimal('6425464.41727000'),
                    acc_trade_volume=Decimal('0.12593089'),
                    unit=MinCandle.Unit.MIN1,
                ),
            ),
            (
                dict(
                    market='BTC-ETH',
                    candle_date_time_utc=datetime(2022, 2, 6, 9, 13, tzinfo=timezone.utc),
                    opening_price=Decimal('0.07214696'),
                    high_price=Decimal('0.07214696'),
                    low_price=Decimal('0.07214696'),
                    trade_price=Decimal('0.07214696'),
                    timestamp=1644138819463,
                    candle_acc_trade_price=Decimal('0.00065250'),
                    candle_acc_trade_volume=Decimal('0.00904404'),
                    unit=1,
                ),
                MinCandle(
                    ticker='BTC-ETH',
                    date_time=datetime(2022, 2, 6, 9, 13, tzinfo=timezone.utc),
                    opening_price=Decimal('0.07214696'),
                    high_price=Decimal('0.07214696'),
                    low_price=Decimal('0.07214696'),
                    trade_price=Decimal('0.07214696'),
                    latest_tick_timestamp=datetime(2022, 2, 6, 9, 13, 39, 463000, tzinfo=timezone.utc),
                    acc_trade_price=Decimal('0.00065250'),
                    acc_trade_volume=Decimal('0.00904404'),
                    unit=MinCandle.Unit.MIN1,
                ),
            ),
        ),
    )
    def test_from_json(self, json, expected) -> None:
        assert expected == MinCandle.from_json(json)


class TestDayCandle:
    @pytest.mark.parametrize(
        ('json', 'expected'),
        (
            (
                dict(
                    market='KRW-BTC',
                    candle_date_time_utc=datetime(2022, 2, 6, 0, 0, tzinfo=timezone.utc),
                    candle_date_time_kst=datetime(2022, 2, 6, 9, 0, tzinfo=timezone.utc),
                    opening_price=Decimal('50788000.00000000'),
                    high_price=Decimal('51210000.00000000'),
                    low_price=Decimal('50788000.00000000'),
                    trade_price=Decimal('51008000.00000000'),
                    timestamp=1644140329692,
                    candle_acc_trade_price=Decimal('73956981749.35733000'),
                    candle_acc_trade_volume=Decimal('1450.67115190'),
                    prev_closing_price=Decimal('50788000.00000000'),
                    change_price=Decimal('220000.00000000'),
                    change_rate=Decimal('0.0043317319'),
                ),
                DayCandle(
                    ticker='KRW-BTC',
                    date_time=datetime(2022, 2, 6, 0, 0, tzinfo=timezone.utc),
                    opening_price=Decimal('50788000.00000000'),
                    high_price=Decimal('51210000.00000000'),
                    low_price=Decimal('50788000.00000000'),
                    trade_price=Decimal('51008000.00000000'),
                    latest_tick_timestamp=datetime(2022, 2, 6, 9, 38, 49, 692000, tzinfo=timezone.utc),
                    acc_trade_price=Decimal('73956981749.35733000'),
                    acc_trade_volume=Decimal('1450.67115190'),
                    prev_closing_price=Decimal('50788000.00000000'),
                    change_price=Decimal('220000.00000000'),
                    change_rate=Decimal('0.0043317319'),
                    converted_trade_price=None,
                ),
            ),
            (
                dict(
                    market='BTC-ETC',
                    candle_date_time_utc=datetime(2022, 2, 6, 0, 0, tzinfo=timezone.utc),
                    candle_date_time_kst=datetime(2022, 2, 6, 9, 0, tzinfo=timezone.utc),
                    opening_price=Decimal('0.00070964'),
                    high_price=Decimal('0.00071469'),
                    low_price=Decimal('0.00070141'),
                    trade_price=Decimal('0.00071096'),
                    timestamp=1644137563018,
                    candle_acc_trade_price=Decimal('0.23636389'),
                    candle_acc_trade_volume=Decimal('335.04845034'),
                    prev_closing_price=Decimal('0.00070756'),
                    change_price=Decimal('0.00000340'),
                    change_rate=Decimal('0.0048052462'),
                ),
                DayCandle(
                    ticker='BTC-ETC',
                    date_time=datetime(2022, 2, 6, 0, 0, tzinfo=timezone.utc),
                    opening_price=Decimal('0.00070964'),
                    high_price=Decimal('0.00071469'),
                    low_price=Decimal('0.00070141'),
                    trade_price=Decimal('0.00071096'),
                    latest_tick_timestamp=datetime(2022, 2, 6, 8, 52, 43, 18000, tzinfo=timezone.utc),
                    acc_trade_price=Decimal('0.23636389'),
                    acc_trade_volume=Decimal('335.04845034'),
                    prev_closing_price=Decimal('0.00070756'),
                    change_price=Decimal('0.00000340'),
                    change_rate=Decimal('0.0048052462'),
                    converted_trade_price=None,
                ),
            ),
        ),
    )
    def test_from_json(self, json, expected) -> None:
        assert expected == DayCandle.from_json(json)


class TestWeekCandle:
    @pytest.mark.parametrize(
        ('json', 'expected'),
        (
            (
                dict(
                    market='BTC-ETC',
                    candle_date_time_utc=datetime(2022, 1, 24, 0, 0, tzinfo=timezone.utc),
                    candle_date_time_kst=datetime(2022, 1, 24, 9, 0, tzinfo=timezone.utc),
                    opening_price=Decimal('0.00068891'),
                    high_price=Decimal('0.00068910'),
                    low_price=Decimal('0.00061749'),
                    trade_price=Decimal('0.00066004'),
                    timestamp=1643586203235,
                    candle_acc_trade_price=Decimal('3.47277484'),
                    candle_acc_trade_volume=Decimal('5262.07358114'),
                    first_day_of_period=date(2022, 1, 24),
                ),
                WeekCandle(
                    ticker='BTC-ETC',
                    date_time=datetime(2022, 1, 24, 0, 0, tzinfo=timezone.utc),
                    opening_price=Decimal('0.00068891'),
                    high_price=Decimal('0.00068910'),
                    low_price=Decimal('0.00061749'),
                    trade_price=Decimal('0.00066004'),
                    latest_tick_timestamp=datetime(2022, 1, 30, 23, 43, 23, 235000, tzinfo=timezone.utc),
                    acc_trade_price=Decimal('3.47277484'),
                    acc_trade_volume=Decimal('5262.07358114'),
                    first_day_of_period=date(2022, 1, 24),
                ),
            ),
            (
                dict(
                    market='KRW-BTC',
                    candle_date_time_utc=datetime(2022, 1, 31, 0, 0, tzinfo=timezone.utc),
                    candle_date_time_kst=datetime(2022, 1, 31, 9, 0, tzinfo=timezone.utc),
                    opening_price=Decimal('47208000.00000000'),
                    high_price=Decimal('51488000.00000000'),
                    low_price=Decimal('44770000.00000000'),
                    trade_price=Decimal('50986000.00000000'),
                    timestamp=1644140812758,
                    candle_acc_trade_price=Decimal('1482350834631.18899000'),
                    candle_acc_trade_volume=Decimal('30992.13725501'),
                    first_day_of_period=date(2022, 1, 31),
                ),
                WeekCandle(
                    ticker='KRW-BTC',
                    date_time=datetime(2022, 1, 31, 0, 0, tzinfo=timezone.utc),
                    opening_price=Decimal('47208000.00000000'),
                    high_price=Decimal('51488000.00000000'),
                    low_price=Decimal('44770000.00000000'),
                    trade_price=Decimal('50986000.00000000'),
                    latest_tick_timestamp=datetime(2022, 2, 6, 9, 46, 52, 758000, tzinfo=timezone.utc),
                    acc_trade_price=Decimal('1482350834631.18899000'),
                    acc_trade_volume=Decimal('30992.13725501'),
                    first_day_of_period=date(2022, 1, 31),
                ),
            ),
        ),
    )
    def test_from_json(self, json, expected) -> None:
        assert expected == WeekCandle.from_json(json)


class TestMonthCandle:
    @pytest.mark.parametrize(
        ('json', 'expected'),
        (
            (
                dict(
                    market='BTC-ETC',
                    candle_date_time_utc=datetime(2022, 1, 24, 0, 0, tzinfo=timezone.utc),
                    candle_date_time_kst=datetime(2022, 1, 24, 9, 0, tzinfo=timezone.utc),
                    opening_price=Decimal('0.00068891'),
                    high_price=Decimal('0.00068910'),
                    low_price=Decimal('0.00061749'),
                    trade_price=Decimal('0.00066004'),
                    timestamp=1643586203235,
                    candle_acc_trade_price=Decimal('3.47277484'),
                    candle_acc_trade_volume=Decimal('5262.07358114'),
                    first_day_of_period=date(2022, 1, 24),
                ),
                MonthCandle(
                    ticker='BTC-ETC',
                    date_time=datetime(2022, 1, 24, 0, 0, tzinfo=timezone.utc),
                    opening_price=Decimal('0.00068891'),
                    high_price=Decimal('0.00068910'),
                    low_price=Decimal('0.00061749'),
                    trade_price=Decimal('0.00066004'),
                    latest_tick_timestamp=datetime(2022, 1, 30, 23, 43, 23, 235000, tzinfo=timezone.utc),
                    acc_trade_price=Decimal('3.47277484'),
                    acc_trade_volume=Decimal('5262.07358114'),
                    first_day_of_period=date(2022, 1, 24),
                ),
            ),
            (
                dict(
                    market='KRW-BTC',
                    candle_date_time_utc=datetime(2022, 1, 31, 0, 0, tzinfo=timezone.utc),
                    candle_date_time_kst=datetime(2022, 1, 31, 9, 0, tzinfo=timezone.utc),
                    opening_price=Decimal('47208000.00000000'),
                    high_price=Decimal('51488000.00000000'),
                    low_price=Decimal('44770000.00000000'),
                    trade_price=Decimal('50986000.00000000'),
                    timestamp=1644140812758,
                    candle_acc_trade_price=Decimal('1482350834631.18899000'),
                    candle_acc_trade_volume=Decimal('30992.13725501'),
                    first_day_of_period=date(2022, 1, 31),
                ),
                MonthCandle(
                    ticker='KRW-BTC',
                    date_time=datetime(2022, 1, 31, 0, 0, tzinfo=timezone.utc),
                    opening_price=Decimal('47208000.00000000'),
                    high_price=Decimal('51488000.00000000'),
                    low_price=Decimal('44770000.00000000'),
                    trade_price=Decimal('50986000.00000000'),
                    latest_tick_timestamp=datetime(2022, 2, 6, 9, 46, 52, 758000, tzinfo=timezone.utc),
                    acc_trade_price=Decimal('1482350834631.18899000'),
                    acc_trade_volume=Decimal('30992.13725501'),
                    first_day_of_period=date(2022, 1, 31),
                ),
            ),
        ),
    )
    def test_from_json(self, json, expected) -> None:
        assert expected == MonthCandle.from_json(json)


class TestTrade:
    @pytest.mark.parametrize(
        ('json', 'expected'),
        (
            (
                dict(
                    market='BTC-ETC',
                    trade_date_utc=date(2022, 2, 6),
                    trade_time_utc=time(8, 52, 42, tzinfo=timezone.utc),
                    timestamp=1644137562000,
                    trade_price=Decimal('0.00071096'),
                    trade_volume=Decimal('3.11909372'),
                    prev_closing_price=Decimal('0.00070756'),
                    change_price=Decimal('0.00000340'),
                    ask_bid='ASK',
                    sequential_id=16441375620000000,
                ),
                Trade(
                    ticker='BTC-ETC',
                    timestamp=datetime(2022, 2, 6, 8, 52, 42, tzinfo=timezone.utc),
                    trade_price=Decimal('0.00071096'),
                    trade_volume=Decimal('3.11909372'),
                    prev_closing_price=Decimal('0.00070756'),
                    change_price=Decimal('0.00000340'),
                    side=Side.ASK,
                    sequential_id=16441375620000000,
                ),
            ),
        ),
    )
    def test_from_json(self, json, expected) -> None:
        assert expected == Trade.from_json(json)


class TestTick:
    @pytest.mark.parametrize(
        ('json', 'expected'),
        (
            (
                dict(
                    market='BTC-ETC',
                    trade_date='20220206',
                    trade_time='085242',
                    trade_date_kst='20220206',
                    trade_time_kst='175242',
                    trade_timestamp=1644137562000,
                    opening_price=Decimal('0.00070964'),
                    high_price=Decimal('0.00071469'),
                    low_price=Decimal('0.00070141'),
                    trade_price=Decimal('0.00071096'),
                    prev_closing_price=Decimal('0.00070756'),
                    change='RISE',
                    change_price=Decimal('0.00000340'),
                    change_rate=Decimal('0.0048052462'),
                    signed_change_price=Decimal('0.00000340'),
                    signed_change_rate=Decimal('0.0048052462'),
                    trade_volume=Decimal('3.11909372'),
                    acc_trade_price=Decimal('0.2363638731829693'),
                    acc_trade_price_24h=Decimal('0.52252394'),
                    acc_trade_volume=Decimal('335.04845034'),
                    acc_trade_volume_24h=Decimal('737.38449855'),
                    highest_52_week_price=Decimal('0.00295594'),
                    highest_52_week_date=date(2021, 5, 6),
                    lowest_52_week_price=Decimal('0.00018202'),
                    lowest_52_week_date=date(2021, 2, 9),
                    timestamp=1644138600066,
                ),
                Tick(
                    ticker='BTC-ETC',
                    trade_date_time=datetime(2022, 2, 6, 17, 52, 42, tzinfo=ZoneInfo(key='Asia/Seoul')),
                    opening_price=Decimal('0.00070964'),
                    high_price=Decimal('0.00071469'),
                    low_price=Decimal('0.00070141'),
                    trade_price=Decimal('0.00071096'),
                    prev_closing_price=Decimal('0.00070756'),
                    change=Change.RISE,
                    change_price=Decimal('0.00000340'),
                    change_rate=Decimal('0.0048052462'),
                    signed_change_price=Decimal('0.00000340'),
                    signed_change_rate=Decimal('0.0048052462'),
                    trade_volume=Decimal('3.11909372'),
                    acc_trade_price=Decimal('0.2363638731829693'),
                    acc_trade_price_24h=Decimal('0.52252394'),
                    acc_trade_volume=Decimal('335.04845034'),
                    acc_trade_volume_24h=Decimal('737.38449855'),
                    highest_52_week_price=Decimal('0.00295594'),
                    highest_52_week_date=date(2021, 5, 6),
                    lowest_52_week_price=Decimal('0.00018202'),
                    lowest_52_week_date=date(2021, 2, 9),
                    timestamp=datetime(2022, 2, 6, 9, 10, 0, 66000, tzinfo=timezone.utc),
                ),
            ),
        ),
    )
    def test_from_json(self, json, expected) -> None:
        assert expected == Tick.from_json(json)


class TestOrderbook:
    @pytest.mark.parametrize(
        ('json', 'expected'),
        (
            (
                dict(
                    market='BTC-ETC',
                    timestamp=1644141846608,
                    total_ask_size=Decimal('478.06036493'),
                    total_bid_size=Decimal('865.04970377'),
                    orderbook_units=[
                        {
                            'ask_price': Decimal('0.00071889'),
                            'bid_price': Decimal('0.00071148'),
                            'ask_size': Decimal('33.45127908'),
                            'bid_size': Decimal('227.26683564'),
                        },
                        {
                            'ask_price': Decimal('0.00071971'),
                            'bid_price': Decimal('0.00071147'),
                            'ask_size': Decimal('48.58807316'),
                            'bid_size': Decimal('46.19031266'),
                        },
                        {
                            'ask_price': Decimal('0.00072496'),
                            'bid_price': Decimal('0.00071146'),
                            'ask_size': Decimal('107.635'),
                            'bid_size': Decimal('111.8351165'),
                        },
                        {
                            'ask_price': Decimal('0.00072497'),
                            'bid_price': Decimal('0.00071111'),
                            'ask_size': Decimal('1.0'),
                            'bid_size': Decimal('1.33439195'),
                        },
                        {
                            'ask_price': Decimal('0.00072501'),
                            'bid_price': Decimal('0.00070748'),
                            'ask_size': Decimal('7.92527829'),
                            'bid_size': Decimal('34.486'),
                        },
                        {
                            'ask_price': Decimal('0.00072991'),
                            'bid_price': Decimal('0.00070747'),
                            'ask_size': Decimal('23.85387225'),
                            'bid_size': Decimal('154.070137'),
                        },
                        {
                            'ask_price': Decimal('0.00073571'),
                            'bid_price': Decimal('0.00070464'),
                            'ask_size': Decimal('9.3283582'),
                            'bid_size': Decimal('0.83967983'),
                        },
                        {
                            'ask_price': Decimal('0.00073587'),
                            'bid_price': Decimal('0.00070212'),
                            'ask_size': Decimal('4.61469724'),
                            'bid_size': Decimal('1.0'),
                        },
                        {
                            'ask_price': Decimal('0.00073591'),
                            'bid_price': Decimal('0.00069919'),
                            'ask_size': Decimal('9.28217823'),
                            'bid_size': Decimal('1.0'),
                        },
                        {
                            'ask_price': Decimal('0.00073654'),
                            'bid_price': Decimal('0.0006965'),
                            'ask_size': Decimal('8.34028358'),
                            'bid_size': Decimal('86.14501076'),
                        },
                        {
                            'ask_price': Decimal('0.00074785'),
                            'bid_price': Decimal('0.00069498'),
                            'ask_size': Decimal('0.68'),
                            'bid_size': Decimal('1.0'),
                        },
                        {
                            'ask_price': Decimal('0.00075285'),
                            'bid_price': Decimal('0.00069045'),
                            'ask_size': Decimal('174.2812843'),
                            'bid_size': Decimal('27.72678129'),
                        },
                        {
                            'ask_price': Decimal('0.00075998'),
                            'bid_price': Decimal('0.00069027'),
                            'ask_size': Decimal('32.63849113'),
                            'bid_size': Decimal('72.18387217'),
                        },
                        {
                            'ask_price': Decimal('0.00076'),
                            'bid_price': Decimal('0.00068945'),
                            'ask_size': Decimal('14.47647597'),
                            'bid_size': Decimal('91.6395041'),
                        },
                        {
                            'ask_price': Decimal('0.00076001'),
                            'bid_price': Decimal('0.00068927'),
                            'ask_size': Decimal('1.9650935'),
                            'bid_size': Decimal('8.33206187'),
                        },
                    ],
                ),
                Orderbook(
                    ticker='BTC-ETC',
                    timestamp=datetime(2022, 2, 6, 19, 4, 6, 608000, tzinfo=ZoneInfo(key='Asia/Seoul')),
                    total_ask_size=Decimal('478.06036493'),
                    total_bid_size=Decimal('865.04970377'),
                    orderbook_units=(
                        Orderbook.Unit(
                            ask_price=Decimal('0.00071889'),
                            bid_price=Decimal('0.00071148'),
                            ask_size=Decimal('33.45127908'),
                            bid_size=Decimal('227.26683564'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00071971'),
                            bid_price=Decimal('0.00071147'),
                            ask_size=Decimal('48.58807316'),
                            bid_size=Decimal('46.19031266'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00072496'),
                            bid_price=Decimal('0.00071146'),
                            ask_size=Decimal('107.635'),
                            bid_size=Decimal('111.8351165'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00072497'),
                            bid_price=Decimal('0.00071111'),
                            ask_size=Decimal('1.0'),
                            bid_size=Decimal('1.33439195'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00072501'),
                            bid_price=Decimal('0.00070748'),
                            ask_size=Decimal('7.92527829'),
                            bid_size=Decimal('34.486'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00072991'),
                            bid_price=Decimal('0.00070747'),
                            ask_size=Decimal('23.85387225'),
                            bid_size=Decimal('154.070137'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00073571'),
                            bid_price=Decimal('0.00070464'),
                            ask_size=Decimal('9.3283582'),
                            bid_size=Decimal('0.83967983'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00073587'),
                            bid_price=Decimal('0.00070212'),
                            ask_size=Decimal('4.61469724'),
                            bid_size=Decimal('1.0'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00073591'),
                            bid_price=Decimal('0.00069919'),
                            ask_size=Decimal('9.28217823'),
                            bid_size=Decimal('1.0'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00073654'),
                            bid_price=Decimal('0.0006965'),
                            ask_size=Decimal('8.34028358'),
                            bid_size=Decimal('86.14501076'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00074785'),
                            bid_price=Decimal('0.00069498'),
                            ask_size=Decimal('0.68'),
                            bid_size=Decimal('1.0'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00075285'),
                            bid_price=Decimal('0.00069045'),
                            ask_size=Decimal('174.2812843'),
                            bid_size=Decimal('27.72678129'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00075998'),
                            bid_price=Decimal('0.00069027'),
                            ask_size=Decimal('32.63849113'),
                            bid_size=Decimal('72.18387217'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00076'),
                            bid_price=Decimal('0.00068945'),
                            ask_size=Decimal('14.47647597'),
                            bid_size=Decimal('91.6395041'),
                        ),
                        Orderbook.Unit(
                            ask_price=Decimal('0.00076001'),
                            bid_price=Decimal('0.00068927'),
                            ask_size=Decimal('1.9650935'),
                            bid_size=Decimal('8.33206187'),
                        ),
                    ),
                ),
            ),
        ),
    )
    def test_from_json(self, json, expected) -> None:
        assert expected == Orderbook.from_json(json)
