import logging
import os
import sys

from pythonjsonlogger import jsonlogger


def configure_logging(level: str | None = None) -> None:
    """Configure consistent JSON logging for the application."""
    log_level = (level or os.getenv("LOG_LEVEL", "INFO")).upper()

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))

    if not root_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a consistently configured application logger."""
    configure_logging()
    return logging.getLogger(name)
