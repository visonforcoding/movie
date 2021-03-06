import logging
from logging.config import dictConfig
import os
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'logs')
logging_config = dict(
    version=1,
    formatters={
        'f': {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': logging.DEBUG
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'f',
            'level': logging.INFO,
            'filename':log_dir+'/log.log' 
        }
    },
    loggers={
        'root': {
            'handlers': ['console'],
            'level': logging.DEBUG
        },
        'root.file': {
            'handlers': ['file'],
            'level': logging.DEBUG
        }
    }
)

dictConfig(logging_config)
