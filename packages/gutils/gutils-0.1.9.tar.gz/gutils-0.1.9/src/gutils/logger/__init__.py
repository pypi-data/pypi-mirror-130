from logging.handlers import RotatingFileHandler
from pathlib import Path, PosixPath
from datetime import datetime
from typing import Union

import logging

from ..components import LogLevel


def init_logger(log_file: Union[Path, str],
                log_level: LogLevel = LogLevel.NOTSET,
                rotate: bool = False,
                name: str = '') -> logging.Logger:
    if not isinstance(log_file, PosixPath):
        log_file = Path(log_file).expanduser()
    if log_level not in LogLevel.items():
        raise ValueError(f"Unknown log level: {log_level}")
    log_format = logging.Formatter(
        f"[%(levelname)s] (%(asctime)s) - {name}: %(message)s")
    logger = logging.getLogger()
    logger.setLevel(log_level.value)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.handlers = [console_handler]

    log_file.parent.mkdir(parents=True, exist_ok=True)
    if log_file.suffix == '':
        log_file.mkdir(parents=True, exist_ok=True)
        log_file /= f"{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log"
    if log_file.name and log_file.name != '':
        if rotate:
            file_handler = RotatingFileHandler(
                log_file, maxBytes=1000000, backupCount=10)
        else:
            file_handler = logging.FileHandler(str(log_file))
        file_handler.setLevel(log_level.value)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    return logger
