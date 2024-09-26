import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox, QTabBar

from mmcp.data import ModelData
from mmcp.ui import LoadDataTab, VisualizationTab, SolutionDisplayTab


class CustomTabBar(QTabBar):
    def tabSizeHint(self, index):
        """Override the tab size hint to set a custom width."""
        # Set a dynamic size based on the current widget size and number of tabs
        if self.count() == 0:
            return QSize(0, 50)  # No tabs
        total_width = self.parent().width()  # Get the width of the parent (QTabWidget)
        tab_width = total_width // self.count()  # Calculate equal width for each tab
        return QSize(tab_width, 50)  # Return calculated width and fixed height


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Binary Production System Optimization")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.setTabsClosable(False)

        # Set the custom tab bar
        self.tab_widget.setTabBar(CustomTabBar())

        self.load_data_tab = LoadDataTab()
        self.solution_display_tab = SolutionDisplayTab()
        self.visualization_tab = VisualizationTab(self.tab_widget, self.solution_display_tab)

        self.tab_widget.addTab(self.load_data_tab, "Load Data")
        self.tab_widget.addTab(self.visualization_tab, "Visualization")
        self.tab_widget.addTab(self.solution_display_tab, "Solution Display")

        self.load_data_tab.data_loaded.connect(self.handle_data_loaded)

        self.init_ui()

    def init_ui(self):
        """Initializes the UI for the main window with a Microsoft-style theme."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
                font-family: Arial;
            }
            QTabWidget::pane {
                border: none; 
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #F0F0F0; /* Light gray */
                color: #333333; /* Point Charcoal */
                padding: 8px 16px;
                border: 1px solid #CCCCCC;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                font-weight: bold;
                border-bottom: 2px solid #0078D7; /* Microsoft Blue */
            }
            QTabBar::tab:hover {
                background-color: #E0E0E0; /* Slightly darker gray on hover */
            }
        """)

    def handle_data_loaded(self, data: ModelData):
        """Handle the data loaded signal from the LoadDataTab."""
        if len(data.c) < 2:
            QMessageBox.critical(self, "Error", "At least 2 elements are required.")
            return

        self.visualization_tab.set_data(data)
        self.tab_widget.setCurrentIndex(1)  # Switch to Visualization tab

    def resizeEvent(self, event):
        """Handle resize event to update tab widths."""
        self.tab_widget.tabBar().update()  # Update the tab bar to reflect size changes
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
