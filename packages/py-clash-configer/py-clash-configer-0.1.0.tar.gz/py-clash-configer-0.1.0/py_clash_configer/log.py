import logging

from rich.logging import RichHandler

APP_NAME = 'py-clash-configer'
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger(APP_NAME)
