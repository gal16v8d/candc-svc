'''Configs to properly connect with the database'''
from dotenv import dotenv_values, find_dotenv
from sqlalchemy.pool import QueuePool


class DbConfig:
    '''Base SQLAlchemy props'''
    SQLALCHEMY_POOL_CLASS = QueuePool
    SQLALCHEMY_TIMEZONE = 'UTC'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(DbConfig):
    '''Dev config inherits from DbConfig and use .env file'''
    env_file = find_dotenv('.env')
    config = dotenv_values(env_file)
    SQLALCHEMY_DATABASE_URI = config['CANDC_DB_URL']
    # close idle connections after POOL_RECYCLE seconds
    SQLALCHEMY_POOL_RECYCLE = config['POOL_RECYCLE']
    SQLALCHEMY_POOL_SIZE = config['POOL_SIZE']


class TestConfig(DbConfig):
    '''Test config inherits from DbConfig and use .env.test file'''
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    env_file = find_dotenv('.env.test')
    config = dotenv_values(env_file)
    SQLALCHEMY_DATABASE_URI = config['CANDC_DB_URL']
    SQLALCHEMY_POOL_RECYCLE = config['POOL_RECYCLE']
    SQLALCHEMY_POOL_SIZE = config['POOL_SIZE']
