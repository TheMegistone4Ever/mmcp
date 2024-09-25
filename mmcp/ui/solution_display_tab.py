from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QFileDialog, QMessageBox
from numpy import array

from mmcp.data import generate_data_json_file


class SolutionDisplayTab(QWidget):
    def __init__(self):
        super().__init__()

        self.save_button = None
        self.copy_button = None
        self.text_edit = None
        self.filename = "solution.json"

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
            for message, solution in solution_data:
                formatted_solution += f"{message}: {solution}\n"
        else:  # Handle other types of data
            formatted_solution = repr(solution_data)
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

    def set_filename(self, filename: str, extension: str = ".json"):
        """
        Set the default filename for saving the solution data.

        Args:
            filename: The default filename.
            extension: The file extension (e.g., ".json").
        """

        assert extension.startswith("."), "Extension must start with a dot."

        if not filename.endswith(extension):
            filename += extension

        self.filename = filename

    def save_to_file(self):
        """
        Saves the content of the QTextEdit to a .json file.
        """

        options = QFileDialog.Options()
        save_filter = "JSON Files (*.json)"
        filename, _ = QFileDialog.getSaveFileName(self, "Save Solution", self.filename, save_filter, options=options)
        if filename:
            try:
                # Assuming you want to save the formatted solution as JSON
                solution_data = self.get_solution_data_from_text()  # Get the data from QTextEdit
                generate_data_json_file(filename, data=solution_data)  # Use generate_data_json_file to save

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")

    def get_solution_data_from_text(self) -> dict:
        """
        Extract solution data from the QTextEdit (you might need to adjust this based on your formatting).

        Returns:
            A dictionary containing the solution data.
        """

        return {k: array(v) for k, v in
                (line.split(": ", 1) for line in self.text_edit.toPlainText().splitlines() if ": " in line)}
