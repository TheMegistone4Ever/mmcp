import logging

logging.basicConfig(filename=r"..\..\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout

from mmcp.core import FileSavingError
from mmcp.data import generate_data_json_file, SolutionData


class SolutionDisplayTab(QWidget):
    logging.debug(f"Initialized {__name__}")

    def __init__(self):
        logging.debug("Initializing SolutionDisplayTab.")
        super().__init__()

        self.save_button = None
        self.copy_button = None
        self.text_edit = None
        self.filename = "solution.json"
        self.solution = None

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI for the solution display tab with a Microsoft-style theme.
        """

        self.setStyleSheet("""
            QTextEdit {
                border: 1px solid #CCCCCC;
                padding: 5px;
                font-size: 12pt;
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

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        button_layout = QHBoxLayout()

        self.copy_button = QPushButton("Copy to Clipboard", self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)  # type: ignore
        button_layout.addWidget(self.copy_button)

        self.save_button = QPushButton("Save to .json file", self)
        self.save_button.clicked.connect(self.save_to_file)  # type: ignore
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)

    def display_solution(self, solution_data: SolutionData):
        """
        Formats and displays the solution data in the QTextEdit.

        Args:
            solution_data: The solution data to display.
        """
        logging.debug("Displaying solution in SolutionDisplayTab.")

        self.solution = solution_data
        self.text_edit.setPlainText(str(self.solution) if len(self.solution.values)
                                    else "No optimal solution found.\nPlease check your input data.")

    def copy_to_clipboard(self):
        """
        Copies the content of the QTextEdit to the clipboard.
        """
        logging.debug("Copying solution to clipboard.")
        self.text_edit.selectAll()
        self.text_edit.copy()

    def set_filename(self, filename: str, extension: str = ".json"):
        """
        Set the default filename for saving the solution data.

        Args:
            filename: The default filename.
            extension: The file extension (e.g., ".json").
        """
        logging.debug(f"Setting default filename to: {filename}{extension}")
        assert extension.startswith("."), "Extension must start with a dot."

        if not filename.endswith(extension):
            filename += extension

        self.filename = filename

    def save_to_file(self):
        """
        Saves the content of the QTextEdit to a .json file.
        """
        logging.debug("Saving solution to file.")

        options = QFileDialog.Options()
        save_filter = "JSON Files (*.json)"
        filename, _ = QFileDialog.getSaveFileName(self, "Save Solution", self.filename, save_filter, options=options)
        if filename:
            logging.debug(f"Saving solution to: {filename}")
            try:
                generate_data_json_file(filename, data=self.solution)
                logging.info(f"Solution saved to: {filename}")
                QMessageBox.information(self, "Success", "File saved successfully.")
            except FileSavingError as e:
                logging.exception(f"Failed to save file: {e}")
                QMessageBox.critical(self, "Error", f"Failed to save file: {e}")
            else:
                logging.info(f"Solution saved to: {filename}")
                QMessageBox.information(self, "Success", "File saved successfully.")
            finally:
                self.filename = filename
