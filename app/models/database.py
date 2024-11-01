"""db and crud module"""

from typing import Any, Dict, Final, List, Optional, Type

from sqlmodel import SQLModel
from flask_sqlalchemy import SQLAlchemy

from app.error.custom_exc import BadArgException, UnpatchableFieldException


NON_UPDATABLE_FIELDS: Final[List[str]] = ["created_at", "updated_at"]
db = SQLAlchemy()


def get_all(model: Type[SQLModel]) -> List[Type[SQLModel]]:
    """Fetch all active data"""
    session = db.session()
    return session.query(model).filter_by(active=True).all()


def get_by_id(model: Type[SQLModel], data_id: int) -> Optional[Type[SQLModel]]:
    """Fetch data by id"""
    session = db.session()
    data = session.get(model, data_id)
    if data and hasattr(data, "active") and data.active is True:
        return data
    return None


def get_by_query_args(
    model: Type[SQLModel], data: Dict[str, str]
) -> List[Type[SQLModel]]:
    """Allow to search given certain args in data dict"""
    session = db.session()
    query = session.query(model)
    for key, value in data.items():
        if hasattr(model, key):
            query = query.filter(getattr(model, key) == value)
        else:
            raise BadArgException(
                f"Attribute '{key}' is not part of '{model.__tablename__}' info"
            )
    return query.all()


def save(model: Type[SQLModel], data: Dict[str, Any]) -> Type[SQLModel]:
    """Persist object in database"""
    session = db.session()
    obj = model(**data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def patch(model: Type[SQLModel], data: Dict[str, Any]) -> Type[SQLModel]:
    """Update object in database"""
    session = db.session()
    for key, value in data.items():
        if key in NON_UPDATABLE_FIELDS:
            raise UnpatchableFieldException(key)
        elif hasattr(model, key):
            setattr(model, key, value)
        else:
            raise BadArgException(
                f"Attribute '{key}' is not part of '{model.__tablename__}' info"
            )
    session.commit()
    session.refresh(model)
    return model


def delete(obj: Type[SQLModel]) -> None:
    """Remove object from database"""
    session = db.session()
    session.delete(obj)
    session.commit()
