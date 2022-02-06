from __future__ import annotations

import codecs

try:
    from functools import cache  # type: ignore[attr-defined]
except ImportError:
    from functools import lru_cache
    from typing import Callable, TypeVar

    from typing_extensions import ParamSpec

    _T = TypeVar('_T')
    _P = ParamSpec('_P')

    def cache(user_function: Callable[_P, _T]) -> Callable[_P, _T]:
        return lru_cache(maxsize=None)(user_function)


from typing import Optional

__all__ = ('get_codec',)


@cache  # type: ignore[misc]
def get_codec(enc: str) -> Optional[codecs.CodecInfo]:
    try:
        return codecs.lookup(enc)
    except LookupError:
        return None
