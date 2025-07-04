"""Allows to check how to spend the money depending on model"""

from builtins import map
import logging
import random
from collections import Counter
from typing import Any

from sqlalchemy import select, join

from app.configs.log_cfg import LOG_NAME
from app.error.custom_exc import BadModelException
from app.models.database import db
from app.models.models import (
    Boat,
    BoatXFaction,
    Infantry,
    InfantryXFaction,
    Plane,
    PlaneXFaction,
    Structure,
    StructureXFaction,
    Tank,
    TankXFaction,
)
from app.models.schemas import MoneySpend, MoneySpendRequest
from app.service.cache_service import CacheService


log = logging.getLogger(LOG_NAME)
switch_model_dict: dict[str, Any] = {
    "boats": {
        "model_1": Boat,
        "model_2": BoatXFaction,
        "on_clause": Boat.boat_id == BoatXFaction.boat_id,
    },
    "infantry": {
        "model_1": Infantry,
        "model_2": InfantryXFaction,
        "on_clause": Infantry.infantry_id == InfantryXFaction.infantry_id,
    },
    "planes": {
        "model_1": Plane,
        "model_2": PlaneXFaction,
        "on_clause": Plane.plane_id == PlaneXFaction.plane_id,
    },
    "structures": {
        "model_1": Structure,
        "model_2": StructureXFaction,
        "on_clause": Structure.structure_id == StructureXFaction.structure_id,
    },
    "tanks": {
        "model_1": Tank,
        "model_2": TankXFaction,
        "on_clause": Tank.tank_id == TankXFaction.tank_id,
    },
}


class MoneySpendService:
    """
    Service to calculate units to build given army (faction_id) and money amount
    """

    def __init__(self) -> None:
        self.cache_service = CacheService()

    @staticmethod
    def retrieve_cost(data: Any) -> int:
        """
        Get the right money cost for a unit.
            Args:
                data (Any): One of the api objects that can be built.
            Returns:
                custom cost if exists, else base cost
        """
        return data.custom_cost if data.custom_cost is not None else data.base_cost

    @staticmethod
    def filter_by_build_limit(all_opt: list[Any], result_list: list[str]) -> list[Any]:
        """
        Attempt to exclude from options list any unit which has
        build limit restriction and has been selected.
        """
        return list(
            filter(
                lambda opt: opt.build_limit is False
                or (opt.build_limit is True and opt.name not in result_list),
                all_opt,
            )
        )

    def spend_money_by_type(
        self, model_type: str, money_request: MoneySpendRequest
    ) -> dict[str, Any]:
        """
        Spend money depending on faction, type and money to spend.
        """
        if model_type in switch_model_dict:
            data_options = self.fetch_cached_data_or_else(
                model_type, money_request.faction_id, switch_model_dict[model_type]
            )
            return self.spend_money(data_options, money_request.money)
        model_values = ", ".join(switch_model_dict.keys())
        raise BadModelException(f"Model should be one of: {model_values}")

    def fetch_cached_data_or_else(
        self, model_type: str, faction_id: int, data_dict: dict[str, Any]
    ) -> Any:
        """
        Find data by faction in cache else check in db
            Args:
                model_type (str): boats, infantry, planes, structures, tanks
                faction_id (int): army identifier
                data_dict (dict): contains fun to execute
            Returns:
                Any data found in cache or db
        """
        cache_key = f"{model_type}-money-{faction_id}"
        return self.cache_service.fetch_from_cache_or_else(
            cache_key,
            self.get_data_by_faction_db,
            faction_id=faction_id,
            data_dict=data_dict,
        )

    def spend_money(
        self, data_options: list[Any], money_to_spend: int
    ) -> dict[str, Any]:
        """
        Retrieves random plane units to build depending on cash.
        """
        result_list = []
        cost_list = list(map(MoneySpendService.retrieve_cost, data_options))
        if len(cost_list) > 0:
            lowest_cost: int = min(cost_list)
            while money_to_spend > 0 and money_to_spend >= lowest_cost:
                log.debug("Money to spend %s", money_to_spend)
                filtered_options = MoneySpendService.filter_by_build_limit(
                    data_options, result_list
                )
                filtered_options = list(
                    filter(
                        lambda data: MoneySpendService.retrieve_cost(data)
                        <= money_to_spend,
                        filtered_options,
                    )
                )
                selected_data = random.choice(filtered_options)
                result_list.append(selected_data.name)
                money_to_spend -= MoneySpendService.retrieve_cost(selected_data)
        result_dict = dict(Counter(result_list))
        return MoneySpend(units=result_dict, available_cash=money_to_spend).dict()

    # pylint: disable=C0121
    def get_data_by_faction_db(self, faction_id: int, data_dict: dict[str, Any]):
        """
        Fetch db to get all the boats available for the faction.
        """
        first_model = data_dict["model_1"]
        second_model = data_dict["model_2"]
        from_clause = join(first_model, second_model, data_dict["on_clause"], True)
        query_to_run = (
            select(
                first_model.name,
                first_model.base_cost,
                first_model.build_limit,
                second_model.custom_cost,
            )
            .select_from(from_clause)
            .where(
                first_model.active.is_(True),
                second_model.active.is_(True),
                second_model.faction_id == faction_id,
            )
        )
        return db.session.execute(query_to_run).fetchall()
