from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox, QTreeWidget, QTreeWidgetItem, QPushButton, QDialog, QLineEdit,
                             QMessageBox, QMenu)

from mmcp import lm, cm
from mmcp.ui import ElementConfigurationWindow
from mmcp.utils import Vars


class VisualizationTab(QWidget):
    def __init__(self, tab_widget, solution_display_tab):
        """
        Initializes the VisualizationTab.
        """

        super().__init__()

        self.tab_widget = tab_widget
        self.solution_display_tab = solution_display_tab

        self.solve_button = None
        self.tree_widget = None
        self.elements_to_display_combo = None  # Renamed for clarity
        self.dmc_label = None
        self.data = None
        self.c, self.A, self.b, self.d = None, None, None, None
        self.model_types, self.processing_times, self.weights, self.precedence_graph = None, None, None, None

        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI for the visualization tab.
        """

        self.dmc_label = QLabel("DMC (Decision Making Center)", self)
        self.dmc_label.setAlignment(Qt.AlignCenter)
        self.dmc_label.setGeometry(200, 20, 200, 30)

        self.elements_to_display_combo = QComboBox(self)  # Renamed
        self.elements_to_display_combo.setGeometry(420, 20, 80, 30)
        self.elements_to_display_combo.currentIndexChanged.connect(self.on_elements_to_display_changed)  # type: ignore

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setGeometry(50, 70, 700, 400)
        self.tree_widget.setHeaderLabels(["Elements"])
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)  # type: ignore

        self.solve_button = QPushButton("Solve", self)
        self.solve_button.setGeometry(350, 480, 100, 30)
        self.solve_button.clicked.connect(self.solve)  # type: ignore

    def solve(self):
        """
        Solves the optimization problem for each element in the data.
        Displays the solution in the SolutionDisplayTab.
        """

        num_elements = self.get_num_elements_to_display()  # Use the helper method

        try:
            solutions = []
            for i in range(num_elements):
                selected_model = self.get_selected_model(i)
                selected_criterion = self.get_selected_criterion(i)

                solution = None
                if selected_model == "Linear Model 1":
                    if selected_criterion == "Criterion 1":
                        solution = lm.first.criterion_1.solve(self.c[i], self.A[i], self.b[i], Vars.M)
                    elif selected_criterion == "Criterion 2":
                        solution = lm.first.criterion_2.solve(self.c[i], self.A[i], self.b[i], Vars.z_min, Vars.alpha)
                    elif selected_criterion == "Criterion 3":
                        solution = lm.first.criterion_3.solve(self.c[i], self.A[i], self.b[i], Vars.weights)
                elif selected_model == "Linear Model 2":
                    if selected_criterion == "Criterion 1":
                        solution = lm.second.criterion_1.solve(self.c[i], self.A[i], self.b[i], self.d[i], Vars.M)
                    elif selected_criterion == "Criterion 2":
                        solution = lm.second.criterion_2.solve(self.c[i], self.A[i], self.b[i], self.d[i], Vars.z_min,
                                                               Vars.alpha)
                    elif selected_criterion == "Criterion 3":
                        solution = lm.second.criterion_3.solve(self.c[i], self.A[i], self.b[i], self.d[i], Vars.weights)
                elif selected_model == "Combinatorial Model":
                    if selected_criterion == "Criterion 1":
                        solution = cm.first.criterion_1.solve(self.processing_times, self.weights,
                                                              self.precedence_graph, Vars.M)
                    elif selected_criterion == "Criterion 2":
                        solution = cm.first.criterion_2.solve(self.processing_times, self.weights,
                                                              self.precedence_graph, Vars.target_difference)

                if solution:
                    solutions.append(solution)
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

        num_elements = len(self.c)
        self.elements_to_display_combo.addItems(list(map(str, range(2, num_elements + 1))))
        self.elements_to_display_combo.setCurrentIndex(num_elements - 1)  # Set default to max value

        save_filename = f"sol_{"x".join(map(str, self.A.shape))}_{"m".join(map(str, self.model_types))}"
        self.solution_display_tab.set_filename(save_filename)

        self.populate_tree()

    def populate_tree(self):
        """
        Populates the tree widget with the data.
        """

        self.tree_widget.clear()

        if self.data:
            num_elements_to_display = self.get_num_elements_to_display()
            for i in range(num_elements_to_display):
                element_item = QTreeWidgetItem(self.tree_widget, [f"Element {i + 1}"])

                for key, value in self.data.items():
                    if len(value) > i:
                        QTreeWidgetItem(element_item, [f"{key}: {list(value)[i]}"])

                configure_button = QPushButton("Configure", self.tree_widget)
                configure_button.config_window = None
                self.tree_widget.setItemWidget(element_item, 1, configure_button)

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
            show_action = menu.addAction("Show")
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
            self.populate_tree()

    def on_elements_to_display_changed(self, index):
        """
        Handles the event when the elements to display combo box value changes.
        """

        self.populate_tree()

    def get_num_elements_to_display(self):
        """
        Returns the selected number of elements to display from the combo box.
        """

        return int(txt) if (txt := self.elements_to_display_combo.currentText()) else 0
