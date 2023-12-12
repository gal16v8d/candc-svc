'''Test Service layer for cache service'''
from unittest import TestCase
from unittest.mock import Mock, patch
from typing import NamedTuple, Optional
from app.error.custom_exc import BadModelException
from app.models.models import Boat, BoatXFaction
from app.service.money_spend_service import MoneySpendService


class DbResultRow(NamedTuple):
    '''Emulates a row result from db'''
    name: str
    base_cost: int
    build_limit: bool
    custom_cost: Optional[int]


class TestMoneySpendService(TestCase):
    '''Test class for MoneySpendService'''
    TANYA_ROW = DbResultRow(name='Tanya', base_cost=1500,
                            custom_cost=None, build_limit=True)
    BLACK_EAGLE_ROW = DbResultRow(name='Black Eagle', base_cost=1200,
                              custom_cost=None, build_limit=False)

    def setUp(self) -> None:
        self._cache_service_patch = patch('app.service.money_spend_service.CacheService')
        self._db_execute_patch = patch('app.service.money_spend_service.db.session.execute')
        self._cache_service_mock = self._cache_service_patch.start()
        self._db_execute_mock = self._db_execute_patch.start()
        self.money_spend_service = MoneySpendService()

    def tearDown(self) -> None:
        self._cache_service_patch.stop()
        self._db_execute_patch.stop()

    def test_retrieve_cost_custom(self) -> None:
        '''Test retrieve_cost when custom cost exists'''
        data_with_custom = DbResultRow(name='Harrier', base_cost=1200,
                                       custom_cost=960, build_limit=False)
        result_custom = MoneySpendService.retrieve_cost(data_with_custom)
        self.assertEqual(960, result_custom)

    def test_retrieve_cost_no_custom(self) -> None:
        '''Test retrieve_cost when custom cost not exists'''
        result = MoneySpendService.retrieve_cost(self.BLACK_EAGLE_ROW)
        self.assertEqual(1200, result)

    def test_filter_by_build_limit_false(self) -> None:
        '''Test filter_by_build_limit when build_limit is false'''
        all_opt = [self.BLACK_EAGLE_ROW]
        result = MoneySpendService.filter_by_build_limit(all_opt, [])
        result_2 = MoneySpendService.filter_by_build_limit(all_opt, ['Black Eagle'])
        self.assertEqual(1, len(result))
        self.assertEqual(1, len(result_2))

    def test_filter_by_build_limit_true(self) -> None:
        '''Test filter_by_build_limit when build_limit is true'''
        all_opt = [self.TANYA_ROW]
        result = MoneySpendService.filter_by_build_limit(all_opt, [])
        result_2 = MoneySpendService.filter_by_build_limit(all_opt, ['Tanya'])
        self.assertEqual(1, len(result))
        self.assertEqual(0, len(result_2))

    def test_spend_money_by_type_unsupported(self) -> None:
        '''Test spend_money_by_type invalid type'''
        with self.assertRaises(BadModelException) as ctx:
            self.money_spend_service.spend_money_by_type('error', 1, 20000)
        self.assertEqual('Model should be one of: ' +
                         'boats, infantry, planes, structures, tanks', str(ctx.exception))

    @patch('app.service.money_spend_service.MoneySpendService.fetch_cached_data_or_else')
    @patch('app.service.money_spend_service.MoneySpendService.spend_money')
    def test_spend_money_by_type(self, mock_spend_money: Mock, mock_fetch_data: Mock) -> None:
        '''Test spend_money_by_type valid type'''
        mock_fetch_data.return_value = [self.TANYA_ROW]
        mock_spend_money.return_value = {
            'available_cash': 300,
            'units': {
                'Aegis Cruiser': 3,
                'Aircraft Carrier': 1,
                'Amphibious Transport': 3,
                'Destroyer': 3,
                'Dolphin': 3,
                'Heavy Cruiser': 3
            }
        }
        result = self.money_spend_service.spend_money_by_type('boats', 1, 20000)
        self.assertEqual(300, result['available_cash'])
        self.assertEqual(6, len(result['units'].keys()))
        mock_fetch_data.assert_called_once()
        mock_spend_money.assert_called_once()

    @patch('app.service.money_spend_service.MoneySpendService.get_data_by_faction_db')
    def test_fetch_cached_data_or_else(self, mock_get_data_by_faction_db: Mock) -> None:
        '''Test for fetch_cached_data_or_else'''
        data = [self.TANYA_ROW]
        cache_service = self._cache_service_mock.return_value
        cache_service.fetch_from_cache_or_else.return_value = data
        result = self.money_spend_service.fetch_cached_data_or_else('boats', 1, {})
        self.assertEqual(1, len(result))
        self.assertEqual('Tanya', result[0].name)
        cache_service.fetch_from_cache_or_else.assert_called_once()
        mock_get_data_by_faction_db.assert_not_called()

    def test_spend_money(self) -> None:
        '''Test for spend_money'''
        result = self.money_spend_service.spend_money([self.BLACK_EAGLE_ROW, self.TANYA_ROW], 5000)
        self.assertTrue('units' in result)

    def test_get_data_by_faction_db(self) -> None:
        '''Test for get_data_by_faction_db'''
        data_result = [{'name': 'Tanya', 'base_cost': 1500, 'build_limit': True}]
        self._db_execute_mock.return_value.fetchall.return_value = data_result
        data_dict = {
            'model_1': Boat,
            'model_2': BoatXFaction,
            'on_clause': Boat.boat_id == BoatXFaction.boat_id}
        result = self.money_spend_service.get_data_by_faction_db(1, data_dict)
        self.assertEqual(data_result, result)
