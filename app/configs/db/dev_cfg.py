'''Dev configuration class to connect to db'''
from dotenv import dotenv_values, find_dotenv
from app.configs.db.database_cfg import DbConfig
import app.const as consts


class DevConfig(DbConfig):
    '''Dev config inherits from DbConfig and use .env file'''
    env_file = find_dotenv('.env')
    config = dotenv_values(env_file)
    SQLALCHEMY_DATABASE_URI = config[consts.envs.CANDC_DB_URL]
    # close idle connections after POOL_RECYCLE seconds
    SQLALCHEMY_POOL_RECYCLE = config[consts.envs.POOL_RECYCLE]
    SQLALCHEMY_POOL_SIZE = config[consts.envs.POOL_SIZE]
