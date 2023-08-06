import logging

from clinlog import Logger


class ClinlogHandler(logging.StreamHandler):
    def __init__(self, stream=None):
        super().__init__(stream)
        self._clinlog = Logger()

        self.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
        self.setLevel(logging.DEBUG)

    # TODO: Remove typing
    def emit(self, record: logging.LogRecord):
        try:
            msg = self._get_decorated_msg(self.format(record), record.levelno)

            stream = self.stream
            stream.write(msg + self.terminator)
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)

    def _get_decorated_msg(self, msg, log_level):
        if log_level == logging.CRITICAL:
            return self._clinlog._get_error_str(msg, highlight=True)
        elif log_level == logging.ERROR:
            return self._clinlog._get_error_str(msg)
        elif log_level == logging.WARNING:
            return self._clinlog._get_warning_str(msg)
        elif log_level == logging.INFO:
            return self._clinlog._get_info_str(msg) 

        return msg