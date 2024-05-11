"""Test configuration class to connect to db"""

from dotenv import dotenv_values, find_dotenv
from app.configs.db.database_cfg import DbConfig
import app.const as consts


class TestConfig(DbConfig):
    """Test config inherits from DbConfig and use .env.test file"""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    env_file = find_dotenv(".env.test")
    config = dotenv_values(env_file)
    SQLALCHEMY_DATABASE_URI = config[consts.envs.CANDC_DB_URL]
    SQLALCHEMY_POOL_RECYCLE = config[consts.envs.POOL_RECYCLE]
    SQLALCHEMY_POOL_SIZE = config[consts.envs.POOL_SIZE]
