'''All db models definition'''
from typing import Dict
from sqlalchemy import Column, UniqueConstraint, inspect
from app.models.database import db


class BaseSqlModelMixin:
    '''Add util method for all the models'''
    def to_dict(self) -> Dict:
        '''Transform sql model to dict'''
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    def __repr__(self) -> str:
        return f'<{type(self).__name__} {self.name}>'


class LogicalDeletionMixin:
    '''This Mixin inherits logical attribute for entities'''
    active = Column(db.Boolean, default=True, nullable=False)


class NamedMixin:
    '''Append common name prop to all models'''
    name = Column(db.String(64), nullable=False, unique=True)


class DataCostMixin:
    '''
    Most of the objects in the game like Structures, Infantry, Tanks, etc
    are composed by name and cost, so this one will be used for these data types.
    '''
    base_cost = Column(db.Integer, nullable=False)
    notes = Column(db.String(256), nullable=True)
    is_stealth = Column(db.Boolean, default=False, nullable=False)
    build_limit = Column(db.Boolean, default=False, nullable=False)
    is_special = Column(db.Boolean, default=False, nullable=False)


class Game(db.Model, BaseSqlModelMixin, LogicalDeletionMixin, NamedMixin):
    '''If several games in db are registered allows to select one'''
    __tablename__ = 'game'

    game_id = Column(db.BigInteger, primary_key=True, autoincrement=True)


class Faction(db.Model, BaseSqlModelMixin, LogicalDeletionMixin, NamedMixin):
    '''Represents the specific faction'''
    __tablename__ = 'faction'

    faction_id = Column(db.BigInteger, primary_key=True, autoincrement=True)
    game_id = Column(db.BigInteger,
                     db.ForeignKey('game.game_id'),
                     nullable=False)
    notes = Column(db.String(512), nullable=True)

    __table_args__ = (
        UniqueConstraint('name', 'game_id', name = 'uq_name_game_id'),
    )


class Structure(db.Model, BaseSqlModelMixin, DataCostMixin, LogicalDeletionMixin, NamedMixin):
    '''Structures each faction can build'''
    __tablename__ = 'structure'

    structure_id = Column(db.BigInteger, primary_key=True, autoincrement=True)
    build_on_water = Column(db.Boolean, default=False, nullable=False)


class StructureXFaction(db.Model, BaseSqlModelMixin, LogicalDeletionMixin):
    '''
    Since some structures can repeat for each faction,
    then adding intermediate table to avoid duplicates
    '''
    __tablename__ = 'structurexfaction'

    id = Column(db.BigInteger, primary_key=True, autoincrement=True)
    structure_id = Column(db.BigInteger,
                          db.ForeignKey('structure.structure_id'),
                          nullable=False)
    faction_id = Column(db.BigInteger,
                        db.ForeignKey('faction.faction_id'),
                        nullable=True)
    custom_cost = Column(db.Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint('structure_id', 'faction_id', name = 'uq_structure_faction'),
    )


class Infantry(db.Model, BaseSqlModelMixin, DataCostMixin, LogicalDeletionMixin, NamedMixin):
    '''Infantry each faction can build'''
    __tablename__ = 'infantry'

    infantry_id = Column(db.BigInteger, primary_key=True, autoincrement=True)
    can_swim = Column(db.Boolean, default=False, nullable=False)
    can_fly = Column(db.Boolean, default=False, nullable=False)


class InfantryXFaction(db.Model, BaseSqlModelMixin, LogicalDeletionMixin):
    '''
    Since infantry can repeat for each faction,
    then adding intermediate table to avoid duplicates
    '''
    __tablename__ = 'infantryxfaction'

    id = Column(db.BigInteger, primary_key=True, autoincrement=True)
    infantry_id = Column(db.BigInteger,
                          db.ForeignKey('infantry.infantry_id'),
                          nullable=False)
    faction_id = Column(db.BigInteger,
                        db.ForeignKey('faction.faction_id'),
                        nullable=True)
    custom_cost = Column(db.Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint('infantry_id', 'faction_id', name = 'uq_infantry_faction'),
    )


class Tank(db.Model, BaseSqlModelMixin, DataCostMixin, LogicalDeletionMixin, NamedMixin):
    '''Tank each faction can build'''
    __tablename__ = 'tank'

    tank_id = Column(db.BigInteger, primary_key=True, autoincrement=True)
    can_swim = Column(db.Boolean, default=False, nullable=False)


class TankXFaction(db.Model, BaseSqlModelMixin, LogicalDeletionMixin):
    '''
    Since tank can repeat for each faction,
    then adding intermediate table to avoid duplicates
    '''
    __tablename__ = 'tankxfaction'

    id = Column(db.BigInteger, primary_key=True, autoincrement=True)
    tank_id = Column(db.BigInteger,
                     db.ForeignKey('tank.tank_id'),
                     nullable=False)
    faction_id = Column(db.BigInteger,
                        db.ForeignKey('faction.faction_id'),
                        nullable=True)
    custom_cost = Column(db.Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint('tank_id', 'faction_id', name = 'uq_tank_faction'),
    )


class Boat(db.Model, BaseSqlModelMixin, DataCostMixin, LogicalDeletionMixin, NamedMixin):
    '''Boat each faction can build'''
    __tablename__ = 'boat'

    boat_id = Column(db.BigInteger, primary_key=True, autoincrement=True)
    can_go_ground = Column(db.Boolean, default=False, nullable=False)


class BoatXFaction(db.Model, BaseSqlModelMixin, LogicalDeletionMixin):
    '''
    Since boat can repeat for each faction,
    then adding intermediate table to avoid duplicates
    '''
    __tablename__ = 'boatxfaction'

    id = Column(db.BigInteger, primary_key=True, autoincrement=True)
    boat_id = Column(db.BigInteger,
                     db.ForeignKey('boat.boat_id'),
                     nullable=False)
    faction_id = Column(db.BigInteger,
                        db.ForeignKey('faction.faction_id'),
                        nullable=True)
    custom_cost = Column(db.Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint('boat_id', 'faction_id', name = 'uq_boat_faction'),
    )


class Plane(db.Model, BaseSqlModelMixin, DataCostMixin, LogicalDeletionMixin, NamedMixin):
    '''Plane each faction can build'''
    __tablename__ = 'plane'

    plane_id = Column(db.BigInteger, primary_key=True, autoincrement=True)


class PlaneXFaction(db.Model, BaseSqlModelMixin, LogicalDeletionMixin):
    '''
    Since plane can repeat for each faction,
    then adding intermediate table to avoid duplicates
    '''
    __tablename__ = 'planexfaction'

    id = Column(db.BigInteger, primary_key=True, autoincrement=True)
    plane_id = Column(db.BigInteger,
                     db.ForeignKey('plane.plane_id'),
                     nullable=False)
    faction_id = Column(db.BigInteger,
                        db.ForeignKey('faction.faction_id'),
                        nullable=True)
    custom_cost = Column(db.Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint('plane_id', 'faction_id', name = 'uq_plane_faction'),
    )
