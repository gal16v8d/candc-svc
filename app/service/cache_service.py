'''Caching service for app'''
from typing import Any, Callable, List
from flask_caching import Cache


class CacheService:
    ''' Allow to manage data in cache'''

    def __init__(self, cache: Cache) -> None:
        self.cache = cache

    def get_cache_keys(self) -> List[str]:
        '''
        List all the keys present in cache
        '''
        return [key for key in self.cache.cache._cache.keys()]

    def clear_cache_by_name(self, name: str) -> None:
        '''
        Delete all the elements in cache which starts with name
        '''
        all_keys = self.get_cache_keys()
        matched_key = [key for key in all_keys if key.startswith(name)]
        for key in matched_key:
            self.cache.delete(key)

    def clear_cache(self) -> None:
        '''
        Clear all the elements in cache
        '''
        self.cache.clear()

    def delete(self, cache_key: str) -> None:
        '''
        Remove a single value from cache
        '''
        self.cache.delete(cache_key)

    def fetch_from_cache_or_else(self, cache_key: str, fun: Callable[..., Any], **kwargs) -> Any:
        '''
        Check data from cache, if present it returns cached data.
        If not present then execute fun, and stores it result in cache,
        then returns that value.
            Args:
                cache_key (str): key to check cache.
                fun (Callable): Any callable fun to execute.
                **kwargs: Any additional data to send to fun.
            Returns:
                Any: cached data or fun result (after cache value)
        '''
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        db_data = fun(**kwargs)
        self.cache.set(cache_key, db_data)
        return db_data
