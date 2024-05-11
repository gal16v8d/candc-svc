"""Lazy load object data"""

from typing import Final


DB_MODULE: Final = "app.configs.db"
DEV_DB_MODULE: Final = DB_MODULE + ".dev_cfg"
PROD_DB_MODULE: Final = DB_MODULE + ".prod_cfg"
TEST_DB_MODULE: Final = DB_MODULE + ".test_cfg"

DEV_DB_CLASS: Final = "DevConfig"
PROD_DB_CLASS: Final = "ProdConfig"
TEST_DB_CLASS: Final = "TestConfig"
