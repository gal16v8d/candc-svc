'''Logger config'''
import logging


LOG_NAME = 'candc'
LOG_LEVEL = logging.INFO
log_file = f'{LOG_NAME}.log'


log = logging.getLogger(LOG_NAME)
log.setLevel(LOG_LEVEL)

# Create a file handler and set the log level
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(LOG_LEVEL)

# Create a formatter and set it for the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
log.addHandler(file_handler)
