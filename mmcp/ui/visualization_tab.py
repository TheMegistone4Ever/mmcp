from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QTreeWidget, QTreeWidgetItem, QPushButton, QDialog, QLineEdit, QMenu,
                             QMessageBox, QCheckBox, QVBoxLayout, QScrollArea, QGridLayout)

from mmcp import lm, cm
from mmcp.ui import ElementConfigurationWindow
from mmcp.utils import Vars

model_mapping = {
    "Linear Model 1": lm.first,
    "Linear Model 2": lm.second,
    "Linear Model 3": lm.third,
    "Combinatorial Model": cm.first,
}

criterion_mapping = {
    "Criterion 1": "criterion_1",
    "Criterion 2": "criterion_2",
    "Criterion 3": "criterion_3",
}


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
        self.elements_checkboxes = []
        self.master_checkbox = None
        self.dmc_label = None
        self.data = None
        self.c, self.A, self.b, self.d = None, None, None, None
        self.model_types, self.processing_times, self.weights, self.precedence_graph = None, None, None, None

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI for the visualization tab using a 2x2 grid layout.
        """

        # DMC Label with a modern, flat style
        self.dmc_label = QLabel("DMC (Decision Making Center)", self)
        self.dmc_label.setAlignment(Qt.AlignCenter)
        self.dmc_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2E8BC0;  /* Chrome-like Blue */
            padding: 10px 0;
        """)

        # Solve Button with Material Design style
        self.solve_button = QPushButton("Solve", self)
        self.solve_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;  /* Flat Green */
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 20px;  /* Rounded corners for Chrome style */
                border: none;  /* No borders for flat look */
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);  /* Subtle shadow */
            }
            QPushButton:hover {
                background-color: #45A049;  /* Slightly darker green on hover */
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);  /* Stronger shadow on hover */
            }
            QPushButton:pressed {
                background-color: #3D8C43;  /* Darker shade for press */
            }
        """)
        self.solve_button.setCursor(Qt.PointingHandCursor)
        self.solve_button.clicked.connect(self.solve)  # type: ignore

        # Tree Widget styled with a flat, modern look
        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["Elements"])
        self.tree_widget.setStyleSheet("""
            QTreeWidget {
                background-color: #FFFFFF;  /* Flat white background */
                border: 1px solid #E0E0E0;  /* Light gray border */
                border-radius: 10px;  /* Slightly rounded edges */
            }
            QTreeWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #2E8BC0;  /* Blue header background */
                color: white;
                font-weight: bold;
                padding: 8px;
                border: none;  /* Remove border for cleaner look */
            }
        """)
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)  # type: ignore

        # --- Main Layout (Grid) ---
        main_layout = QGridLayout(self)

        # --- Top Row ---
        # Scroll Area for Checkboxes, with rounded and flat design
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #F9F9F9;  /* Light gray background for Chrome-style */
                border: 1px solid #E0E0E0;  /* Thin light gray border */
                border-radius: 10px;  /* Slightly rounded corners */
            }
            QWidget {
                background-color: #F9F9F9;  /* Same background for consistency */
            }
        """)
        scroll_widget = QWidget(self.scroll_area)
        self.scroll_area.setWidget(scroll_widget)
        self.checkbox_layout = QVBoxLayout(scroll_widget)
        main_layout.addWidget(self.scroll_area, 0, 0)  # Checkboxes in Row 0, Column 0

        # DMC Label and Button (Row 0, Column 1)
        top_right_layout = QVBoxLayout()
        top_right_layout.addWidget(self.dmc_label)
        top_right_layout.addWidget(self.solve_button)
        main_layout.addLayout(top_right_layout, 0, 1)

        # --- Bottom Row (Elements List) ---
        main_layout.addWidget(self.tree_widget, 1, 0, 1, 2)  # Span 2 columns

    def populate_tree(self):
        """
        Populates the tree widget with the data and manages checkboxes.
        """

        self.tree_widget.clear()
        self.elements_checkboxes.clear()
        # Remove master_checkbox from layout if it exists
        if self.master_checkbox is not None:
            self.checkbox_layout.removeWidget(self.master_checkbox)
            self.master_checkbox.deleteLater()  # Important: delete the widget

        if self.data:
            total_elements = len(self.c)

            self.master_checkbox = QCheckBox("Select All", self)
            self.master_checkbox.setChecked(True)
            self.master_checkbox.stateChanged.connect(self.on_master_checkbox_changed)  # type: ignore
            self.checkbox_layout.addWidget(self.master_checkbox)

            for i in range(total_elements):
                element_item = QTreeWidgetItem(self.tree_widget, [f"Element {i + 1}"])
                for key, value in self.data.items():
                    if len(value) > i:
                        QTreeWidgetItem(element_item, [f"{key}: {list(value)[i]}"])

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

        try:
            solutions = []
            for i, checkbox in enumerate(self.elements_checkboxes):
                if not checkbox.isChecked():
                    continue

                selected_model = self.get_selected_model(i)
                selected_criterion = self.get_selected_criterion(i)

                try:
                    model_class = model_mapping[selected_model]
                    criterion_method = getattr(model_class, criterion_mapping[selected_criterion])
                except KeyError:
                    QMessageBox.warning(self, "Warning", f"Invalid model or criterion selected for Element {i + 1}.")
                    continue

                if selected_model.startswith("Linear Model"):
                    if selected_model == "Linear Model 1":
                        params = [self.c[i], self.A[i], self.b[i]]
                        if selected_criterion == "Criterion 1":
                            params.append(Vars.M)
                        elif selected_criterion == "Criterion 2":
                            params.extend([Vars.z_min, Vars.alpha])
                        elif selected_criterion == "Criterion 3":
                            params.append(Vars.weights)
                        solution = criterion_method.solve(*params)
                    elif selected_model == "Linear Model 2":
                        params = [self.c[i], self.A[i], self.b[i], self.d[i]]
                        if selected_criterion == "Criterion 1":
                            params.append(Vars.M)
                        elif selected_criterion == "Criterion 2":
                            params.extend([Vars.z_min, Vars.alpha])
                        elif selected_criterion == "Criterion 3":
                            params.append(Vars.weights)
                        solution = criterion_method.solve(*params)
                    else:  # Linear Model 3
                        # TODO: Implement Linear Model 3
                        # params = [self.c, self.A, self.b, self.d, self.model_types, Vars.beta]
                        # solution = criterion_method.solve(*params)
                        raise NotImplementedError("Linear Model 3 is not implemented.")
                else:  # Combinatorial Model
                    solution = criterion_method.solve(
                        self.processing_times, self.weights, self.precedence_graph,
                        Vars.M if selected_criterion == "Criterion 1" else Vars.target_difference
                    )

                if solution:
                    solutions.append((f"Element {i + 1}", solution))
                else:
                    QMessageBox.warning(self, "Warning", f"No solution found for Element {i + 1}.")

            if solutions:
                self.solution_display_tab.display_solution(solutions)
            else:
                self.solution_display_tab.display_no_solution_message()

            self.tab_widget.setCurrentIndex(2)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            print(f"Error: {e}")

    def get_selected_model(self, element_index):
        """
        Get the selected model type for the given element index.

        Args:
            element_index: The index of the element.

        Returns:
            The selected model type.
        """

        element_item = self.tree_widget.topLevelItem(element_index)
        configure_button = self.tree_widget.itemWidget(element_item, 1)

        # If config_window doesn't exist, assume Linear Model 1
        if configure_button.config_window is None:
            return "Linear Model 1"

        config_window = configure_button.config_window
        if config_window.linear_model_1_radio.isChecked():
            return "Linear Model 1"
        elif config_window.linear_model_2_radio.isChecked():
            return "Linear Model 2"
        elif config_window.combinatorial_model_radio.isChecked():
            return "Combinatorial Model"
        else:
            return None

    def get_selected_criterion(self, element_index):
        """
        Get the selected criterion for the given element index.

        Args:
            element_index: The index of the element.

        Returns:
            The selected criterion.
        """

        element_item = self.tree_widget.topLevelItem(element_index)
        configure_button = self.tree_widget.itemWidget(element_item, 1)

        # If config_window doesn't exist, assume Criterion 1
        if configure_button.config_window is None:
            return "Criterion 1"

        config_window = configure_button.config_window
        return config_window.criterion_combo.currentText()

    def set_data(self, data):
        """
        Sets the data for visualization.

        Args:
            data: The data to be visualized.
        """

        # TODO: replace with class: Data (extends @dataclass)
        self.data = data
        self.c, self.A, self.b, self.d, self.model_types, self.processing_times, self.weights, self.precedence_graph = \
            data["c"], data["A"], data["b"], data["d"], data["model_types"], data["processing_times"], \
                data["weights"], data["precedence_graph"]

        save_filename = f"sol_{"x".join(map(str, self.A.shape))}_{"m".join(map(str, self.model_types))}"
        self.solution_display_tab.set_filename(save_filename)

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
            linear_model_1_action = menu.addAction("Linear Model 1")
            linear_model_2_action = menu.addAction("Linear Model 2")
            combinatorial_model_action = menu.addAction("Combinatorial Model")

            action = menu.exec_(self.tree_widget.mapToGlobal(pos))

            if action == linear_model_1_action:
                self.open_configuration_window(element_index, "Linear Model 1")
            elif action == linear_model_2_action:
                self.open_configuration_window(element_index, "Linear Model 2")
            elif action == combinatorial_model_action:
                self.open_configuration_window(element_index, "Combinatorial Model")
            else:
                self.open_configuration_window(element_index, None)

    def open_configuration_window(self, element_index, model_type):
        """
        Opens the configuration window for the specified element index and model type.

        Args:
            element_index: The index of the element.
            model_type: The model type to set.
        """

        element_data = {}
        for key, value in self.data.items():
            if len(value) > element_index:
                element_data[key] = list(value)[element_index]

        element_item = self.tree_widget.topLevelItem(element_index)
        configure_button = self.tree_widget.itemWidget(element_item, 1)

        if not configure_button.config_window:
            configure_button.config_window = ElementConfigurationWindow(element_data, element_index)

        if model_type:
            configure_button.config_window.set_model_type(model_type)

        if configure_button.config_window.exec_() == QDialog.Accepted:
            for edit in configure_button.config_window.findChildren(QLineEdit):
                self.data[edit.objectName()] = edit.text()

    def on_master_checkbox_changed(self, state):
        """
        Handles the primary checkbox state change.

        Args:
            state: The state of the primary checkbox.
        """

        for checkbox in self.elements_checkboxes:
            if checkbox.text() != "Select All":
                if checkbox.isChecked() != (state == Qt.Checked):
                    checkbox.setChecked(state)

    def on_element_checkbox_changed(self, state):
        """
        Handles the element checkbox state change.

        Args:
            state: The state of the element checkbox.
        """

        num_checked = sum(checkbox.isChecked() for checkbox in self.elements_checkboxes)
        self.master_checkbox.setCheckState(Qt.Checked if num_checked == len(self.elements_checkboxes)
                                           else Qt.Unchecked if num_checked == 0 else Qt.PartiallyChecked)
        print(f"Element checkbox state changed to: {state}, {num_checked = }.")
