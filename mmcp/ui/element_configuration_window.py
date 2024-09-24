from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QHBoxLayout, QComboBox,
                             QRadioButton)


class ElementConfigurationWindow(QDialog):
    def __init__(self, element_data, element_index):
        """
        Initializes the element configuration window.
        """

        super().__init__()

        self.criterion_combo = None
        self.combinatorial_model_radio = None
        self.linear_model_2_radio = None
        self.linear_model_1_radio = None
        self.setWindowTitle(f"Element {element_index + 1} Configuration")
        self.element_data = element_data
        self.element_index = element_index

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI for the element configuration window.
        """

        layout = QVBoxLayout(self)

        # Model selection
        model_layout = QHBoxLayout()
        model_label = QLabel("Model:", self)
        model_layout.addWidget(model_label)

        self.linear_model_1_radio = QRadioButton("Linear Model 1", self)
        self.linear_model_2_radio = QRadioButton("Linear Model 2", self)
        self.combinatorial_model_radio = QRadioButton("Combinatorial Model", self)

        model_layout.addWidget(self.linear_model_1_radio)
        model_layout.addWidget(self.linear_model_2_radio)
        model_layout.addWidget(self.combinatorial_model_radio)

        layout.addLayout(model_layout)

        # Criterion selection
        criterion_layout = QHBoxLayout()
        criterion_label = QLabel("Criterion:", self)
        criterion_layout.addWidget(criterion_label)

        self.criterion_combo = QComboBox(self)
        self.criterion_combo.addItems(["Criterion 1", "Criterion 2", "Criterion 3"])  # Add all criteria

        criterion_layout.addWidget(self.criterion_combo)
        layout.addLayout(criterion_layout)

        # Other element data (you might need to adjust this based on your data structure)
        for key, value in self.element_data.items():
            label = QLabel(f"{key}:", self)
            edit = QLineEdit(str(value), self)
            layout.addWidget(label)
            layout.addWidget(edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)  # type: ignore
        button_box.rejected.connect(self.reject)  # type: ignore
        layout.addWidget(button_box)

    def set_model_type(self, model_type):
        """
        Sets the model type and updates the available criteria.

        Args:
            model_type: The model type to set.
        """

        if model_type == "Linear Model 1":
            self.linear_model_1_radio.setChecked(True)
            self.criterion_combo.clear()
            self.criterion_combo.addItems(["Criterion 1", "Criterion 2", "Criterion 3"])
        elif model_type == "Linear Model 2":
            self.linear_model_2_radio.setChecked(True)
            self.criterion_combo.clear()
            self.criterion_combo.addItems(["Criterion 1", "Criterion 2", "Criterion 3"])
        elif model_type == "Combinatorial Model":
            self.combinatorial_model_radio.setChecked(True)
            self.criterion_combo.clear()
            self.criterion_combo.addItems(["Criterion 1", "Criterion 2"])  # Only Criterion 1 and 2 implemented
