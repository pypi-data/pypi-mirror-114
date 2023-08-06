import json
import logging
import sys
from pathlib import Path

from pythonjsonlogger import jsonlogger

from .vcdilogintrospect import get_nicest_module_name


def get_logger_by_name(name):
    return logging.getLogger(name)


class StdHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        if record.levelno >= logging.WARNING:
            stream = sys.stderr
        else:
            stream = sys.stdout
        stream.write(msg)
        stream.write("\n")
        self.flush()


def get_logging_attr(name):
    return getattr(logging, name)


LEVELS = "debug info warn warning error critical exception".split()


class Logger:
    def __init__(self, name=None, real_logger=None, top_level=True):
        if real_logger:
            self._logger = real_logger
            return

        if name is None:
            name = get_nicest_module_name()

            if top_level:
                name = name.split(".")[0]

        self.name = name

        self._logger = get_logger_by_name(name)

        self.handlers = {}

    def set_level(self, level="DEBUG"):
        _level = get_logging_attr(level)
        self._logger.setLevel(_level)

    def set_handler_by_key(self, k, h):
        old_h = self.handlers.pop(k, None)

        if old_h:
            self._logger.removeHandler(old_h)

        self._logger.addHandler(h)

    def add_std_handler(self, level="DEBUG", set_logger_level=True):
        if set_logger_level:
            self.set_level(level)
        _level = get_logging_attr(level)
        h = StdHandler()
        h.setLevel(_level)
        self._logger.addHandler(h)

        self.set_handler_by_key("std", h)

    def add_null_handler(self, level="DEBUG"):

        _level = get_logging_attr(level)

        h = logging.NullHandler()

        h.setLevel(_level)
        self._logger.addHandler(h)

        self.handlers["null"] = h

    def add_json_handler(self, level="DEBUG", path="log.json"):
        p = Path(path).expanduser().resolve()
        _level = get_logging_attr(level)

        def json_translate(obj):
            pass

        h = logging.FileHandler(str(p))

        formatter = jsonlogger.JsonFormatter(
            json_default=json_translate, json_encoder=json.JSONEncoder
        )
        h.setFormatter(formatter)

        h.setLevel(_level)
        self._logger.addHandler(h)

        self.handlers["json"] = h

    def __getattr__(self, method, *args, **kwargs):
        if method.startswith("_"):
            raise AttributeError

        return getattr(self._logger, method)


def p():
    import logging_tree

    s = logging_tree.format.build_description()
    print()
    print(s)
    print()
    print()
    # logging_tree.printout()


class AutoLogger:
    def __getattr__(self, name):
        self.name = get_nicest_module_name()
        _logger = Logger(name=self.name)
        return getattr(_logger, name)


log = AutoLogger()
