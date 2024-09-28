import logging

from mmcp.utils import Vars

logging.basicConfig(filename=r"..\..\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.debug(f"Initialized {__name__}")

from . import combinatorial_models as cm
from . import core
from . import data
from . import linear_models as lm
from . import ui
from . import utils

__all__ = [
    "cm",
    "lm",
    "core",
    "data",
    "utils",
    "ui",
]
