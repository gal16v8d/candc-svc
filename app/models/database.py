'''db and crud module'''
from typing import Any, Dict, List
from flask_sqlalchemy import SQLAlchemy
from app.error.custom_exc import BadArgException


db = SQLAlchemy()


def get_all(model) -> List[Any]:
    '''Fetch all active data'''
    session = db.session()
    return session.query(model).filter_by(active=True).all()


def get_by_id(model, data_id: Any) -> Any:
    '''Fetch data by id'''
    session = db.session()
    data = session.query(model).get(data_id)
    if data and data.active is True:
        return data


def get_by_query_args(model, data: Dict) -> Any:
    '''Allow to search given certain args in data dict'''
    session = db.session()
    query = session.query(model)
    for key, value in data.items():
        if hasattr(model, key):
            query = query.filter(getattr(model, key) == value)
        else:
            raise BadArgException(f"Attribute '{key}' is not part of '{model.__tablename__}' info")
    return query.all()


def save(model, data) -> Any:
    '''Persist object in database'''
    session = db.session()
    obj = model(**data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def patch(model, data: Dict) -> Any:
    '''Update object in database'''
    session = db.session()
    for key, value in data.items():
        if hasattr(model, key):
            setattr(model, key, value)
        else:
            raise BadArgException(f"Attribute '{key}' is not part of '{model.__tablename__}' info")
    session.commit()
    session.refresh(model)
    return model


def delete(obj) -> None:
    '''Remove object from database'''
    session = db.session()
    session.delete(obj)
    session.commit()
