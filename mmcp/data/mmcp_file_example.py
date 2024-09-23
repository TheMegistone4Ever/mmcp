import numpy as np
import yaml


def generate_mmcp_file(filename, num_elements=5, num_vars=50, num_jobs=50):
    """Generates an example MMCF file (YAML wrapper) with synthetic data."""

    data = {}

    # Linear Model Data
    data['c_list'] = [np.random.rand(num_vars).tolist() for _ in range(num_elements)]
    data['A_list'] = [np.random.rand(num_vars, num_vars).tolist() for _ in range(num_elements)]
    data['b_list'] = [np.random.rand(num_vars).tolist() for _ in range(num_elements)]
    data['d_list'] = [np.random.rand(num_vars).tolist() if np.random.rand() < 0.5 else None for _ in
                      range(num_elements)]
    data['model_types'] = [1 if data['d_list'][i] is not None else 2 for i in range(num_elements)]

    # Combinatorial Model Data
    data['processing_times'] = np.random.randint(1, 10, size=num_jobs).tolist()
    precedence_graph = {}
    for j in range(1, num_jobs):
        num_predecessors = np.random.randint(0, min(j, 5))
        predecessors = np.random.choice(np.arange(j), size=num_predecessors, replace=False).tolist()
        precedence_graph[j] = predecessors
    data['weights'] = np.random.rand(num_jobs).tolist()
    data['precedence_graph'] = precedence_graph

    # Write data to YAML file
    with open(filename, 'w') as f:
        yaml.dump(data, f)


# Example usage:
if __name__ == "__main__":
    generate_mmcp_file("../ui/example.mmcp")
