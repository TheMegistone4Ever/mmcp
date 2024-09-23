import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QApplication

from mmcp import parse_mmcp_file


class LoadDataTab(QWidget):
    data_loaded = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.load_button = None
        self.label = None
        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI for the load data tab.
        """

        self.label = QLabel("Load .mmcp file:", self)
        self.label.move(20, 20)

        self.load_button = QPushButton("Browse", self)
        self.load_button.move(150, 15)
        self.load_button.clicked.connect(self.browse_file)  # type: ignore

    def browse_file(self):
        """
        Opens a file dialog to browse for a .mmcp file.
        Emits the data_loaded signal if the file is successfully loaded.
        """

        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Load .mmcp File", "", "MMCP Files (*.mmcp);;All Files (*)",
                                                  options=options)
        if filename:
            try:
                data = parse_mmcp_file(filename)
                if data:
                    self.data_loaded.emit(data)  # type: ignore
                else:
                    QMessageBox.critical(self, "Error", "Failed to parse .mmcp file. Please check the file format.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")  # Display error message
                print(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoadDataTab()
    window.show()
    sys.exit(app.exec_())
