import logging

logging.basicConfig(filename=r"..\..\logs\mmcp.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QTreeWidget, QTreeWidgetItem, QPushButton, QDialog, QMenu, QMessageBox,
                             QCheckBox, QVBoxLayout, QScrollArea, QGridLayout, QHBoxLayout, QComboBox)

from mmcp.core import Solver, ConfigurationError, ModelTypeError, CriterionError
from mmcp.data import ModelData, SolutionData
from mmcp.ui import ElementConfigurationWindow
from mmcp.utils import ModelType, Criterion


class VisualizationTab(QWidget):
    logging.debug(f"Initialized {__name__}")

    def __init__(self, tab_widget, solution_display_tab):
        """
        Initializes the VisualizationTab.
        """
        self.master_checkbox = None
        self.tree_widget = None
        self.checkbox_layout = None
        self.threads_combo = None
        logging.debug("Initializing VisualizationTab.")

        super().__init__()

        self.tab_widget = tab_widget
        self.solution_display_tab = solution_display_tab

        self.data = ModelData()
        self.elements_checkboxes = list()
        self.config_windows = dict()

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

        dmc_label = QLabel("DMC (Decision Making Center)", self)
        dmc_label.setAlignment(Qt.AlignCenter)
        dmc_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        solve_button = QPushButton("Solve", self)
        solve_button.setCursor(Qt.PointingHandCursor)
        solve_button.clicked.connect(self.solve)  # type: ignore

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["Elements"])
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.show_context_menu)  # type: ignore

        # --- Main Layout (Grid) ---
        main_layout = QGridLayout(self)

        # --- Top Row - Scroll Area for Checkboxes ---
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget(scroll_area)
        scroll_area.setWidget(scroll_widget)
        checkbox_layout = QVBoxLayout(scroll_widget)
        main_layout.addWidget(scroll_area, 0, 0)

        # DMC Label and Button (Row 0, Column 1)
        top_right_layout = QVBoxLayout()
        top_right_layout.addWidget(dmc_label)
        top_right_layout.addWidget(solve_button)
        dmc_label.setStyleSheet("padding-bottom: 50px;")
        main_layout.addLayout(top_right_layout, 0, 1)

        # --- Threads Selection ---
        threads_layout = QHBoxLayout()
        threads_label = QLabel("Threads:", self)
        threads_layout.addWidget(threads_label)
        self.threads_combo = QComboBox(self)
        self.threads_combo.addItems(["1", "2", "4", "8", "16", "32"])  # Add thread options
        self.threads_combo.setCurrentIndex(0)  # Default to 1 thread
        threads_layout.addWidget(self.threads_combo)
        main_layout.addLayout(threads_layout, 0, 1)

        # --- Bottom Row (Elements List) - Span 2 columns ---
        main_layout.addWidget(self.tree_widget, 1, 0, 1, 2)

        self.checkbox_layout = checkbox_layout
        self.master_checkbox = self._create_master_checkbox()

    def _create_master_checkbox(self):
        """Creates and adds the master checkbox to the layout."""
        logging.debug("Creating master checkbox.")
        master_checkbox = QCheckBox("Select All", self)
        master_checkbox.setChecked(True)
        master_checkbox.stateChanged.connect(self.on_master_checkbox_changed)  # type: ignore
        self.checkbox_layout.addWidget(master_checkbox)
        return master_checkbox

    # noinspection PyProtectedMember
    def populate_tree(self):
        """
        Populates the tree widget with the data and manages checkboxes.
        """
        logging.debug("Populating tree widget with data.")
        self.tree_widget.clear()
        self.elements_checkboxes.clear()

        if self.data.c is not None:
            for i in range(len(self.data.c)):
                element_item = QTreeWidgetItem(self.tree_widget, [f"Element {i + 1}"])
                self._add_element_data_to_tree(element_item, i)

                checkbox = QCheckBox(f"Element {i + 1}", self)
                checkbox.setChecked(True)
                checkbox.stateChanged.connect(self.on_element_checkbox_changed)  # type: ignore
                self.elements_checkboxes.append(checkbox)
                self.checkbox_layout.addWidget(checkbox)

                configure_button = QPushButton("Configure", self.tree_widget)
                configure_button.clicked.connect(lambda _, idx=i: self.open_configuration_window(idx))  # type: ignore
                self.tree_widget.setItemWidget(element_item, 1, configure_button)

    # noinspection PyProtectedMember
    def _add_element_data_to_tree(self, element_item, element_idx):
        """Adds element data to the tree widget item."""
        logging.debug(f"Adding data for element {element_idx + 1} to tree widget.")
        for k, v in self.data._asdict().items():
            if len(v) > element_idx:
                QTreeWidgetItem(element_item, [f"{k}: {str(ModelType(v[element_idx]))
                if k == "model_types" else list(v)[element_idx]}"])

    def solve(self):
        """
        Solves the optimization problem using the selected number of threads and maintains element order.
        """
        logging.debug("Solve button clicked.")
        solutions = SolutionData(names=list(), values=list())

        num_threads = int(self.threads_combo.currentText())  # Get selected thread count
        logging.debug(f"Using {num_threads} threads for solving.")

        with ThreadPoolExecutor(max_workers=num_threads) as pool:
            futures = OrderedDict()
            for i, checkbox in enumerate(self.elements_checkboxes):
                if not checkbox.isChecked():
                    continue
                logging.debug(f"Submitting solve task for element {i + 1} to thread pool.")
                futures[i] = pool.submit(self._solve_for_element, i)

            for element_idx, future in futures.items():
                try:
                    solution = future.result()
                    if solution:
                        logging.info(f"Solution found for element {element_idx + 1}: {solution}")
                        solutions.names.append(f"Element №{element_idx + 1}")
                        solutions.values.append(solution)
                    else:
                        logging.warning(f"No solution found for Element {element_idx + 1}.")
                        QMessageBox.warning(self, "Warning", f"No solution found for Element {element_idx + 1}.")
                except (ConfigurationError, ModelTypeError, CriterionError) as e:
                    logging.exception(f"Failed to solve for Element {element_idx + 1}. Error: {e}")
                    QMessageBox.critical(self, "Error", f"Failed to solve for Element {element_idx + 1}. Error: {e}")
                except Exception as e:
                    logging.exception(f"An unexpected error occurred: {e}")
                    QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

        logging.debug("Displaying solutions in SolutionDisplayTab.")
        self.solution_display_tab.display_solution(solutions)
        self.tab_widget.setCurrentIndex(2)  # Switch to Solution Display tab

    def _solve_for_element(self, element_idx):
        """Solves the optimization problem for a single element."""
        logging.debug(f"Solving for element {element_idx + 1} with model type: "
                      f"{self.selected_model_type(element_idx)} and criterion: {self.selected_criterion(element_idx)}")
        return Solver(self.ith_data(element_idx),
                      self.selected_model_type(element_idx),
                      self.selected_criterion(element_idx)).solve()

    # noinspection PyProtectedMember
    def ith_data(self, element_idx: int):
        """
        Get the data for the given element index.

        Args:
            element_idx: The index of the element.

        Returns:
            The data for the element.
        """
        logging.debug(f"Retrieving data for element {element_idx + 1}.")

        return ModelData(**{k: list(v)[element_idx] for k, v in self.data._asdict().items() if len(v) > element_idx})

    def selected_model_type(self, element_idx):
        """
        Get the selected model type for the given element index.
        """
        logging.debug(f"Getting selected model type for element {element_idx + 1}.")
        config_window = self.config_windows.get(element_idx)
        if config_window is None:
            return ModelType.LINEAR_MODEL_1
        for i, model_type in enumerate(ModelType):
            if config_window and config_window.model_radio_buttons[i].isChecked():
                return model_type

    def selected_criterion(self, element_idx):
        """
        Get the selected criterion for the given element index.
        """
        logging.debug(f"Getting selected criterion for element {element_idx + 1}.")
        config_window = self.config_windows.get(element_idx)
        if config_window and config_window.criterion_combo:
            criteria = config_window.criterion_combo.currentIndex() + 1
            try:
                self.data.set_criteria(element_idx, criteria)
                return Criterion(criteria)
            except ValueError:
                logging.warning(f"Invalid criterion selected: {criteria}")
        return Criterion.CRITERION_1

    def set_data(self, data):
        """
        Sets the data for visualization.
        """
        logging.debug(f"Setting data in VisualizationTab: {data}")
        self.data = data
        self.solution_display_tab.set_filename(f"sol_{"x".join(map(str, self.data.A.shape))}")
        self.populate_tree()

    def show_context_menu(self, pos):
        """
        Shows a context menu for the tree widget items.
        """
        logging.debug("Showing context menu.")
        item = self.tree_widget.itemAt(pos)
        if item:
            element_idx = self._get_element_idx_from_tree_item(item)

            menu = QMenu(self)
            show_action = menu.addAction("Show")
            actions = {model_type: menu.addAction(str(model_type)) for model_type in ModelType}

            action = menu.exec_(self.tree_widget.mapToGlobal(pos))

            if action in actions.values():
                model_type = next(model_type for model_type, act in actions.items() if act == action)
                self.open_configuration_window(element_idx, model_type)
            elif action == show_action:
                self.open_configuration_window(element_idx)

    def _get_element_idx_from_tree_item(self, item):
        """Gets the element index from the tree widget item."""
        logging.debug("Getting element index from tree item.")
        while item.parent() is not None:
            item = item.parent()
        return self.tree_widget.indexOfTopLevelItem(item)

    # noinspection PyProtectedMember
    def open_configuration_window(self, element_idx, model_type: ModelType = None):
        """
        Opens the configuration window for the specified element.
        """
        logging.debug(f"Opening configuration window for element {element_idx + 1}.")
        element_data = {k: list(v)[element_idx] for k, v in self.data._asdict().items() if len(v) > element_idx}

        if element_idx not in self.config_windows:
            self.config_windows[element_idx] = ElementConfigurationWindow(self.data, element_data, element_idx)

        config_window = self.config_windows.get(element_idx)

        if model_type:
            config_window.set_model_type(model_type)

        if config_window.exec_() == QDialog.Accepted:
            self._update_tree_item(element_idx)

    def _update_tree_item(self, element_idx):
        """Updates the tree widget item for the given element index."""
        logging.debug(f"Updating tree item for element {element_idx + 1}.")
        element_item = self.tree_widget.topLevelItem(element_idx)
        element_item.takeChildren()
        self._add_element_data_to_tree(element_item, element_idx)

    def on_master_checkbox_changed(self, state):
        """Handles the master checkbox state change."""
        logging.debug(f"Master checkbox changed to: {"Checked" if state == Qt.Checked else "Unchecked"}")
        for checkbox in self.elements_checkboxes:
            checkbox.blockSignals(True)
            checkbox.setChecked(state == Qt.Checked)
            checkbox.blockSignals(False)

    def on_element_checkbox_changed(self, state):
        """Handles the element checkbox state change."""
        logging.debug(f"Element checkbox changed to: {"Checked" if state == Qt.Checked else "Unchecked"}")
        num_checked = sum(checkbox.isChecked() for checkbox in self.elements_checkboxes)
        total_checkboxes = len(self.elements_checkboxes)

        self.master_checkbox.blockSignals(True)
        if num_checked == total_checkboxes:
            self.master_checkbox.setCheckState(Qt.Checked)
        elif num_checked == 0:
            self.master_checkbox.setCheckState(Qt.Unchecked)
        else:
            self.master_checkbox.setCheckState(Qt.PartiallyChecked)
        self.master_checkbox.blockSignals(False)
