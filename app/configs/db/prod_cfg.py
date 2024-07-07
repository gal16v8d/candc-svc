"""Prod configuration class to connect to db"""

import os

from app.configs.db.database_cfg import DbConfig
import app.const as consts


class ProdConfig(DbConfig):
    """Prod config inherits from DbConfig and use environment variables"""

    SQLALCHEMY_DATABASE_URI = os.getenv(consts.envs.CANDC_DB_URL)
    # close idle connections after POOL_RECYCLE seconds
    SQLALCHEMY_POOL_RECYCLE = os.getenv(consts.envs.POOL_RECYCLE)
    SQLALCHEMY_POOL_SIZE = os.getenv(consts.envs.POOL_SIZE)
