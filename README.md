# MMCP: Multi-Model Combinatorial Problem Solver

This project provides a framework and implementations for solving Multi-Model Combinatorial Problems (MMCPs). Which are
optimization problems involving a two-level hierarchical structure, where the higher level (center) coordinates the
actions of lower-level elements, each potentially employing a different optimization model.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Models and Criteria](#models-and-criteria)
    - [Linear Models](#linear-models)
    - [Combinatorial Model](#combinatorial-model)
    - [Connected Model](#connected-model)
- [Data Generation](#data-generation)
- [MMCP File Format](#mmcp-file-format)
- [Graphical User Interface](#graphical-user-interface)
- [License](#license)

## Introduction

MMCPs arise in various domains, including production planning, resource allocation, and scheduling. This project aims to
provide a flexible and extensible framework for solving such problems by supporting different models for individual
elements and offering a range of compromise criteria to guide the coordination by the center.

## Features

- **Multiple Models:** Supports different optimization models for individual elements, including linear and
  combinatorial models.
- **Compromise Criteria:** Implements a variety of compromise criteria to balance the goals of the center and the
  individual elements.
- **Data Generation:** Includes functions for generating synthetic MMCP instances for testing and experimentation.
- **MMCP File Parser:** Defines a standardized file format for representing MMCP instances and provides a parser for
  loading data from these files.
- **Graphical User Interface (GUI):** Offers a PyQt5-based GUI for loading, visualizing, and solving MMCP instances.

## Project Structure

The project has the following structure (simplified, showing only relevant directories and files):

```
mmcp/
├── combinatorial_models/
│   └── first/
│       ├── criterion_1.py
│       └── criterion_2.py
├── data/
│   ├── data_generation.py
│   ├── mmcp_file_generation.py 
│   └── mmcp_file_parser.py
├── linear_models/
│   ├── first/
│   │   ├── criterion_1.py
│   │   ├── criterion_2.py
│   │   └── criterion_3.py
│   ├── second/
│   │   ├── criterion_1.py
│   │   ├── criterion_2.py
│   │   └── criterion_3.py
│   └── third/
│       └── connected_model.py 
├── ui/
│   ├── element_configuration_window.py
│   ├── load_data_tab.py
│   ├── main_ui.py
│   ├── README.md  
│   ├── solution_display_tab.py
│   └── visualization_tab.py
└── utils/
    └── config.py

```

## Models and Criteria

### Linear Models

The project supports three types of linear models for individual elements:

- **Linear Model 1:**
    - Objective: `c^T * x`
    - Constraints: `A * x <= b`, `x >= 0`
- **Linear Model 2:**
    - Objective: `c^T * x`
    - Constraints: `A * x <= b`, `x >= d`
- **Linear Model 3:**
    - A combination of Linear Model 1 and Linear Model 2, as defined in `connected_model.py`.

Each linear model can be solved using different compromise criteria, including:

- **Criterion 1:** Minimizes the weighted sum of deviations from the individual element's optimal objective values.
- **Criterion 2:** Minimizes the center's objective while ensuring that each element's goal is within a specified
  range of its optimal value.
- **Criterion 3:** A generalization of Criterion 2 with more flexible constraints on the individual element's objective
  values.

### Combinatorial Model

The combinatorial model represents a scheduling problem where jobs need to be assigned to a single machine with
precedence constraints:

- Objective: Minimize the weighted sum of completion times.
- Constraints: Precedence constraints represented by a directed acyclic graph.

The combinatorial model can be solved using different compromise criteria, including:

- **Criterion 1:** Minimizes the center's objective while ensuring that each element's goal is within a specified
  range of its optimal value.
- **Criterion 2:** A generalization of Criterion 1 with more flexible constraints on the individual element's objective
  values.

### Connected Model

The connected model, implemented in `connected_model.py`, represents a scenario where the elements are interconnected,
and their decisions affect each other. It is a specific type of Linear Model 3.

## Data Generation

The project includes functions for generating synthetic MMCP instances:

- `generate_linear_model_data()`: Generates data for linear models, including cost vectors, constraint matrices, and
  model types.
- `generate_combinatorial_model_data()`: Generates data for the combinatorial model, including processing times,
  precedence graphs, and weights.
- `mmcp_file_generation.py`: Contains code for generating example .mmcp files.

## MMCP File Format

MMCP instances can be stored in `.mmcp` files, which are YAML files with a specific structure. See the documentation for
the `mmcp.data` module, specifically `mmcp_file_parser.py` for details on the file format. An example file (
`example.mmcp`) is provided in the `ui` directory.

## Graphical User Interface

The project includes a PyQt5-based GUI for loading, visualizing, and solving MMCP instances. For details on the GUI's
features and usage, refer to the [GUI README](mmcp/ui/README.md).

## License

This project is licensed under
the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](LICENSE.md).

## Getting Started

1. Clone the repository: `git clone <repository_url>`
2. Install the dependencies: `pip install -r requirements.txt`
3. Run the main application: `python main_ui.py` (for the GUI) or `python main.py` (for the command-line interface).
4. Explore the different models, criteria, and data generation functions.
5. Refer to the documentation in the code and the respective README files for more detailed information.
