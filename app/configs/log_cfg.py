'''Logger config'''
import logging
import os
import app.const as consts


LOG_NAME = 'candc'
LOG_LEVEL = logging.INFO
log_file = f'{LOG_NAME}.log'


log = logging.getLogger(LOG_NAME)
log.setLevel(LOG_LEVEL)

# Create a formatter and set it for the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a console handler and set its level and formatter
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

# Create a file handler and set the log level
if os.getenv(consts.envs.CANDC_ENV) != 'prod':
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
