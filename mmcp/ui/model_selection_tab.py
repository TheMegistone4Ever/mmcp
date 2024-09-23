from PyQt5.QtCore import pyqtSignal, QModelIndex

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QWidget, QTreeView,
                             QTextEdit, QVBoxLayout)


# Assuming your parser and other project modules are accessible
# You might need to adjust import paths based on your project structure


class ModelSelectionTab(QWidget):
    modelSelected = pyqtSignal(str, str)  # Signal for model selection
    criterionDoubleClicked = pyqtSignal(str, str)  # Signal for double-click

    def __init__(self):
        super().__init__()
        self.setEnabled(False)  # Initially disable until data is loaded

        layout = QVBoxLayout()

        self.model_tree = QTreeView()
        self.model_tree.clicked.connect(self.handle_model_tree_click)
        self.model_tree.doubleClicked.connect(self.handle_model_tree_double_click)

        self.model_description = QTextEdit()
        self.model_description.setReadOnly(True)

        layout.addWidget(self.model_tree)
        layout.addWidget(self.model_description)
        self.setLayout(layout)

        self.populate_model_tree()

    def populate_model_tree(self):
        model = QStandardItemModel()
        self.model_tree.setModel(model)

        # Add linear models
        linear_models_item = QStandardItem("Linear Models")
        model.appendRow(linear_models_item)

        # First linear model
        first_linear_item = QStandardItem("Linear Model - First")
        linear_models_item.appendRow(first_linear_item)
        first_linear_item.appendRow(QStandardItem("Criterion 1"))
        first_linear_item.appendRow(QStandardItem("Criterion 2"))
        first_linear_item.appendRow(QStandardItem("Criterion 3"))

        # Second linear model
        second_linear_item = QStandardItem("Linear Model - Second")
        linear_models_item.appendRow(second_linear_item)
        second_linear_item.appendRow(QStandardItem("Criterion 1"))
        second_linear_item.appendRow(QStandardItem("Criterion 2"))
        second_linear_item.appendRow(QStandardItem("Criterion 3"))

        # Add combinatorial model
        combinatorial_models_item = QStandardItem("Combinatorial Model")
        model.appendRow(combinatorial_models_item)
        combinatorial_models_item.appendRow(QStandardItem("Criterion 1"))
        combinatorial_models_item.appendRow(QStandardItem("Criterion 2"))

        # ... Add other models as needed

    def handle_model_tree_click(self, index: QModelIndex):
        item = self.model_tree.model().itemFromIndex(index)
        if item.parent() is not None:  # Check if it's a child item (model instance)
            model_type = item.parent().text()
            model_instance = item.text()
            self.model_description.setPlainText(
                f"Selected Model Type: {model_type}\n"
                f"Selected Model Instance: {model_instance}\n\n"
                # Add detailed description here based on model_type and model_instance
            )
            self.modelSelected.emit(model_type, model_instance)

    def handle_model_tree_double_click(self, index: QModelIndex):
        item = self.model_tree.model().itemFromIndex(index)
        if item.parent() is not None:  # Check if it's a child item (criterion)
            model_type = item.parent().text()
            criterion = item.text()
            self.criterionDoubleClicked.emit(model_type, criterion)
