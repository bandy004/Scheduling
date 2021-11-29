import numpy as np
import random
# define data
tasks = range(1, 10)
resource_types = range(1, 1)
resources = range(1, 2)

colors = range(0, 3)

task_durations = {}
for d in tasks:
    task_durations[d] = random.randint(3, 10)

task_resource_demands = {}
for t in tasks:
    task_resource_demands[t] = {}
    for rt in resource_types:
        task_resource_demands[t][rt] = random.randint(1, 1)
task_dependency = {}
color_setup_matrix = {}
for c in colors:
    color_setup_matrix[c] = {}
    for c2 in colors:
        if c == 0 or c2 == 0 or c == c2:
            color_setup_matrix[c][c2] = 0
        else:
            color_setup_matrix[c][c2] = random.randint(7, 27)


# define variables

# define constraints

# define solver

# solve

# process result
