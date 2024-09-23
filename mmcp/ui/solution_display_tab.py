# ui/solution_display_tab.py

from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QFileDialog, QMessageBox


class SolutionDisplayTab(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(20, 20, 760, 400)
        self.text_edit.setReadOnly(True)

        self.copy_button = QPushButton("Copy to Clipboard", self)
        self.copy_button.setGeometry(20, 440, 150, 30)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        self.save_button = QPushButton("Save to .mmcp file", self)
        self.save_button.setGeometry(200, 440, 150, 30)
        self.save_button.clicked.connect(self.save_to_file)

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
        Saves the content of the QTextEdit to a .mmcp file.
        """
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Solution", "solution.mmcp", "MMCP Files (*.mmcp)",
                                                  options=options)
        if filename:
            try:
                with open(filename, "w") as f:
                    f.write(self.text_edit.toPlainText())  # Assuming plain text for now
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
