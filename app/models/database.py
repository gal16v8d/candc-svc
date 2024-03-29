'''db and crud module'''
from typing import Any, Dict, List
from flask_sqlalchemy import SQLAlchemy
from app.error.custom_exc import BadArgException, UnpatchableFieldException


NON_UPDATABLE_FIELDS = ['created_at', 'updated_at']
db = SQLAlchemy()


def get_all(model: Any) -> List[Any]:
    '''Fetch all active data'''
    session = db.session()
    return session.query(model).filter_by(active=True).all()


def get_by_id(model: Any, data_id: Any) -> Any:
    '''Fetch data by id'''
    session = db.session()
    data = session.query(model).get(data_id)
    if data and data.active is True:
        return data


def get_by_query_args(model: Any, data: Dict) -> Any:
    '''Allow to search given certain args in data dict'''
    session = db.session()
    query = session.query(model)
    for key, value in data.items():
        if hasattr(model, key):
            query = query.filter(getattr(model, key) == value)
        else:
            raise BadArgException(f"Attribute '{key}' is not part of '{model.__tablename__}' info")
    return query.all()


def save(model: Any, data: Any) -> Any:
    '''Persist object in database'''
    session = db.session()
    obj = model(**data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def patch(model: Any, data: Dict) -> Any:
    '''Update object in database'''
    session = db.session()
    for key, value in data.items():
        if hasattr(model, key) and key not in NON_UPDATABLE_FIELDS:
            setattr(model, key, value)
        elif key in NON_UPDATABLE_FIELDS:
            raise UnpatchableFieldException(key)
        else:
            raise BadArgException(f"Attribute '{key}' is not part of '{model.__tablename__}' info")
    session.commit()
    session.refresh(model)
    return model


def delete(obj: Any) -> None:
    '''Remove object from database'''
    session = db.session()
    session.delete(obj)
    session.commit()
