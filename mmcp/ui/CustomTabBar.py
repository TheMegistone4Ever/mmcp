from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTabBar

from mmcp.utils import LOGGER


class CustomTabBar(QTabBar):
    LOGGER.debug(f"Initialized {__name__}")

    def tabSizeHint(self, index):
        """
        Override the tab size hint to set a custom width.
        Set a dynamic size based on the current widget size and number of tabs.
        """
        return QSize(self.parent().width() // self.count(), 50) if self.count() else QSize(0, 50)
