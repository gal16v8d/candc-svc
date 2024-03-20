'''Lazy load object data'''
DB_MODULE = 'app.configs.db'
DEV_DB_MODULE = DB_MODULE + '.dev_cfg'
PROD_DB_MODULE = DB_MODULE + '.prod_cfg'
TEST_DB_MODULE = DB_MODULE + '.test_cfg'

DEV_DB_CLASS = 'DevConfig'
PROD_DB_CLASS = 'ProdConfig'
TEST_DB_CLASS = 'TestConfig'
