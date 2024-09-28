import logging

logging.basicConfig(filename=r"..\..\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.debug(f"Initialized {__name__}")

from .element_configuration_window import ElementConfigurationWindow
from .load_data_tab import LoadDataTab
from .solution_display_tab import SolutionDisplayTab
from .visualization_tab import VisualizationTab

__all__ = [
    "ElementConfigurationWindow",
    "LoadDataTab",
    "SolutionDisplayTab",
    "VisualizationTab",
]
