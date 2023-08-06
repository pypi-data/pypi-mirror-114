"""Set up logging for the project"""
import logging
from pathlib import Path
from typing import Optional, Union

from rich.console import Console
from rich.logging import RichHandler

_logger: Optional[logging.Logger] = None


def _add_file_handler(file_path: Optional[Union[str, Path]]):
    file_handler = logging.FileHandler(file_path)
    fmt = "%(levelname)-8s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
    file_handler.setFormatter(logging.Formatter(fmt))
    _logger.addHandler(file_handler)


def logger(file_path: Optional[Union[str, Path]] = None) -> logging.Logger:
    """
    Get logger of the project

    Parameters
    ----------
    file_path if firs call and not `None` then setup a file logger with provided path

    Returns
    -------
    logger: an instance of `logging.Logger`
    """
    global _logger

    if _logger is not None and file_path is not None:
        for idx, handler in enumerate(_logger.handlers):
            if isinstance(handler, logging.FileHandler):
                del _logger.handlers[idx]
        _add_file_handler(file_path)

    if _logger is None:
        _logger = logging.getLogger(__name__)

        # stdout handler (default)
        # handler: logging.Handler = logging.StreamHandler()
        rich_handler: logging.Handler = RichHandler(console=Console(width=180))
        rich_handler.setFormatter(logging.Formatter("%(message)s"))
        _logger.addHandler(rich_handler)

        # file handler (if file_path is provided)
        if file_path is not None:
            _add_file_handler(file_path)

        _logger.setLevel(logging.DEBUG)
    return _logger
