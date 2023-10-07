'''db and crud module'''
from typing import Any, List
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def get_all(model) -> List[Any]:
    '''Fetch all active data'''
    session = db.session()
    return session.query(model).filter_by(active=True).all()


def get_by_id(model, id) -> Any:
    '''Fetch data by id'''
    session = db.session()
    data = session.query(model).get(id)
    if data and data.active is True:
        return data


def save(model, data) -> Any:
    '''Persist object in database'''
    session = db.session()
    obj = model(**data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def update(obj, data) -> Any:
    '''Update object in database'''
    session = db.session()
    for key, value in data.items():
        setattr(obj, key, value)
    session.commit()
    session.refresh(obj)
    return obj


def delete(obj) -> None:
    '''Remove object from database'''
    session = db.session()
    session.delete(obj)
    session.commit()
