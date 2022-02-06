# aio-upbit

asyncio를 지원하는 [Upbit](https://upbit.com) Python 클라이언트.

## 예제

```python
import asyncio
from typing import Tuple

from aioupbit.v1 import RestClient, Ticker


async def main() -> None:
    markets: Tuple[Ticker, ...] = tuple(await RestClient.markets())
    ticks = await RestClient.latest_tick(markets)
    for tick in ticks:
        print(f'마켓: {tick.ticker}\n시간: {tick.trade_date_time}\n거래가: {tick.trade_price}')


if __name__ == '__main__':
    asyncio.run(main())
```

## 설치

`pip install aio-upbit`

## 구현 여부

하나씩 추가될 예정

### REST API

| API           | 상세  | ✅ / 🚧 |
|---------------|-----|:------:|
| QUOTATION API |     |   ✅    |
| EXCHANGE API  |     |   🚧   |

### WebSocket API

| API           | 상세  | ✅ / 🚧 |
|---------------|-----|:------:|
| QUOTATION API |     |   🚧   |
| EXCHANGE API  |     |   🚧   |

