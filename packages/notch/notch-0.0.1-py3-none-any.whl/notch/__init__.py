import logging
import os
import sys


def make_log(log_name: str) -> logging.Logger:
    _log = logging.getLogger(log_name)

    log_format = os.getenv('LOG_FORMAT', '%(levelname)s [%(name)s] %(message)s')
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    logging.basicConfig(format=log_format, level=logging.DEBUG, stream=sys.stdout)
    _log.debug(f'Initializing logger for {log_name}')

    if not log_level == 'DEBUG':
        _log.debug(f'Changing log level to {log_level}')
    logging.getLogger().setLevel(log_level)

    for log_spec in os.getenv('OTHER_LOG_LEVELS', '').split():
        for logger, level in log_spec.split(':', maxsplit=1):
            _log.debug(f'Changing log level for {logger} to {level}')
            logging.getLogger(logger).setLevel(level)

    return _log
