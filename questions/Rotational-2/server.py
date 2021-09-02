from random import randint
import numpy as np

def generate(data):

    # initialize variables
    cyl = randint(200, 400)         # mass of cylinder (g)
    d = randint(100, 200)         # hypotenuse slope surface (cm)
    theta = randint(10, 30)       # angle of slope (degrees)

    data['params']['m_cyl'] = cyl
    data['params']['d'] = d
    data['params']['theta'] = theta

    # physical constants
    g = 9.81 # acceleration due to gravity at Earth's surface (m/s^2)

    # calculated quantities
    theta *= np.pi / 180.0 # convert to radians
    d /= 100.0             # convert to meters
    h = d * np.sin(theta)
    v_hollow = np.sqrt(g*h)
    v_solid = np.sqrt(4/3*g*h)

    data['correct_answers']['v_metal'] = v_hollow
    data['correct_answers']['v_wood'] = v_solid
