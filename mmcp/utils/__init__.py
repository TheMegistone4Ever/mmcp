import logging

from .config import Vars

logging.basicConfig(filename=r".\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.debug(f"Initialized {__name__}")

from .config import Criterion, ModelType
from .outs import with_precision, message

__all__ = [
    "Vars",
    "Criterion",
    "ModelType",
    "with_precision",
    "message",
]
