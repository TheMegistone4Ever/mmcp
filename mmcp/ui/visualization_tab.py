from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QTreeWidget, QTreeWidgetItem, QPushButton, QDialog, QLineEdit, \
    QMessageBox, QMenu

from mmcp import lm, cm
from .element_configuration_window import ElementConfigurationWindow


class VisualizationTab(QWidget):
    def __init__(self, solution_display_tab):
        super().__init__()
        self.data = None
        self.solution_display_tab = solution_display_tab

        self.init_ui()

    def init_ui(self):
        self.dmc_label = QLabel("DMC (Decision Making Center)", self)
        self.dmc_label.setAlignment(Qt.AlignCenter)
        self.dmc_label.setGeometry(200, 20, 200, 30)

        self.dimension_combo = QComboBox(self)
        self.dimension_combo.setGeometry(420, 20, 80, 30)
        self.dimension_combo.addItems(["2", "3", "4", "5"])

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setGeometry(50, 70, 700, 400)
        self.tree_widget.setHeaderLabels(["Elements"])
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)

        self.solve_button = QPushButton("Solve", self)
        self.solve_button.setGeometry(350, 480, 100, 30)
        self.solve_button.clicked.connect(self.solve)
        # self.solve_button.setEnabled(False)  # No need to disable initially

    def solve(self):
        try:
            solutions = []
            for i in range(len(self.data["c_list"])):
                selected_model = self.get_selected_model(i)
                selected_criterion = self.get_selected_criterion(i)

                if selected_model == "Linear Model 1":
                    if selected_criterion == "Criterion 1":
                        solution = lm.first.criterion_1.solve(self.data["c_list"][i], self.data["A_list"][i],
                                                              self.data["b_list"][i], 1000)
                    elif selected_criterion == "Criterion 2":
                        solution = lm.first.criterion_2.solve(self.data["c_list"][i], self.data["A_list"][i],
                                                              self.data["b_list"][i], 0.8)
                    elif selected_criterion == "Criterion 3":
                        solution = lm.first.criterion_3.solve(self.data["c_list"][i], self.data["A_list"][i],
                                                              self.data["b_list"][i], 0.5)
                elif selected_model == "Linear Model 2":
                    if selected_criterion == "Criterion 1":
                        solution = lm.second.criterion_1.solve(self.data["c_list"][i], self.data["A_list"][i],
                                                               self.data["b_list"][i],
                                                               self.data["d_list"][i], 1000)
                    elif selected_criterion == "Criterion 2":
                        solution = lm.second.criterion_2.solve(self.data["c_list"][i], self.data["A_list"][i],
                                                               self.data["b_list"][i],
                                                               self.data["d_list"][i], 0.8)
                    elif selected_criterion == "Criterion 3":
                        solution = lm.second.criterion_3.solve(self.data["c_list"][i], self.data["A_list"][i],
                                                               self.data["b_list"][i],
                                                               self.data["d_list"][i], 0.5)
                elif selected_model == "Combinatorial Model":
                    if selected_criterion == "Criterion 1":
                        solution = cm.first.criterion_1.solve(self.data["processing_times"], self.data["weights"],
                                                              self.data["precedence_graph"])
                    elif selected_criterion == "Criterion 2":
                        solution = cm.first.criterion_2.solve(self.data["processing_times"], self.data["weights"],
                                                              self.data["precedence_graph"],
                                                              0.8)

                if solution:
                    solutions.append(solution)
                else:
                    QMessageBox.warning(self, "Warning", f"No solution found for Element {i + 1}.")

            if solutions:
                self.solution_display_tab.display_solution(solutions)
            else:
                self.solution_display_tab.display_no_solution_message()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            print(f"Error: {e}")

    def get_selected_model(self, element_index):
        element_item = self.tree_widget.topLevelItem(element_index)
        configure_button = self.tree_widget.itemWidget(element_item, 1)

        # If config_window doesn"t exist, assume Linear Model 1
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
        element_item = self.tree_widget.topLevelItem(element_index)
        configure_button = self.tree_widget.itemWidget(element_item, 1)

        # If config_window doesn"t exist, assume Criterion 1
        if configure_button.config_window is None:
            return "Criterion 1"

        config_window = configure_button.config_window
        return config_window.criterion_combo.currentText()

    def set_data(self, data):
        self.data = data
        self.populate_tree()

    def populate_tree(self):
        self.tree_widget.clear()
        # self.solve_button.setEnabled(False)  # No need to disable

        if self.data:
            num_elements = len(self.data["c_list"])
            for i in range(num_elements):
                element_item = QTreeWidgetItem(self.tree_widget, [f"Element {i + 1}"])

                for key, value in self.data.items():
                    if isinstance(value, list) and len(value) > i:
                        QTreeWidgetItem(element_item, [f"{key}: {value[i]}"])

                configure_button = QPushButton("Configure", self.tree_widget)
                configure_button.config_window = None  # Create a config window for each element
                self.tree_widget.setItemWidget(element_item, 1, configure_button)

                # Automatically open and accept the configuration window for default selection
                self.open_configuration_window(i, "Linear Model 1")
                configure_button.config_window.accept()

    def show_context_menu(self, pos):
        item = self.tree_widget.itemAt(pos)
        if item:
            element_index = self.tree_widget.indexOfTopLevelItem(item)

            menu = QMenu(self)

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

    def open_configuration_window(self, element_index, model_type):
        element_data = {}
        for key, value in self.data.items():
            if isinstance(value, list) and len(value) > element_index:
                element_data[key] = value[element_index]

        element_item = self.tree_widget.topLevelItem(element_index)
        configure_button = self.tree_widget.itemWidget(element_item, 1)

        if configure_button.config_window is None:
            config_window = ElementConfigurationWindow(element_data)
            configure_button.config_window = config_window

        config_window = configure_button.config_window
        config_window.set_model_type(model_type)

        if config_window.exec_() == QDialog.Accepted:
            for edit in config_window.findChildren(QLineEdit):
                key = edit.objectName()
                value = edit.text()

                self.data[key] = value
            self.populate_tree()
