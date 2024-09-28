from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QHBoxLayout, QComboBox,
                             QRadioButton)

from mmcp.core import ConfigurationError
from mmcp.data import ModelData
from mmcp.utils import ModelType, Criterion


class ElementConfigurationWindow(QDialog):
    def __init__(self, master_data: ModelData, element_data, element_index):
        """
        Initializes the element configuration window.
        """

        super().__init__()

        self.master_data = master_data
        self.criterion_combo = None
        self.model_radio_buttons = list()
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

        model_layout = QHBoxLayout()
        model_label = QLabel("Model:", self)
        model_layout.addWidget(model_label)

        for model_type in ModelType:
            radio_button = QRadioButton(str(model_type), self)
            self.model_radio_buttons.append(radio_button)
            model_layout.addWidget(radio_button)
            radio_button.toggled.connect(  # type: ignore
                lambda checked, mt=model_type: self.set_model_type(mt) if checked else None)

        layout.addLayout(model_layout)

        self.criterion_combo = QComboBox(self)
        criterion_layout = QHBoxLayout()
        criterion_label = QLabel("Criterion:", self)
        criterion_layout.addWidget(criterion_label)
        criterion_layout.addWidget(self.criterion_combo)
        layout.addLayout(criterion_layout)

        # Initial Model and Criterion Setup
        self.set_model_type(ModelType(self.element_data["model_types"]))

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

    def set_model_type(self, model_type: ModelType):
        """
        Sets the model type and updates the available criteria.

        Args:
            model_type: The model type to set.
        """

        try:
            self.master_data.set_model_type(self.element_index, model_type)
        except AssertionError as e:
            raise ConfigurationError(f"Error setting model type ({model_type}): {e}") from e

        self.criterion_combo.clear()
        if model_type in (ModelType.LINEAR_MODEL_1, ModelType.LINEAR_MODEL_2):
            self.criterion_combo.addItems(
                [str(Criterion.CRITERION_1), str(Criterion.CRITERION_2), str(Criterion.CRITERION_3)])
        elif model_type == ModelType.LINEAR_MODEL_3:
            self.criterion_combo.addItems([str(Criterion.CRITERION_1)])
        elif model_type == ModelType.COMBINATORIAL_MODEL:
            self.criterion_combo.addItems([str(Criterion.CRITERION_1), str(Criterion.CRITERION_2)])

        # Set the correct radio button as checked
        for radio_button in self.model_radio_buttons:
            if radio_button.text() == str(model_type):
                radio_button.setChecked(True)
                break
