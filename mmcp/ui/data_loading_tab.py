import yaml
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit, QFileDialog,
                             QTextEdit, QMessageBox, QVBoxLayout, QHBoxLayout)

# Assuming your parser and other project modules are accessible
# You might need to adjust import paths based on your project structure
from mmcp import parse_mmcp_file  # Or wherever your parser is located


class DataLoadingTab(QWidget):
    dataLoaded = pyqtSignal(dict)  # Signal to emit when data is loaded

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.file_path_label = QLabel("MMCP File:")
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)

        self.data_preview = QTextEdit()
        self.data_preview.setReadOnly(True)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(self.browse_button)

        layout.addLayout(file_layout)
        layout.addWidget(self.data_preview)

        self.setLayout(layout)

    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select MMCP File", "", "MMCP Files (*.mmcp)", options=options)

        if filename:
            self.file_path_edit.setText(filename)
            self.load_data(filename)

    def load_data(self, filename):
        try:
            data = parse_mmcp_file(filename)  # Call your parser
            self.data_preview.setPlainText(yaml.dump(data))  # Display data in YAML format
            self.dataLoaded.emit(data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading file: {e}")
