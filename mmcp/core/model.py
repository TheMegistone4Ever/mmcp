import logging

logging.basicConfig(filename=r".\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

from abc import ABC, abstractmethod


class Model(ABC):
    logging.debug(f"Initialized {__name__}")

    @abstractmethod
    def solve(self, *args, **kwargs):
        pass
