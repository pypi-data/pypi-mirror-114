from .Logger import Logger

DEFAULT_LOGGER = None


def get_logger(log_level=None):
    """ Get custom clinlog instance with default configuration (Singleton).

    Args:
        log_level: Verbosity level

    Returns:
        clinlog.Logger
    """

    global DEFAULT_LOGGER

    if not DEFAULT_LOGGER:
        DEFAULT_LOGGER = create_logger(log_level)

    return DEFAULT_LOGGER


def create_logger(log_level=None):
    """ Create custom clinlog instance with default configuration.

    Args:
        log_level: Verbosity level

    Returns:
        clinlog.Logger
    """
    if not log_level:
        log_level = Logger.DEBUG

    logger = Logger(log_level)
    logger.error_tag = '[ERROR] '
    logger.warn_tag = '[WARN] '
    logger.confirm_tag = '[SUCCESS] '
    logger.info_tag = '[INFO] '
    logger.debug_tag = '[DEBUG] '

    return logger
