"""Caching service for app"""

from collections.abc import Callable
import logging
from typing import Any

from app.configs.log_cfg import LOG_NAME
from app.core.cache import app_cache


log = logging.getLogger(LOG_NAME)


class CacheService:
    """Allow to manage data in cache"""

    def __init__(self) -> None:
        self.cache = app_cache

    # pylint: disable=W0212
    def get_cache_keys(self) -> list[str]:
        """
        List all the keys present in cache
        """
        return list(self.cache.cache._cache.keys())

    def clear_cache_by_name(self, name: str) -> None:
        """
        Delete all the elements in cache which starts with name
        """
        all_keys = self.get_cache_keys()
        matched_keys = list(filter(lambda key: key.startswith(name), all_keys))
        for key in matched_keys:
            log.debug("About to remove %s key from cache", key)
            self.cache.delete(key)

    def clear_cache(self) -> None:
        """
        Clear all the elements in cache
        """
        self.cache.clear()

    def delete(self, cache_key: str) -> None:
        """
        Remove a single value from cache
        """
        self.cache.delete(cache_key)

    def fetch_from_cache_or_else(
        self, cache_key: str, fun: Callable[..., Any], **kwargs
    ) -> Any:
        """
        Check data from cache, if present it returns cached data.
        If not present then execute fun, and stores it result in cache,
        then returns that value.
            Args:
                cache_key (str): key to check cache.
                fun (Callable): Any callable fun to execute.
                **kwargs: Any additional data to send to fun.
            Returns:
                Any: cached data or fun result (after cache value)
        """
        cached_data = self.cache.get(cache_key)
        if cached_data:
            log.info("Returning data from cache for key: %s", cache_key)
            return cached_data
        log.info("No data found in cache for key: %s", cache_key)
        db_data = fun(**kwargs)
        log.info("About to set data in cache for key: %s", cache_key)
        self.cache.set(cache_key, db_data)
        return db_data
