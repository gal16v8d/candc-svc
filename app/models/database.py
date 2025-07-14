"""db and crud module"""

from datetime import datetime, timezone
from typing import Any, Final

from sqlmodel import SQLModel
from flask_sqlalchemy import SQLAlchemy

from app.error.custom_exc import BadArgException, UnpatchableFieldException


NON_UPDATABLE_FIELDS: Final[list[str]] = ["created_at", "updated_at"]
db = SQLAlchemy()


def get_all(model: type[SQLModel]) -> list[type[SQLModel]]:
    """Fetch all active data"""
    session = db.session()
    return session.query(model).filter_by(active=True).all()


def get_by_id(model: type[SQLModel], data_id: int) -> type[SQLModel] | None:
    """Fetch data by id"""
    session = db.session()
    data = session.get(model, data_id)
    if data and hasattr(data, "active") and data.active is True:
        return data
    return None


def get_by_query_args(
    model: type[SQLModel], data: dict[str, str]
) -> list[type[SQLModel]]:
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


def save(model: type[SQLModel], data: dict[str, Any]) -> type[SQLModel]:
    """Persist object in database"""
    session = db.session()
    obj = model(**data)
    if hasattr(obj, "created_at") and obj.created_at is None:
        obj.created_at = datetime.now(timezone.utc)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def patch(model: type[SQLModel], data: dict[str, Any]) -> type[SQLModel]:
    """Update object in database"""
    session = db.session()
    update_performed = False
    for key, value in data.items():
        if key in NON_UPDATABLE_FIELDS:
            raise UnpatchableFieldException(key)
        if hasattr(model, key):
            setattr(model, key, value)
            update_performed = True
        else:
            raise BadArgException(
                f"Attribute '{key}' is not part of '{model.__tablename__}' info"
            )
    if update_performed and hasattr(model, "updated_at"):
        model.updated_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(model)
    return model


def delete(obj: type[SQLModel]) -> None:
    """Remove object from database"""
    session = db.session()
    session.delete(obj)
    session.commit()
