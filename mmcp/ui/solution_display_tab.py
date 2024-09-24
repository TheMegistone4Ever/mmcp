# ui/solution_display_tab.py

import numpy as np
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QFileDialog, QMessageBox

from mmcp import generate_data_json_file


class SolutionDisplayTab(QWidget):
    def __init__(self):
        super().__init__()

        self.save_button = None
        self.copy_button = None
        self.text_edit = None
        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI for the solution display tab.
        """

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(20, 20, 760, 400)
        self.text_edit.setReadOnly(True)

        self.copy_button = QPushButton("Copy to Clipboard", self)
        self.copy_button.setGeometry(20, 440, 150, 30)
        self.copy_button.clicked.connect(self.copy_to_clipboard)  # type: ignore

        self.save_button = QPushButton("Save to .json file", self)
        self.save_button.setGeometry(200, 440, 150, 30)
        self.save_button.clicked.connect(self.save_to_file)  # type: ignore

    def display_solution(self, solution_data):
        """
        Formats and displays the solution data in the QTextEdit.

        Args:
            solution_data: A dictionary or list containing the solution data.
        """

        formatted_solution = ""
        if isinstance(solution_data, dict):
            for key, value in solution_data.items():
                formatted_solution += f"{key}: {value}\n"
        elif isinstance(solution_data, list):
            for i, item in enumerate(solution_data):
                formatted_solution += f"Item {i + 1}: {item}\n"
        else:
            formatted_solution = str(solution_data)  # Handle other data types

        self.text_edit.setPlainText(formatted_solution)

    def display_no_solution_message(self):
        """
        Displays a message indicating that no optimal solution was found.
        """

        self.text_edit.setPlainText("No optimal solution found. Please check your input data.")

    def copy_to_clipboard(self):
        """
        Copies the content of the QTextEdit to the clipboard.
        """

        self.text_edit.selectAll()
        self.text_edit.copy()

    def save_to_file(self):
        """
        Saves the content of the QTextEdit to a .json file.
        """

        options = QFileDialog.Options()
        # TODO: Better filename with information from the data (pass filename: str to this method via class constructor)
        filename, _ = QFileDialog.getSaveFileName(self, "Save Solution", f"solution.json", "JSON Files (*.json)",
                                                  options=options)  # Updated filter
        if filename:
            try:
                # Assuming you want to save the formatted solution as JSON
                solution_data = self.get_solution_data_from_text()  # Get the data from QTextEdit
                generate_data_json_file(filename, data=solution_data)  # Use generate_data_json_file to save

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

    def get_solution_data_from_text(self) -> dict:
        """Extract solution data from the QTextEdit (you might need to adjust this based on your formatting)."""
        text = self.text_edit.toPlainText()
        # Example: If your format is "key: value\n", you can parse it like this:
        solution_data = {}
        for line in text.splitlines():
            if ": " in line:
                key, value = line.split(": ", 1)
                solution_data[key] = np.array(value)
        return solution_data
