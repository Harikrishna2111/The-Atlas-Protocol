import random


# Variables to store the count of specific components collected
component_count_holder = [ 0, 0, 0, 0, 0, 0]

# Weights for corresponding components
component_weights =  [0.4, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

def component_selector():
    return random.choices([0, 1, 2, 3, 4, 5, 6], 
    weights=component_weights)[0]