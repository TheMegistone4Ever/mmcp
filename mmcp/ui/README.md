# MMCP Data Processing UI

This PyQt5 interface provides a user-friendly way to process data from MMCF files using various models defined in your
project.

## Integration with Existing Project

1. **Place this script (`ui.py`) in your project directory.**
2. **Ensure the necessary imports are correct.** You might need to adjust import paths based on your project structure (
   e.g., `from mmcp.data import mmcp_parser`).

## Running the Interface

1. **Install PyQt5:** If you don't have PyQt5 installed, use pip:
   ```bash
   pip install PyQt5
   ```
2. **Run the script:**
   ```bash
   python ui.py 
   ```

## Dependencies

- PyQt5
- Your existing project modules (e.g., `mmcp_parser`, `linear_models`, `combinatorial_models`)

## Usage

1. **Data Loading:** Load an MMCF file using the "Browse" button.
2. **Model Selection:** Select a model type and a specific model instance from the tree view.
3. **Results & Export:**
    - View the computed results in the table.
    - Save the results to an MMCF file using the "Save" button.
    - Copy the results to the clipboard using the "Copy to Clipboard" button.

## Notes

- The `README` provides basic instructions. You can expand it with more specific details about your project and models.
- The UI is designed to be flexible. You can easily add more models and functionality by extending the
  `ModelSelectionTab` and `ResultsExportTab` classes.
- Ensure that the parser logic (`mmcp_parser`) and model solver functions in your project are correctly implemented.
- Implement the clipboard copying logic in `ResultsExportTab.copy_results_to_clipboard`.
- Add detailed model descriptions in `ModelSelectionTab.handle_model_tree_click`.
- Consider adding input validation and more robust error handling as needed.
