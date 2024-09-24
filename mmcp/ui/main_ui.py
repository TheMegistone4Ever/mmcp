import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox

from mmcp.ui import LoadDataTab, VisualizationTab, SolutionDisplayTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Binary Production System Optimization")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.load_data_tab = LoadDataTab()
        self.solution_display_tab = SolutionDisplayTab()
        self.visualization_tab = VisualizationTab(self.tab_widget, self.solution_display_tab)

        self.tab_widget.addTab(self.load_data_tab, "Load Data")
        self.tab_widget.addTab(self.visualization_tab, "Visualization")
        self.tab_widget.addTab(self.solution_display_tab, "Solution Display")

        self.load_data_tab.data_loaded.connect(self.handle_data_loaded)

    def handle_data_loaded(self, data):
        """
        Handle the data loaded signal from the LoadDataTab.

        Args:
            data: The data loaded from the LoadDataTab.
        """

        if len(data["c"]) < 2:
            QMessageBox.critical(self, "Error", "At least 2 elements are required.")
            return

        self.visualization_tab.set_data(data)
        self.tab_widget.setCurrentIndex(1)  # Switch to Visualization tab


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
