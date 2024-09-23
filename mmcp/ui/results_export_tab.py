from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QHBoxLayout)


# Assuming your parser and other project modules are accessible
# You might need to adjust import paths based on your project structure


class ResultsExportTab(QWidget):
    saveResults = pyqtSignal(str)  # Signal to emit when save button is clicked

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.results_table = QTableWidget()
        # Configure table as needed (e.g., number of columns, headers)

        self.filename_label = QLabel("Filename:")
        self.filename_edit = QLineEdit()
        self.filename_edit.setText("results_{model_type}_{model_instance}.mmcp")  # Set default filename

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_results_to_file)

        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_results_to_clipboard)

        filename_layout = QHBoxLayout()
        filename_layout.addWidget(self.filename_label)
        filename_layout.addWidget(self.filename_edit)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.copy_button)

        layout.addWidget(self.results_table)
        layout.addLayout(filename_layout)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def display_results(self, results):
        self.results_table.clearContents()
        self.results_table.setRowCount(0)

        # Assuming results is a list of lists or something similar
        if isinstance(results, list):
            for row in results:
                row_index = self.results_table.rowCount()
                self.results_table.insertRow(row_index)
                for col_index, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.results_table.setItem(row_index, col_index, item)

        # Or if results is a dictionary, you might need to adapt
        elif isinstance(results, dict):
            # ... (Handle dictionary results)
            pass

    def save_results_to_file(self):
        filename = self.filename_edit.text()
        self.saveResults.emit(filename)

    def copy_results_to_clipboard(self):
        # ... (Implement copying results to clipboard)
        pass

    def clear_results(self):
        self.results_table.clearContents()
        self.results_table.setRowCount(0)
