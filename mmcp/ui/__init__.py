# main.py:
# Sets up the main application window with three tabs using QTabWidget.
# Instantiates each tab as a separate class.
# Connects the data_loaded signal from the LoadDataTab to the handle_data_loaded slot, which then passes the data to the VisualizationTab and switches to that tab.
# ui/load_data_tab.py:
# Implements the "Load Data" tab functionality.
# Includes a button to browse for .mmcp files.
# Uses parse_mmcp_file from the data module to load the data.
# Emits the data_loaded signal when data is successfully loaded.
# Handles parsing errors with a QMessageBox.
# ui/visualization_tab.py:
# Implements the "Visualization" tab.
# Includes a label for "DMC," a dropdown for dimension selection, and a QTreeWidget for visualizing the elements.
# The set_data method populates the tree based on the loaded data.
# The open_configuration_window method (currently a placeholder) would handle opening a detailed configuration window for each element.
# ui/solution_display_tab.py:
# Implements the "Solution Display" tab.
# Uses a QTextEdit to display the solution data.
# Includes buttons for "Copy to Clipboard" and "Save to .mmcp file."
# Implements the display_solution, display_no_solution_message, copy_to_clipboard, and save_to_file methods as described in the requirements.


from .element_configuration_window import ElementConfigurationWindow
from .load_data_tab import LoadDataTab
from .solution_display_tab import SolutionDisplayTab
from .visualization_tab import VisualizationTab
