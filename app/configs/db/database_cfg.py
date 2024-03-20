'''Configs to properly connect with the database'''
from sqlalchemy.pool import QueuePool


class DbConfig:
    '''Base SQLAlchemy props'''
    SQLALCHEMY_POOL_CLASS = QueuePool
    SQLALCHEMY_TIMEZONE = 'UTC'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
