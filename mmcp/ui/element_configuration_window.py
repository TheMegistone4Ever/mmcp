from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QHBoxLayout, QComboBox,
                             QRadioButton)

from mmcp.data import ModelData


class ElementConfigurationWindow(QDialog):
    def __init__(self, master_data: ModelData, element_data, element_index):
        """
        Initializes the element configuration window.
        """

        super().__init__()

        self.master_data = master_data
        self.criterion_combo = None
        self.comb_model_radio = None
        self.linear_model_2_radio = None
        self.linear_model_1_radio = None
        self.setWindowTitle(f"Element {element_index + 1} Configuration")
        self.element_data = element_data
        self.element_index = element_index

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI for the element configuration window with a Microsoft-style theme.
        """

        self.setStyleSheet("""
            QDialog {
                background-color: white;
                font-family: Arial;
            }
            QLabel {
                color: #333333; /* Point Charcoal */
            }
            QLineEdit, QComboBox {
                border: 1px solid #CCCCCC;
                padding: 5px;
            }
            QRadioButton {
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
            QDialogButtonBox QPushButton {
                min-width: 80px; /* Ensure consistent button width */
            }
        """)

        layout = QVBoxLayout(self)

        # Model selection
        model_layout = QHBoxLayout()
        model_label = QLabel("Model:", self)
        model_layout.addWidget(model_label)

        self.linear_model_1_radio = QRadioButton("Linear Model 1", self)
        self.linear_model_2_radio = QRadioButton("Linear Model 2", self)
        self.comb_model_radio = QRadioButton("Combinatorial Model", self)

        # Initialize the radio button based on the model type
        if self.element_data["model_types"] == 1:
            self.linear_model_1_radio.setChecked(True)
        elif self.element_data["model_types"] == 2:
            self.linear_model_2_radio.setChecked(True)
        elif self.element_data["model_types"] == 3:
            self.comb_model_radio.setChecked(True)

        model_layout.addWidget(self.linear_model_1_radio)
        model_layout.addWidget(self.linear_model_2_radio)
        model_layout.addWidget(self.comb_model_radio)

        layout.addLayout(model_layout)

        # Criterion selection
        criterion_layout = QHBoxLayout()
        criterion_label = QLabel("Criterion:", self)
        criterion_layout.addWidget(criterion_label)

        self.criterion_combo = QComboBox(self)
        self.criterion_combo.addItems(["Criterion 1", "Criterion 2", "Criterion 3"])  # Add all criteria

        criterion_layout.addWidget(self.criterion_combo)

        self.linear_model_1_radio.toggled.connect(  # type: ignore
            lambda checked: self.set_model_type("Linear Model 1") if checked else None)
        self.linear_model_2_radio.toggled.connect(  # type: ignore
            lambda checked: self.set_model_type("Linear Model 2") if checked else None)
        self.comb_model_radio.toggled.connect(  # type: ignore
            lambda checked: self.set_model_type("Combinatorial Model") if checked else None)

        layout.addLayout(criterion_layout)

        # Other element data (make them read-only)
        for key, value in self.element_data.items():
            label = QLabel(f"{key}:", self)
            edit = QLineEdit(str(value), self)
            edit.setReadOnly(True)
            layout.addWidget(label)
            layout.addWidget(edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)  # type: ignore
        button_box.rejected.connect(self.reject)  # type: ignore
        layout.addWidget(button_box)

    def set_model_type(self, model_type: str):
        """
        Sets the model type and updates the available criteria.

        Args:
            model_type: The model type to set.
        """

        self.master_data.set_model_type(self.element_index, model_type)

        if model_type == "Linear Model 1":
            self.linear_model_1_radio.setChecked(True)
            self.criterion_combo.clear()
            self.criterion_combo.addItems(["Criterion 1", "Criterion 2", "Criterion 3"])
        elif model_type == "Linear Model 2":
            self.linear_model_2_radio.setChecked(True)
            self.criterion_combo.clear()
            self.criterion_combo.addItems(["Criterion 1", "Criterion 2", "Criterion 3"])
        elif model_type == "Combinatorial Model":
            self.comb_model_radio.setChecked(True)
            self.criterion_combo.clear()
            self.criterion_combo.addItems(["Criterion 1", "Criterion 2"])
