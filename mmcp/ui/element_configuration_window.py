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
        self.linear_model_1_radio = None
        self.linear_model_2_radio = None
        self.linear_model_3_radio = None
        self.comb_model_radio = None
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

        self.linear_model_1_radio = QRadioButton(str(ModelType.LINEAR_MODEL_1), self)
        self.linear_model_2_radio = QRadioButton(str(ModelType.LINEAR_MODEL_2), self)
        self.linear_model_3_radio = QRadioButton(str(ModelType.LINEAR_MODEL_3), self)
        self.comb_model_radio = QRadioButton(str(ModelType.COMBINATORIAL_MODEL), self)

        self.criterion_combo = QComboBox(self)
        if self.element_data["model_types"] == int(ModelType.LINEAR_MODEL_1):
            self.linear_model_1_radio.setChecked(True)
            self.criterion_combo.addItems([
                str(Criterion.CRITERION_1), str(Criterion.CRITERION_2), str(Criterion.CRITERION_3)
            ])
        elif self.element_data["model_types"] == int(ModelType.LINEAR_MODEL_2):
            self.linear_model_2_radio.setChecked(True)
            self.criterion_combo.addItems([
                str(Criterion.CRITERION_1), str(Criterion.CRITERION_2), str(Criterion.CRITERION_3)
            ])
        elif self.element_data["model_types"] == int(ModelType.LINEAR_MODEL_3):
            self.linear_model_3_radio.setChecked(True)
            self.criterion_combo.addItems([str(Criterion.CRITERION_1)])
        elif self.element_data["model_types"] == int(ModelType.COMBINATORIAL_MODEL):
            self.comb_model_radio.setChecked(True)
            self.criterion_combo.addItems([str(Criterion.CRITERION_1), str(Criterion.CRITERION_2)])

        model_layout.addWidget(self.linear_model_1_radio)
        model_layout.addWidget(self.linear_model_2_radio)
        model_layout.addWidget(self.linear_model_3_radio)
        model_layout.addWidget(self.comb_model_radio)

        layout.addLayout(model_layout)

        criterion_layout = QHBoxLayout()
        criterion_label = QLabel("Criterion:", self)
        criterion_layout.addWidget(criterion_label)

        criterion_layout.addWidget(self.criterion_combo)

        self.linear_model_1_radio.toggled.connect(  # type: ignore
            lambda checked: self.set_model_type(ModelType.LINEAR_MODEL_1) if checked else None)
        self.linear_model_2_radio.toggled.connect(  # type: ignore
            lambda checked: self.set_model_type(ModelType.LINEAR_MODEL_2) if checked else None)
        self.linear_model_3_radio.toggled.connect(  # type: ignore
            lambda checked: self.set_model_type(ModelType.LINEAR_MODEL_3) if checked else None)
        self.comb_model_radio.toggled.connect(  # type: ignore
            lambda checked: self.set_model_type(ModelType.COMBINATORIAL_MODEL) if checked else None)

        layout.addLayout(criterion_layout)

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

        current_criterion = self.criterion_combo.currentText()
        if model_type == ModelType.LINEAR_MODEL_1:
            self.linear_model_1_radio.setChecked(True)
            self.criterion_combo.clear()
            self.criterion_combo.addItems([
                str(Criterion.CRITERION_1), str(Criterion.CRITERION_2), str(Criterion.CRITERION_3)
            ])
        elif model_type == ModelType.LINEAR_MODEL_2:
            self.linear_model_2_radio.setChecked(True)
            self.criterion_combo.clear()
            self.criterion_combo.addItems([
                str(Criterion.CRITERION_1), str(Criterion.CRITERION_2), str(Criterion.CRITERION_3)
            ])
        elif model_type == ModelType.LINEAR_MODEL_3:
            self.linear_model_3_radio.setChecked(True)
            self.criterion_combo.clear()
            self.criterion_combo.addItems([str(Criterion.CRITERION_1)])
        elif model_type == ModelType.COMBINATORIAL_MODEL:
            self.comb_model_radio.setChecked(True)
            self.criterion_combo.clear()
            self.criterion_combo.addItems([str(Criterion.CRITERION_1), str(Criterion.CRITERION_2)])
        if (index := self.criterion_combo.findText(current_criterion)) != -1:
            self.criterion_combo.setCurrentIndex(index)
