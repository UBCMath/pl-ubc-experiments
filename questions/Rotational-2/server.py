from random import randint
import numpy as np

def generate(data):

    # initialize variables
    can = randint(20, 30)         # mass of can (g)
    pineapple = randint(600, 900) # mass of pineapple (g)
    d = randint(100, 200)         # hypotenuse slope surface (cm)
    theta = randint(10, 30)       # angle of slope (degrees)

    data['params']['m_can'] = can
    data['params']['m_pa'] = pineapple
    data['params']['d'] = d
    data['params']['theta'] = theta

    # physical constants
    g = 9.81 # acceleration due to gravity at Earth's surface (m/s^2)

    # calculated quantities
    theta *= np.pi / 180.0 # convert to radians
    d /= 100.0
    h = d * np.sin(theta)
    v_hollow = np.sqrt(g*h)
    v_solid = np.sqrt(4/3*g*h)

    data['correct_answers']['v_empty'] = v_hollow
    data['correct_answers']['v_unopened'] = v_solid
