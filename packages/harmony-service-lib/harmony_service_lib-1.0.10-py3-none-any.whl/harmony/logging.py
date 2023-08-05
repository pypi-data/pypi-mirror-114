import datetime as dt
from functools import lru_cache
import logging
import sys

from pythonjsonlogger import jsonlogger


class HarmonyJsonFormatter(jsonlogger.JsonFormatter):
    """A JSON log entry formatter."""
    def add_fields(self, log_record, record, message_dict):
        super(HarmonyJsonFormatter, self).add_fields(
            log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
        if not log_record.get('application'):
            log_record['application'] = self.app_name


@lru_cache(maxsize=128)
def build_logger(config, name=None):
    """
    Builds a logger with appropriate defaults for Harmony
    Parameters
    ----------
    config : harmony.util.Config
        The configuration values for this runtime environment.
    name : string
        The name of the logger

    Returns
    -------
    logger : Logging
        A logger for service output
    """
    logger = logging.getLogger()
    syslog = logging.StreamHandler()
    if config.text_logger:
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s.%(funcName)s:%(lineno)d] %(message)s")
    else:
        formatter = HarmonyJsonFormatter()
        formatter.app_name = config.app_name
    syslog.setFormatter(formatter)
    logger.addHandler(syslog)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


def setup_stdout_log_formatting(config):
    """
    Updates sys.stdout and sys.stderr to pass messages through the Harmony log formatter.
    """
    # See https://stackoverflow.com/questions/11124093/redirect-python-print-output-to-logger/11124247
    class StreamToLogger(object):
        def __init__(self, logger, log_level=logging.INFO):
            self.logger = logger
            self.log_level = log_level
            self.linebuf = ''

        def write(self, buf):
            temp_linebuf = self.linebuf + buf
            self.linebuf = ''
            for line in temp_linebuf.splitlines(True):
                if line[-1] == '\n':
                    self.logger.log(self.log_level, line.rstrip())
                else:
                    self.linebuf += line

        def flush(self):
            if self.linebuf != '':
                self.logger.log(self.log_level, self.linebuf.rstrip())
            self.linebuf = ''
    sys.stdout = StreamToLogger(build_logger(config), logging.INFO)
    sys.stderr = StreamToLogger(build_logger(config), logging.ERROR)
