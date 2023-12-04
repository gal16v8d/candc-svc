'''All db models definition'''
from typing import Optional
from sqlmodel import BigInteger, Column, Field
from sqlalchemy import UniqueConstraint
import app.models.schemas as schemas


# Init db entities
class Boat(schemas.BoatBase, table=True):
    '''Boat each faction can build'''
    __tablename__ = 'boat'

    boat_id: Optional[int] = Field(sa_column=Column(
        BigInteger, primary_key=True, autoincrement=True))


class BoatXFaction(schemas.BoatXFactionBase, table=True):
    '''
    Since boat can repeat for each faction,
    then adding intermediate table to avoid duplicates
    '''
    __tablename__ = 'boatxfaction'

    id: Optional[int] = Field(sa_column=Column(BigInteger, primary_key=True, autoincrement=True))

    __table_args__ = (
        UniqueConstraint('boat_id', 'faction_id', name = 'uq_boat_faction'),
    )


class Faction(schemas.FactionBase, table=True):
    '''Represents the specific faction'''
    __tablename__ = 'faction'

    faction_id: Optional[int] = Field(sa_column=Column(
        BigInteger, primary_key=True, autoincrement=True))

    __table_args__ = (
        UniqueConstraint('name', 'game_id', name = 'uq_name_game_id'),
    )


class Game(schemas.GameBase, table=True):
    '''If several games in db are registered allows to select one'''
    __tablename__ = 'game'

    game_id: Optional[int] = Field(sa_column=Column(
        BigInteger, primary_key=True, autoincrement=True))


class Infantry(schemas.InfantryBase, table=True):
    '''Infantry each faction can build'''
    __tablename__ = 'infantry'

    infantry_id: Optional[int] = Field(sa_column=Column(
        BigInteger, primary_key=True, autoincrement=True))


class InfantryXFaction(schemas.InfantryXFactionBase, table=True):
    '''
    Since infantry can repeat for each faction,
    then adding intermediate table to avoid duplicates
    '''
    __tablename__ = 'infantryxfaction'

    id: Optional[int] = Field(sa_column=Column(BigInteger, primary_key=True, autoincrement=True))

    __table_args__ = (
        UniqueConstraint('infantry_id', 'faction_id', name = 'uq_infantry_faction'),
    )


class Plane(schemas.PlaneBase, table=True):
    '''Plane each faction can build'''
    __tablename__ = 'plane'

    plane_id: Optional[int] = Field(sa_column=Column(
        BigInteger, primary_key=True, autoincrement=True))


class PlaneXFaction(schemas.PlaneXFactionBase, table=True):
    '''
    Since plane can repeat for each faction,
    then adding intermediate table to avoid duplicates
    '''
    __tablename__ = 'planexfaction'

    id: Optional[int] = Field(sa_column=Column(BigInteger, primary_key=True, autoincrement=True))

    __table_args__ = (
        UniqueConstraint('plane_id', 'faction_id', name = 'uq_plane_faction'),
    )


class Structure(schemas.StructureBase, table=True):
    '''Structures each faction can build'''
    __tablename__ = 'structure'

    structure_id: Optional[int] = Field(sa_column=Column(
        BigInteger, primary_key=True, autoincrement=True))


class StructureXFaction(schemas.StructureXFactionBase, table=True):
    '''
    Since some structures can repeat for each faction,
    then adding intermediate table to avoid duplicates
    '''
    __tablename__ = 'structurexfaction'

    id: Optional[int] = Field(sa_column=Column(BigInteger, primary_key=True, autoincrement=True))

    __table_args__ = (
        UniqueConstraint('structure_id', 'faction_id', name = 'uq_structure_faction'),
    )


class Tank(schemas.TankBase, table=True):
    '''Tank each faction can build'''
    __tablename__ = 'tank'

    tank_id: Optional[int] = Field(sa_column=Column(
        BigInteger, primary_key=True, autoincrement=True))


class TankXFaction(schemas.TankXFactionBase, table=True):
    '''
    Since tank can repeat for each faction,
    then adding intermediate table to avoid duplicates
    '''
    __tablename__ = 'tankxfaction'

    id: Optional[int] = Field(sa_column=Column(BigInteger, primary_key=True, autoincrement=True))

    __table_args__ = (
        UniqueConstraint('tank_id', 'faction_id', name = 'uq_tank_faction'),
    )
