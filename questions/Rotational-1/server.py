import random

def generate(data):

    # Initialize variables
    v0 = round(random.uniform(1.0, 7.0), 2) # initial velocity (m/s)
    m = random.randint(1, 8)                # ball mass (kg)
    r = round(random.uniform(1.0, 4.0), 2)  # ball radius (m)
    mu = round(random.uniform(0.1, 0.8), 3) # coefficient of friction

    data['params']['v0'] = v0
    data['params']['m'] = m
    data['params']['r'] = r
    data['params']['mu'] = mu

    # Physical constants
    g = 9.81 # acceleration due to gravity at Earth's surface (m/s^2)

    data['params']['g'] = g

    # Answers
    t_value = (2 * v0) / (7 * mu * g)
    
    data['correct_answers']['t'] = t_value
