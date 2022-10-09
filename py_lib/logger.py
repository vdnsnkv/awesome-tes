import logging
import traceback
from typing import Union

from pythonjsonlogger import jsonlogger

FORMAT_STR = "%(levelname)s%(asctime)s%(name)%(module)%(funcName)s%(lineno)d%(message)s%(exc_info)s"
DATEFMT = "%Y-%m-%dT%H:%M:%S%z"
RENAME_FIELDS = {
    "asctime": "@timestamp",
    "name": "logger",
    "exc_info": "trace",
    "funcName": "caller",
    "levelname": "level",
}

LOG_MAX_LEN = 4096


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def formatException(self, exc_info):
        """
        Format exception details
        """
        exc_type, value, tb = exc_info
        return {
            "exc_type": exc_type,
            "exc_value": value,
            "trace": [
                {"fn": entry[0], "lnum": entry[1], "func": entry[2], "txt": entry[3]}
                for entry in traceback.extract_tb(tb)
            ],
        }

    def process_log_record(self, log_record):
        """
        Restrict log message length according to IMP requirements
        """
        if "message" in log_record:
            log_record["message"] = log_record["message"][:LOG_MAX_LEN]
        return log_record


def init_app_logger(app_name: str = "app", log_level: Union[str, int] = None):
    if isinstance(log_level, str):
        log_level = log_level.upper()
    if log_level is None:
        log_level = logging.INFO

    # configure root logger
    root_logger = logging.getLogger()

    formatter = CustomJsonFormatter(
        FORMAT_STR,
        rename_fields=RENAME_FIELDS,
        datefmt=DATEFMT,
        static_fields={
            "application": app_name,
        },
    )

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger.addHandler(handler)
    root_logger.propagate = False

    # configure app logger
    app_logger = logging.getLogger(app_name)

    app_logger.setLevel(log_level)

    return app_logger
