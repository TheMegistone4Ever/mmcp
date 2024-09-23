import yaml
from PyQt5.QtWidgets import (QMainWindow, QWidget, QTabWidget,
                             QMessageBox, QVBoxLayout, QAction)

from mmcp import lm, cm  # Importing linear_models and combinatorial_models modules
from .data_loading_tab import DataLoadingTab
from .model_selection_tab import ModelSelectionTab
from .results_export_tab import ResultsExportTab


# Assuming your parser and other project modules are accessible
# You might need to adjust import paths based on your project structure


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MMCP Data Processing Application")
        self.setGeometry(100, 100, 800, 600)

        self.loaded_data = None  # Store the parsed MMCF data
        self.selected_model_type = None
        self.selected_model_instance = None
        self.results = None

        self.create_menu()
        self.create_central_widget()

    def create_menu(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def create_central_widget(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        tabs = QTabWidget()
        self.data_loading_tab = DataLoadingTab()
        self.model_selection_tab = ModelSelectionTab()
        self.results_export_tab = ResultsExportTab()

        tabs.addTab(self.data_loading_tab, "Data Loading")
        tabs.addTab(self.model_selection_tab, "Model Selection")
        tabs.addTab(self.results_export_tab, "Results & Export")

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        central_widget.setLayout(layout)

        # Connect signals from tabs
        self.data_loading_tab.dataLoaded.connect(self.handle_data_loaded)
        self.model_selection_tab.modelSelected.connect(self.handle_model_selected)
        self.results_export_tab.saveResults.connect(self.save_results)

    def handle_data_loaded(self, data):
        self.loaded_data = data
        self.results_export_tab.clear_results()  # Clear previous results
        # Enable model selection tab (if it was disabled)
        self.model_selection_tab.setEnabled(True)

    def handle_model_selected(self, model_type, model_instance):
        self.selected_model_type = model_type
        self.selected_model_instance = model_instance

        # Trigger computation and display results
        self.compute_and_display_results()

    # main_window.py (updated compute_and_display_results method)

    def compute_and_display_results(self, model_type, criterion):
        if self.loaded_data is None:
            return

        try:
            # Call the appropriate model solver function based on user selections
            if model_type == "Linear Model - First":
                if criterion == "Criterion 1":
                    self.results = lm.first.criterion_1.solve(
                        self.loaded_data.get("c_list", [[]])[0],
                        self.loaded_data.get("A_list", [[]])[0],
                        self.loaded_data.get("b_list", [[]])[0],
                        1000
                    )
                elif criterion == "Criterion 2":
                    self.results = lm.first.criterion_2.solve(
                        self.loaded_data.get("c_list", [[]])[0],
                        self.loaded_data.get("A_list", [[]])[0],
                        self.loaded_data.get("b_list", [[]])[0],
                        0,  # Replace with actual z_min value
                        0.1  # Replace with actual alpha value
                    )
                elif criterion == "Criterion 3":
                    self.results = lm.first.criterion_3.solve(
                        self.loaded_data.get("c_list", [[]])[0],
                        self.loaded_data.get("A_list", [[]])[0],
                        self.loaded_data.get("b_list", [[]])[0],
                        [1] * len(self.loaded_data.get("c_list", [[]])[0])  # Replace with actual weights
                    )

            # TODO: Add similar blocks for other models and criteria
            elif model_type == "Linear Model - Second":
                if criterion == "Criterion 1":
                    self.results = lm.second.criterion_1.solve(
                        self.loaded_data.get("c_list", [[]])[0],
                        self.loaded_data.get("A_list", [[]])[0],
                        self.loaded_data.get("b_list", [[]])[0],
                        self.loaded_data.get("d_list", [[]])[0],  # Assuming d_list exists for second model
                        1000
                    )
                elif criterion == "Criterion 2":
                    self.results = lm.second.criterion_2.solve(
                        # ... (add parameters for criterion 2 of the second linear model)
                    )
                elif criterion == "Criterion 3":
                    self.results = lm.second.criterion_3.solve(
                        # ... (add parameters for criterion 3 of the second linear model)
                    )

            elif model_type == "Combinatorial Model":
                if criterion == "Criterion 1":
                    self.results = cm.first.criterion_1.solve(
                        self.loaded_data.get("processing_times", []),
                        self.loaded_data.get("precedence_graph", {}),
                        self.loaded_data.get("weights", []),
                        1000
                    )
                elif criterion == "Criterion 2":
                    self.results = cm.first.criterion_2.solve(
                        # ... (add parameters for criterion 2 of the combinatorial model)
                    )

            self.results_export_tab.display_results(self.results)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during computation: {e}")

    def save_results(self, filename):
        if self.results is None:
            QMessageBox.warning(self, "Warning", "No results to save.")
            return

        try:
            # Assuming your results can be serialized to YAML
            with open(filename, 'w') as f:
                yaml.dump(self.results, f)
            QMessageBox.information(self, "Success", f"Results saved to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving: {e}")

    def show_about_dialog(self):
        QMessageBox.about(self, "About",
                          "MMCP Data Processing Application\nVersion 1.0\n\n"
                          "Developed by: [Your Name/Team]")
