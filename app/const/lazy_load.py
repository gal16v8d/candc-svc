"""Lazy load object data"""

from typing import Final


DB_MODULE: Final[str] = "app.configs.db"
DEV_DB_MODULE: Final[str] = DB_MODULE + ".dev_cfg"
PROD_DB_MODULE: Final[str] = DB_MODULE + ".prod_cfg"
TEST_DB_MODULE: Final[str] = DB_MODULE + ".test_cfg"

DEV_DB_CLASS: Final[str] = "DevConfig"
PROD_DB_CLASS: Final[str] = "ProdConfig"
TEST_DB_CLASS: Final[str] = "TestConfig"
