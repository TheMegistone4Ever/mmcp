from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QTreeWidget, QTreeWidgetItem, QPushButton, QDialog, QMenu,
                             QMessageBox, QCheckBox, QVBoxLayout, QScrollArea, QGridLayout)

from mmcp.core import Solver
from mmcp.data import ModelData, SolutionData
from mmcp.ui import ElementConfigurationWindow
from mmcp.utils import ModelType, Criterion


class VisualizationTab(QWidget):
    def __init__(self, tab_widget, solution_display_tab):
        """
        Initializes the VisualizationTab.
        """

        super().__init__()

        self.scroll_area = None
        self.tab_widget = tab_widget
        self.solution_display_tab = solution_display_tab

        self.checkbox_layout = None
        self.solve_button = None
        self.tree_widget = None
        self.elements_checkboxes = list()
        self.master_checkbox = None
        self.dmc_label = None
        self.data = ModelData()

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI for the visualization tab using a 2x2 grid layout with a Microsoft-style theme.
        """

        self.setStyleSheet("""
            QLabel {
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
            QTreeWidget {
                border: 1px solid #CCCCCC;
            }
            QHeaderView::section {
                background-color: #F0F0F0; /* Light gray */
                color: #333333; /* Point Charcoal */
                padding: 8px;
                border: 1px solid #CCCCCC;
                border-bottom: none;
            }
            QCheckBox {
                color: #333333; /* Point Charcoal */
            }
            QScrollArea {
                border: 1px solid #CCCCCC;
            }
        """)

        self.dmc_label = QLabel("DMC (Decision Making Center)", self)
        self.dmc_label.setAlignment(Qt.AlignCenter)
        self.dmc_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.solve_button = QPushButton("Solve", self)
        self.solve_button.setCursor(Qt.PointingHandCursor)
        self.solve_button.clicked.connect(self.solve)  # type: ignore

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["Elements"])
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)  # type: ignore

        # --- Main Layout (Grid) ---
        main_layout = QGridLayout(self)

        # --- Top Row - Scroll Area for Checkboxes ---
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget(self.scroll_area)
        self.scroll_area.setWidget(scroll_widget)
        self.checkbox_layout = QVBoxLayout(scroll_widget)
        main_layout.addWidget(self.scroll_area, 0, 0)

        # DMC Label and Button (Row 0, Column 1)
        top_right_layout = QVBoxLayout()
        top_right_layout.addWidget(self.dmc_label)
        top_right_layout.addWidget(self.solve_button)
        main_layout.addLayout(top_right_layout, 0, 1)

        # --- Bottom Row (Elements List) - Span 2 columns ---
        main_layout.addWidget(self.tree_widget, 1, 0, 1, 2)

    # noinspection PyProtectedMember
    def populate_tree(self):
        """
        Populates the tree widget with the data and manages checkboxes.
        """

        self.tree_widget.clear()
        self.elements_checkboxes.clear()
        # Remove master_checkbox from layout if it exists
        if self.master_checkbox is not None:
            self.checkbox_layout.removeWidget(self.master_checkbox)
            self.master_checkbox.deleteLater()

        if self.data.c is not None:
            self.master_checkbox = QCheckBox("Select All", self)
            self.master_checkbox.setChecked(True)
            self.master_checkbox.stateChanged.connect(self.on_master_checkbox_changed)  # type: ignore
            self.checkbox_layout.addWidget(self.master_checkbox)

            for i in range(len(self.data.c)):
                element_item = QTreeWidgetItem(self.tree_widget, [f"Element {i + 1}"])
                for k, v in self.data._asdict().items():
                    if len(v) > i:
                        QTreeWidgetItem(element_item, [f"{k}: {str(ModelType(v[i]))
                        if k == "model_types" else list(v)[i]}"])

                checkbox = QCheckBox(f"Element {i + 1}", self)
                checkbox.setChecked(True)
                checkbox.stateChanged.connect(self.on_element_checkbox_changed)  # type: ignore
                self.elements_checkboxes.append(checkbox)
                self.checkbox_layout.addWidget(checkbox)

                configure_button = QPushButton("Configure", self.tree_widget)
                configure_button.config_window = None
                self.tree_widget.setItemWidget(element_item, 1, configure_button)

    def solve(self):
        """
        Solves the optimization problem for each element in the data.
        Displays the solution in the SolutionDisplayTab.
        """

        solutions = SolutionData(values=list())

        try:
            for i, checkbox in enumerate(self.elements_checkboxes):
                if not checkbox.isChecked():
                    continue
                solution = Solver(self.ith_data(i), self.selected_model_type(i), self.selected_criterion(i)).solve()
                if solution:
                    solutions.values.append(solution)
                else:
                    QMessageBox.warning(self, "Warning", f"No solution found for Element {i + 1}.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            print(f"Error: {e}")

        finally:
            self.solution_display_tab.display_solution(solutions)
            self.tab_widget.setCurrentIndex(2)  # Switch to Solution Display tab

    # noinspection PyProtectedMember
    def ith_data(self, element_index: int):
        """
        Get the data for the given element index.

        Args:
            element_index: The index of the element.

        Returns:
            The data for the element.
        """

        element_data = dict()
        for key, value in self.data._asdict().items():
            if len(value) > element_index:
                element_data[key] = list(value)[element_index]

        return ModelData(**element_data)

    def selected_model_type(self, element_index):
        """
        Get the selected model type for the given element index.

        Args:
            element_index: The index of the element.

        Returns:
            The selected model type as a ModelType enum member.
        """

        element_item = self.tree_widget.topLevelItem(element_index)
        configure_button = self.tree_widget.itemWidget(element_item, 1)

        if (config_window := configure_button.config_window) is None:
            return ModelType.LINEAR_MODEL_1

        if config_window.linear_model_1_radio.isChecked():
            return ModelType.LINEAR_MODEL_1
        elif config_window.linear_model_2_radio.isChecked():
            return ModelType.LINEAR_MODEL_2
        elif config_window.linear_model_3_radio.isChecked():
            return ModelType.LINEAR_MODEL_3
        elif config_window.comb_model_radio.isChecked():
            return ModelType.COMBINATORIAL_MODEL

    def selected_criterion(self, element_index):
        """
        Get the selected criterion for the given element index.

        Args:
            element_index: The index of the element.

        Returns:
            The selected criterion.
        """

        configure_button = self.tree_widget.itemWidget(self.tree_widget.topLevelItem(element_index), 1)
        if configure_button.config_window:
            text_combo = configure_button.config_window.criterion_combo.currentText()
            if text_combo == "Criterion 2":
                return Criterion.CRITERION_2
            elif text_combo == "Criterion 3":
                return Criterion.CRITERION_3
        return Criterion.CRITERION_1

    def set_data(self, data):
        """
        Sets the data for visualization.

        Args:
            data: The data to be visualized.
        """

        self.data = data
        self.solution_display_tab.set_filename(f"sol_{"x".join(map(str, self.data.A.shape))}")
        self.populate_tree()

    def show_context_menu(self, pos):
        """
        Shows a context menu for the tree widget items.

        Args:
            pos: The position of the context menu.
        """

        item = self.tree_widget.itemAt(pos)
        if item:
            # Traverse up to the top-level item
            while item.parent() is not None:
                item = item.parent()

            element_index = self.tree_widget.indexOfTopLevelItem(item)

            menu = QMenu(self)
            menu.addAction("Show")
            linear_model_1_action = menu.addAction(str(ModelType.LINEAR_MODEL_1))
            linear_model_2_action = menu.addAction(str(ModelType.LINEAR_MODEL_2))
            linear_model_3_action = menu.addAction(str(ModelType.LINEAR_MODEL_3))
            combinatorial_model_action = menu.addAction(str(ModelType.COMBINATORIAL_MODEL))

            action = menu.exec_(self.tree_widget.mapToGlobal(pos))

            model_type = None
            if action == linear_model_1_action:
                model_type = ModelType.LINEAR_MODEL_1
            elif action == linear_model_2_action:
                model_type = ModelType.LINEAR_MODEL_2
            elif action == linear_model_3_action:
                model_type = ModelType.LINEAR_MODEL_3
            elif action == combinatorial_model_action:
                model_type = ModelType.COMBINATORIAL_MODEL
            self.open_configuration_window(element_index, model_type)

    # noinspection PyProtectedMember
    def open_configuration_window(self, element_index, model_type: ModelType = None):
        """
        Opens the configuration window for the specified element index and model type.

        Args:
            element_index: The index of the element.
            model_type: The model type to set.
        """

        element_data = dict()
        for key, value in self.data._asdict().items():
            if len(value) > element_index:
                element_data[key] = list(value)[element_index]

        element_item = self.tree_widget.topLevelItem(element_index)
        configure_button = self.tree_widget.itemWidget(element_item, 1)

        if not configure_button.config_window:
            configure_button.config_window = ElementConfigurationWindow(self.data, element_data, element_index)

        if model_type:
            configure_button.config_window.set_model_type(model_type)

        if configure_button.config_window.exec_() == QDialog.Accepted:
            selected_model_type = None
            if configure_button.config_window.linear_model_1_radio.isChecked():
                selected_model_type = ModelType.LINEAR_MODEL_1
            elif configure_button.config_window.linear_model_2_radio.isChecked():
                selected_model_type = ModelType.LINEAR_MODEL_2
            elif configure_button.config_window.linear_model_3_radio.isChecked():
                selected_model_type = ModelType.LINEAR_MODEL_3
            elif configure_button.config_window.comb_model_radio.isChecked():
                selected_model_type = ModelType.COMBINATORIAL_MODEL

            if selected_model_type is not None:
                configure_button.config_window.set_model_type(selected_model_type)

            # Update the specific tree item instead of repopulating the entire tree
            element_item.takeChildren()
            for key, value in self.data._asdict().items():
                if len(value) > element_index:
                    QTreeWidgetItem(element_item, [f"{key}: {str(ModelType(value[element_index]))
                    if key == "model_types" else list(value)[element_index]}"])

    def on_master_checkbox_changed(self, state):
        """
        Handles the primary checkbox state change.

        Args:
            state: The state of the primary checkbox.
        """

        for checkbox in self.elements_checkboxes:
            if checkbox.isChecked() != (state == Qt.Checked):
                checkbox.setChecked(state)

    def on_element_checkbox_changed(self):
        """Handles the element checkbox state change."""

        num_checked = sum(checkbox.isChecked() for checkbox in self.elements_checkboxes)
        self.master_checkbox.setCheckState(Qt.Checked if num_checked == len(self.elements_checkboxes)
                                           else Qt.Unchecked if num_checked == 0 else Qt.PartiallyChecked)
