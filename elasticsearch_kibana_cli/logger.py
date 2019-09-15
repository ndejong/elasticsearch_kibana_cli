
import os
import time
import logging

from . import NAME
from . import ElasticsearchKibanaCLIException


class ElasticsearchKibanaCLILogger:

    logger = None
    default_level = 'info'

    def __init__(self, level=None, level_env_override=None):

        if level_env_override is None:
            level_env_override = '{}_LOGLEVEL'.format(NAME.replace('_', '').replace(' ', '').upper())

        if os.getenv(level_env_override) is not None:
            log_level = os.getenv(level_env_override)
        elif level is not None:
            log_level = level
        else:
            log_level = self.default_level

        logger_init = logging.getLogger(NAME)
        if logger_init.level > 0:
            self.logger = logger_init
            return

        logger_init.setLevel(logging.DEBUG)

        log_level = log_level.upper()
        stream_handler = logging.StreamHandler()

        if log_level == 'CRITICAL':
            stream_handler.setLevel(logging.CRITICAL)
        elif log_level == 'ERROR':
            stream_handler.setLevel(logging.ERROR)
        elif log_level in ('WARNING', 'WARN'):
            stream_handler.setLevel(logging.WARNING)
        elif log_level == 'INFO':
            stream_handler.setLevel(logging.INFO)
        elif log_level == 'DEBUG':
            stream_handler.setLevel(logging.DEBUG)
        elif log_level is not None:
            raise ElasticsearchKibanaCLIException('unknown loglevel value', log_level)
        else:
            stream_handler.setLevel(logging.NOTSET)

        color_start = '\x1b[90m'  # grey
        color_end = '\x1b[0m'

        formatter = logging.Formatter(
            '{}%(asctime)s - %(levelname)s - %(message)s{}'.format(color_start, color_end),
            '%Y%m%dZ%H%M%S'
        )
        logging.Formatter.converter = time.gmtime

        stream_handler.setFormatter(formatter)
        logger_init.addHandler(stream_handler)

        self.logger = logger_init
