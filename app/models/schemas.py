'''All schema definition'''
from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel
from sqlmodel import BigInteger, Column, DateTime, Field, SQLModel, String
from sqlalchemy import inspect


# Base models
class BaseSqlModelMixin(BaseModel):
    '''Add util method for all the models'''
    def to_dict(self) -> Dict:
        '''Transform sql model to dict'''
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self) -> str:
        return f'<{type(self).__name__} {self.name}>'


class CommonDataMixin(BaseModel):
    '''This Mixin inherits logical attribute for entities'''
    active: bool = Field(default=True, nullable=False)
    created_at: Optional[datetime] = Field(sa_column=Column(
        DateTime, default=datetime.utcnow, nullable=False))
    updated_at: Optional[datetime] = Field(sa_column=Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))


class NamedMixin(BaseModel):
    '''Append common name prop to all models'''
    name: str = Field(sa_column=Column(String(64), nullable=False, unique=True))


class DataCostMixin(BaseModel):
    '''
    Most of the objects in the game like Structures, Infantry, Tanks, etc
    are composed by name and cost, so this one will be used for these data types.
    '''
    base_cost: int = Field(nullable=False, ge=0)
    notes: Optional[str] = Field(sa_column=Column(String(256), nullable=True))
    is_stealth: bool = Field(default=False, nullable=False)
    build_limit: bool = Field(default=False, nullable=False)
    is_special: bool = Field(default=False, nullable=False)
    target_air_unit: bool = Field(default=False, nullable=False)


# Schema data
class BoatBase(SQLModel, BaseSqlModelMixin, DataCostMixin, CommonDataMixin, NamedMixin):
    '''Boat schema info'''
    can_go_ground: bool = Field(default=False, nullable=False)


class BoatXFactionBase(SQLModel, BaseSqlModelMixin, CommonDataMixin):
    '''BoatXFaction schema info'''
    boat_id: int = Field(foreign_key='boat.boat_id', nullable=False, sa_type=BigInteger)
    faction_id: int = Field(foreign_key='faction.faction_id', nullable=True, sa_type=BigInteger)
    custom_cost: int = Field(nullable=True)


class FactionBase(SQLModel, BaseSqlModelMixin, CommonDataMixin, NamedMixin):
    '''Faction schema info'''
    game_id: int = Field(foreign_key='game.game_id', nullable=False, sa_type=BigInteger)
    notes: str = Field(sa_column=Column(String(512), nullable=True))


class GameBase(SQLModel, BaseSqlModelMixin, CommonDataMixin, NamedMixin):
    '''Game schema info'''


class InfantryBase(SQLModel, BaseSqlModelMixin, DataCostMixin, CommonDataMixin, NamedMixin):
    '''Infantry schema info'''
    can_swim: bool = Field(default=False, nullable=False)
    can_fly: bool = Field(default=False, nullable=False)


class InfantryXFactionBase(SQLModel, BaseSqlModelMixin, CommonDataMixin):
    '''InfantryXFaction schema info'''
    infantry_id: int = Field(foreign_key='infantry.infantry_id', nullable=False, sa_type=BigInteger)
    faction_id: int = Field(foreign_key='faction.faction_id', nullable=True, sa_type=BigInteger)
    custom_cost: int = Field(nullable=True)


class PlaneBase(SQLModel, BaseSqlModelMixin, DataCostMixin, CommonDataMixin, NamedMixin):
    '''Plane schema info'''


class PlaneXFactionBase(SQLModel, BaseSqlModelMixin, CommonDataMixin):
    '''PlaneXFaction schema info'''
    plane_id: int = Field(foreign_key='plane.plane_id', nullable=False, sa_type=BigInteger)
    faction_id: int = Field(foreign_key='faction.faction_id', nullable=True, sa_type=BigInteger)
    custom_cost: int = Field(nullable=True)


class StructureBase(SQLModel, BaseSqlModelMixin, DataCostMixin,
                CommonDataMixin, NamedMixin):
    '''Structure schema info'''
    build_on_water: bool = Field(default=False, nullable=False)
    base_defense: bool = Field(default=False, nullable=False)


class StructureXFactionBase(SQLModel, BaseSqlModelMixin, CommonDataMixin):
    '''StructureXFaction schema info'''
    structure_id: int = Field(foreign_key='structure.structure_id',
                              nullable=False, sa_type=BigInteger)
    faction_id: int = Field(foreign_key='faction.faction_id', nullable=False, sa_type=BigInteger)
    custom_cost: int = Field(nullable=True)


class TankBase(SQLModel, BaseSqlModelMixin, DataCostMixin, CommonDataMixin, NamedMixin):
    '''Tank schema info'''
    can_swim: bool = Field(default=False, nullable=False)


class TankXFactionBase(SQLModel, BaseSqlModelMixin, CommonDataMixin):
    '''TankXFaction schema info'''
    tank_id: int = Field(foreign_key='tank.tank_id', nullable=False, sa_type=BigInteger)
    faction_id: int = Field(foreign_key='faction.faction_id', nullable=True, sa_type=BigInteger)
    custom_cost: int = Field(nullable=True)
