import logging

from .clinlog_handler import ClinlogHandler


LOGGER_NAME = 'clinlog'

def get_logger(log_level=None):
    create_logger(log_level)

    return logging.getLogger(LOGGER_NAME)


def create_logger(log_level=None):
    if not log_level:
        log_level = logging.DEBUG

    logger = logging.getLogger(LOGGER_NAME)

    if _has_handler(logger):
        return

    cl_handler = ClinlogHandler()

    logger.setLevel(log_level)
    logger.addHandler(cl_handler)


def _has_handler(logger):
    for handler in logger.handlers:
        if isinstance(handler, ClinlogHandler):
            return True

    return False
