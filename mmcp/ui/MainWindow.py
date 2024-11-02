import logging
from os import makedirs
from os.path import join

logs_dir = r".\logs"
makedirs(logs_dir, exist_ok=True)
logging.basicConfig(filename=join(logs_dir, "mmcp.log"), level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMessageBox

from mmcp.ui.CustomTabBar import CustomTabBar
from mmcp.data import ModelData
from mmcp.ui import LoadDataTab, VisualizationTab, SolutionDisplayTab


class MainWindow(QMainWindow):
    logging.debug(f"Initialized {__name__}")

    def __init__(self):
        logging.debug("Initializing MainWindow.")
        super().__init__()

        self.setWindowTitle("Binary Production System Optimization")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = None
        self.visualization_tab = None
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

        tab_widget = QTabWidget(self)
        self.setCentralWidget(tab_widget)
        tab_widget.setTabsClosable(False)

        tab_widget.setTabBar(CustomTabBar())

        load_data_tab = LoadDataTab()
        solution_display_tab = SolutionDisplayTab()
        visualization_tab = VisualizationTab(tab_widget, solution_display_tab)

        tab_widget.addTab(load_data_tab, "Load Data")
        tab_widget.addTab(visualization_tab, "Visualization")
        tab_widget.addTab(solution_display_tab, "Solution Display")

        load_data_tab.data_loaded.connect(self.handle_data_loaded)

        self.visualization_tab = visualization_tab
        self.tab_widget = tab_widget

    def handle_data_loaded(self, data: ModelData):
        """Handle the data loaded signal from the LoadDataTab."""
        logging.debug("Data loaded signal received in MainWindow.")

        if len(data.c) < 2:
            logging.error("At least 2 elements are required.")
            QMessageBox.critical(self, "Error", "At least 2 elements are required.")
            return

        logging.debug("Passing data to VisualizationTab.")
        self.visualization_tab.set_data(data)
        self.tab_widget.setCurrentIndex(1)  # Switch to Visualization tab
