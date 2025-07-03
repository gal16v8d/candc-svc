"""All schema definition"""

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, PositiveInt
from sqlmodel import BigInteger, Column, DateTime, Field, SQLModel, String


class CommonDataMixin(BaseModel):
    """This Mixin inherits logical attribute for entities"""

    active: bool = Field(default=True, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    # need to handle now onupdate manually per sa_column + pydantic 2.x bug
    updated_at: Optional[datetime] = Field(DateTime, nullable=True)


class NamedMixin(BaseModel):
    """Append common name prop to all models"""

    name: str = Field(nullable=False, unique=True, max_length=64)


class DataCostMixin(BaseModel):
    """
    Most of the objects in the game like Structures, Infantry, Tanks, etc
    are composed by name and cost, so this one will be used for these data types.
    """

    base_cost: int = Field(nullable=False, ge=0)
    notes: Optional[str] = Field(default=None , nullable=True, max_length=256)
    is_stealth: bool = Field(default=False, nullable=False)
    build_limit: bool = Field(default=False, nullable=False)
    is_special: bool = Field(default=False, nullable=False)
    target_air_unit: bool = Field(default=False, nullable=False)


# Schema data
class BoatBase(SQLModel, DataCostMixin, CommonDataMixin, NamedMixin):
    """Boat schema info"""

    boat_id: Optional[int] = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )
    can_go_ground: bool = Field(default=False, nullable=False)


class BoatXFactionBase(SQLModel, CommonDataMixin):
    """BoatXFaction schema info"""

    id: Optional[int] = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )
    boat_id: int = Field(foreign_key="boat.boat_id", nullable=False, sa_type=BigInteger)
    faction_id: Optional[int] = Field(
        foreign_key="faction.faction_id", nullable=True, sa_type=BigInteger
    )
    custom_cost: Optional[int] = Field(nullable=True)


class FactionBase(SQLModel, CommonDataMixin, NamedMixin):
    """Faction schema info"""

    faction_id: Optional[int] = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )
    game_id: int = Field(foreign_key="game.game_id", nullable=False, sa_type=BigInteger)
    notes: str = Field(sa_column=Column(String(512), nullable=True))


class GameBase(SQLModel, CommonDataMixin, NamedMixin):
    """Game schema info"""

    game_id: Optional[int] = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )


class InfantryBase(SQLModel, DataCostMixin, CommonDataMixin, NamedMixin):
    """Infantry schema info"""

    infantry_id: Optional[int] = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )
    can_swim: bool = Field(default=False, nullable=False)
    can_fly: bool = Field(default=False, nullable=False)


class InfantryXFactionBase(SQLModel, CommonDataMixin):
    """InfantryXFaction schema info"""

    id: Optional[int] = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )
    infantry_id: int = Field(
        foreign_key="infantry.infantry_id", nullable=False, sa_type=BigInteger
    )
    faction_id: Optional[int] = Field(
        foreign_key="faction.faction_id", nullable=True, sa_type=BigInteger
    )
    custom_cost: Optional[int] = Field(nullable=True)


class PlaneBase(SQLModel, DataCostMixin, CommonDataMixin, NamedMixin):
    """Plane schema info"""

    plane_id: Optional[int] = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )


class PlaneXFactionBase(SQLModel, CommonDataMixin):
    """PlaneXFaction schema info"""

    id: Optional[int] = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )
    plane_id: int = Field(
        foreign_key="plane.plane_id", nullable=False, sa_type=BigInteger
    )
    faction_id: Optional[int] = Field(
        foreign_key="faction.faction_id", nullable=True, sa_type=BigInteger
    )
    custom_cost: Optional[int] = Field(nullable=True)


class StructureBase(SQLModel, DataCostMixin, CommonDataMixin, NamedMixin):
    """Structure schema info"""

    structure_id: Optional[int] = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )
    build_on_water: bool = Field(default=False, nullable=False)
    base_defense: bool = Field(default=False, nullable=False)


class StructureXFactionBase(SQLModel, CommonDataMixin):
    """StructureXFaction schema info"""

    id: Optional[int] = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )
    structure_id: int = Field(
        foreign_key="structure.structure_id", nullable=False, sa_type=BigInteger
    )
    faction_id: int = Field(
        foreign_key="faction.faction_id", nullable=False, sa_type=BigInteger
    )
    custom_cost: Optional[int] = Field(nullable=True)


class TankBase(SQLModel, DataCostMixin, CommonDataMixin, NamedMixin):
    """Tank schema info"""

    tank_id: Optional[int] = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )
    can_swim: bool = Field(default=False, nullable=False)


class TankXFactionBase(SQLModel, CommonDataMixin):
    """TankXFaction schema info"""

    id: Optional[int] = Field(
        sa_column=Column(BigInteger, primary_key=True, autoincrement=True)
    )
    tank_id: int = Field(foreign_key="tank.tank_id", nullable=False, sa_type=BigInteger)
    faction_id: Optional[int] = Field(
        foreign_key="faction.faction_id", nullable=True, sa_type=BigInteger
    )
    custom_cost: Optional[int] = Field(nullable=True)


# Custom models
class MoneySpend(BaseModel):
    """Schema that expose how to spend the money"""

    available_cash: int
    units: dict[str, int]


# Requests
class MoneySpendRequest(BaseModel):
    """Schema for receive data for spend money"""

    faction_id: PositiveInt
    money: PositiveInt
