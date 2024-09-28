import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QApplication, QVBoxLayout

from mmcp.data import parse_data_json_file, ModelData


class LoadDataTab(QWidget):
    data_loaded = pyqtSignal(ModelData)

    def __init__(self):
        super().__init__()

        self.load_button = None
        self.label = None
        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI for the load data tab with a Microsoft-style theme.
        """

        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Arial;
            }
            QLabel {
                color: #333333; /* Point Charcoal */
            }
            QPushButton {
                background-color: #0078D7; /* Microsoft Blue */
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005A9E; /* Darker blue on hover */
            }
        """)

        layout = QVBoxLayout(self)

        self.label = QLabel("Load .json file:", self)
        self.label.setAlignment(Qt.AlignCenter)
        font = self.label.font()
        font.setPointSize(32)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        layout.addWidget(self.label)

        self.load_button = QPushButton("Browse", self)
        self.load_button.clicked.connect(self.browse_file)  # type: ignore
        self.load_button.move(200, 200)

        layout.addWidget(self.load_button)

    def browse_file(self):
        """
        Opens a file dialog to browse for a .json file.
        Emits the data_loaded signal if the file is successfully loaded.
        """

        options = QFileDialog.Options()
        json_filter = "JSON Files (*.json);;All Files (*)"
        filename, _ = QFileDialog.getOpenFileName(self, "Load .json File", "", json_filter, options=options)
        if filename:
            try:
                data = parse_data_json_file(filename)
                if data:
                    self.data_loaded.emit(data)  # type: ignore
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
                print(f"An error occurred while parsing the data file: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoadDataTab()
    window.show()
    sys.exit(app.exec_())
