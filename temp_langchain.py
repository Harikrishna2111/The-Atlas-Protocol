import random
def ai(prompt):
    return 'response'

def component_selector():
    return random.choices([0, 1, 2, 3, 4, 5, 6], weights=[0.5, 0.1, 0.15, 0.13, 0.01, 0.105, 0.005])[0]
