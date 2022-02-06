# aio-upbit

[![PyPI](https://img.shields.io/pypi/v/aio-upbit?style=flat-square&logo=pypi)](https://pypi.org/project/aio-upbit/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aio-upbit?style=flat-square&logo=pypi)](https://pypi.org/project/aio-upbit/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/aio-upbit?style=flat-square&logo=pypi)](https://pypi.org/project/aio-upbit/)
[![PyPI - Status](https://img.shields.io/pypi/status/aio-upbit?style=flat-square)](https://pypi.org/project/aio-upbit/)
![Codecov](https://img.shields.io/codecov/c/gh/isac322/aio-upbit?style=flat-square&logo=codecov)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/isac322/aio-upbit/CI?style=flat-square&logo=github)
![License](https://img.shields.io/github/license/isac322/aio-upbit?style=flat-square&logo=github)
![GitHub last commit](https://img.shields.io/github/last-commit/isac322/aio-upbit?logo=github&style=flat-square)
![Dependabpt Status](https://flat.badgen.net/github/dependabot/isac322/aio-upbit?icon=github)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)


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

