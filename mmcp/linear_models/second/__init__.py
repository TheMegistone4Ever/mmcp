import logging

logging.basicConfig(filename=r"..\..\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.debug(f"Initialized {__name__}")

from . import criterion_1, criterion_2, criterion_3

__all__ = [
    "criterion_1",
    "criterion_2",
    "criterion_3",
]
