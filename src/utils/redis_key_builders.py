from fastapi import Response, Request
from typing import Any, Callable, Dict, Optional, Tuple
import hashlib

from sqlalchemy.ext.asyncio import AsyncSession

from config import settings


def users_list_key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    exclude_types = (AsyncSession,)
    cache_kw = {}
    for name, value in kwargs.items():
        if isinstance(value, exclude_types):
            continue
        cache_kw[name] = value
    cache_key = hashlib.md5(  # noqa: S324
        f"{func.__module__}:{func.__name__}:{args}:{cache_kw}".encode()
    ).hexdigest()
    return f"{namespace}:{cache_key}"


def make_redis_key(*parts: str) -> str:
    safe_parts = []
    for p in parts:
        if p is None:
            continue
        p = str(p).strip()
        if not p:
            continue
        safe_parts.append(p.replace(":", "_"))
    return ":".join(safe_parts)


def get_redis_key(key: str) -> str:
    return make_redis_key(
        settings.redis_keys.prefix,
        settings.redis_keys.namespace.example_key,
        key,
    )
