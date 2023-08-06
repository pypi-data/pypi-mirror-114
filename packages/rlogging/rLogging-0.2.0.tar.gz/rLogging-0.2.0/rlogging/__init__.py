""" Модуль гибкого логирования """

from rlogging import handlers, loggers, printers, service, formaters
from rlogging.main import (get_logger, registration_logger, start_loggers,
                           stop_loggers)
from rlogging.service import celery_app

LOGGING_LEVELS = {
    0: 'RUBBISH',
    20: 'DEBUG',
    40: 'INFO',
    60: 'WARNING',
    80: 'ERROR',
    100: 'CRITICAL',
}

# alpha release
__version__ = '0.2.0'
