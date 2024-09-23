# MMCP Data Processing and Optimization UI

This PyQt5-based graphical user interface (GUI) provides a user-friendly environment for loading, visualizing, and
optimizing data from MMCP (Multi-Model Combinatorial Problem) files. The GUI integrates various optimization models and
allows users to configure and solve MMCP instances, displaying the results in an intuitive manner.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
    - [Loading Data](#loading-data)
    - [Visualizing the Problem](#visualizing-the-problem)
    - [Configuring Element Models and Criteria](#configuring-element-models-and-criteria)
    - [Solving the MMCP Instance](#solving-the-mmcp-instance)
    - [Viewing and Exporting Solutions](#viewing-and-exporting-solutions)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Future Development](#future-development)

## Introduction

The MMCP Data Processing and Optimization UI aims to simplify the process of working with MMCP instances.
It offers a visual representation of the problem structure, allows users to select and configure different optimization
models for each element, and provides tools for solving the problem and analyzing the solutions.

## Features

- **Data Loading:** Loads MMCP data from `.mmcp` files.
- **Visualization:** Displays the elements of the MMCP instance in a tree-like structure, showing the associated data
  for each element.
- **Model Selection:** Allows users to choose between different optimization models (e.g., Linear Model 1, Linear Model
  2, Combinatorial Model) for each element.
- **Criterion Selection:** Enables users to select the optimization criterion (e.g., Criterion 1, Criterion 2,
- Criterion 3) for each element based on the chosen model.
- **Solution Display:** Presents the computed solutions for each element in a formatted text area.
- **Solution Export:** Provides options to copy the solution to the clipboard or save it to a file.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   ```
2. **Navigate to the project directory:**
   ```bash
   cd <project_directory>
   ```
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Loading Data

1. Launch the application.
2. Navigate to the "Load Data" tab.
3. Click the "Browse" button to select the `.mmcp` file containing the MMCP data.
4. The application will parse the file and display the elements in the "Visualization" tab.

### Visualizing the Problem

The "Visualization" tab displays the elements of the MMCP instance in a hierarchical tree view.
Each element can be expanded to reveal its associated data (e.g., cost vectors, constraint matrices, etc.).

### Configuring Element Models and Criteria

1. Right-click on an element in the tree view.
2. A context menu will appear, allowing you to choose the desired optimization model for that element.
3. After selecting the model, a configuration window will open, where you can further customize the model parameters and
   select the optimization criterion.
4. Click "OK" to save the configuration.

### Solving the MMCP Instance

1. Once the models and criteria are configured for all elements, click the "Solve" button in the "Visualization" tab.
2. The application will apply the selected models and criteria to solve the MMCP instance.
3. The solutions for each element will be displayed in the "Solution Display" tab.

### Viewing and Exporting Solutions

The "Solution Display" tab presents the computed solutions in a formatted text area. You can:

- **Copy to Clipboard:** Click the "Copy to Clipboard" button to copy the solution text.
- **Save to File:** Click the "Save to .mmcp file" button to save the solution to a file.

## Project Structure

The project is organized as follows:

- `__init__.py`: Initializes the package.
- `element_configuration_window.py`: Defines the configuration window for element models and criteria.
- `load_data_tab.py`: Implements the "Load Data" tab.
- `main.py`: Contains the main application window.
- `solution_display_tab.py`: Implements the "Solution Display" tab.
- `visualization_tab.py`: Implements the "Visualization" tab.
- `README.md`: This README file.

## Dependencies

- PyQt5
- mmcp (Your existing project modules containing the MMCP data parser and optimization models)

## Future Development

- Enhance the visualization with graphical representations of the MMCP structure.
- Implement more optimization models and criteria.
- Add support for different input and output formats.
- Improve error handling and user feedback.
