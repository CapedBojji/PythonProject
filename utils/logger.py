import logging
import sys
from pathlib import Path


def setup_logging(log_file: Path | None = None, level: int = logging.INFO) -> None:
    """
    Configure root logger to write to `log_file` if given,
    otherwise to stdout.
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    fmt = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # Choose handler: FileHandler if path given, else StreamHandler(sys.stdout)
    if log_file:
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setLevel(logging.INFO)
        handler.setFormatter(fmt)
        logger.addHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmt)
    logger.addHandler(handler)


