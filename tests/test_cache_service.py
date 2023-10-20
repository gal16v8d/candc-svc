'''Test Service layer for cache service'''
from unittest import TestCase
from unittest.mock import Mock, patch
from typing import Any, Dict, List
from app.service.cache_service import CacheService


class TestCacheService(TestCase):
    ''' Test cases for cache service class'''

    def setUp(self) -> None:
        self._boats = 'boats'
        self._cache_patch = patch('app.service.cache_service.cache')
        self._cache_mock = self._cache_patch.start()
        self.cache_service = CacheService()

    def tearDown(self) -> None:
        self._cache_patch.stop()

    @staticmethod
    def mock_fun(faction_id: int) -> List[Dict[str, Any]]:
        '''Mock fun to generate an expected boat body'''
        return [{'boat_id': faction_id}]

    # pylint: disable=W0212
    def test_get_cache_keys(self) -> None:
        '''test case for get_cache_keys'''
        mock_dict = {self._boats: [], f'{self._boats}-1': {}}
        self._cache_mock.cache._cache.keys.return_value = mock_dict.keys()
        keys = self.cache_service.get_cache_keys()
        self.assertEqual([self._boats, f'{self._boats}-1'], keys)

    @patch('app.service.cache_service.CacheService.get_cache_keys')
    def test_clear_cache_by_name(self, mock_get_cache_keys: Mock) -> None:
        '''Test case for clear_cache_by_name'''
        mock_get_cache_keys.return_value = [self._boats, f'{self._boats}-1']
        self.cache_service.clear_cache_by_name(self._boats)
        self.assertEqual(2, self._cache_mock.delete.call_count)

    def test_clear_cache(self) -> None:
        '''Test case for clear_cache'''
        self.cache_service.clear_cache()
        self._cache_mock.clear.assert_called_once()

    def test_delete(self) -> None:
        '''Test case for delete'''
        self.cache_service.delete(self._boats)
        self._cache_mock.delete.assert_called_once_with(self._boats)

    def test_fetch_from_cache_or_else_is_present(self) -> None:
        '''Test case for fetch_from_cache_or_else when present in cache'''
        self._cache_mock.get.return_value = [{'boat_id': 1}]
        result = self.cache_service.fetch_from_cache_or_else(self._boats,
                                                             TestCacheService.mock_fun,
                                                             faction_id=1)
        self.assertEqual([{'boat_id': 1}], result)
        self._cache_mock.get.assert_called_once_with(self._boats)
        self._cache_mock.set.assert_not_called()

    def test_fetch_from_cache_or_else_is_empty(self) -> None:
        '''Test case for fetch_from_cache_or_else when present in cache'''
        self._cache_mock.get.return_value = None
        result = self.cache_service.fetch_from_cache_or_else(self._boats,
                                                             TestCacheService.mock_fun,
                                                             faction_id=1)
        self.assertEqual([{'boat_id': 1}], result)
        self._cache_mock.get.assert_called_once_with(self._boats)
        self._cache_mock.set.assert_called_once()
