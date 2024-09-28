import logging

logging.basicConfig(filename=r"..\..\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.debug(f"Initialized {__name__}")

from . import first, second, third

__all__ = [
    "first",
    "second",
    "third"
]
