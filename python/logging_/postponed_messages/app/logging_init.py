import logging
import logging.handlers
from pathlib import Path

from .config import AcmeConfig


class DelayedLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger):
        super().__init__(logger, extra={})
        self._delayed = True
        self._delayed_logs = []

    @property
    def delayed(self):
        return self._delayed

    @delayed.setter
    def delayed(self, val):
        if val and self.delayed:
            # going from delayed to un-delayed, flush cache
            self._flush_delayed()
        self._delayed = val

    def log(self, level, msg, *args, **kwargs):
        # we adjust the default stacklevel offset to account for two additional
        # calls (this function and whoever called it)
        kwargs.setdefault("stacklevel", 3)
        if self.delayed:
            self._delayed_logs.append((level, msg, args, kwargs))
        else:
            if self._delayed_logs:
                self._flush_delayed()
            super().log(level, msg, *args, **kwargs)

    def _flush_delayed(self):
        for level, msg, args, kwargs in self._delayed_logs:
            kwargs["stacklevel"] += 1
            super().log(level, msg, *args, **kwargs)
        self._delayed_logs.clear()


def _make_log_file(config: AcmeConfig) -> Path:
    log_dir = config.log_dir.expanduser().resolve()
    log_dir.mkdir(exist_ok=True, parents=True)
    log_root_file = log_dir / "acme-service.log"
    log_root_file.touch()
    return log_root_file


def _initialize_logging(config: AcmeConfig) -> Path:
    logging_root = _make_log_file(config)
    print_handler = logging.StreamHandler()
    logfmt = "%(asctime)s [%(levelname)-8s] [%(threadName)s (%(thread)d)] %(module)s.%(funcName)s(+L%(lineno)-3d): %(message)s"
    formatter = logging.Formatter(fmt=logfmt)

    print_handler.setFormatter(formatter)
    logging.basicConfig(
        level=config.log_level,
        format=logfmt,
        handlers=[
            logging.handlers.TimedRotatingFileHandler(logging_root, when="D", utc=True, encoding="UTF8"),
            print_handler,
        ],
    )

    logging.captureWarnings(True)

    return logging_root

