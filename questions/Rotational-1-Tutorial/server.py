import random
from sympy import Symbol, Rational
import prairielearn as pl

def generate(data):

    # Initialize variables
    v0 = random.randint(1, 7)               # initial velocity (m/s)
    m = random.randint(1, 8)                # ball mass (kg)
    r = random.randint(1, 4)                # ball radius (m)
    mu = random.randint(1, 8) / 10          # coefficient of friction

    data['params']['v0'] = "{:.2f}".format(v0)
    data['params']['m'] = "{:.2f}".format(m)
    data['params']['r'] = "{:.2f}".format(r)
    data['params']['mu'] = "{:.3f}".format(mu)

    # Physical constants
    g = 9.81 # acceleration due to gravity at Earth's surface (m/s^2)

    data['params']['g'] = g

    # Answers
    t_value = (2 * v0) / (7 * mu * g)
    
    g = Rational(str(g)) # swapping over to rationals for ease of calculation
    mu = Rational(str(mu))

    t = Symbol('t') # for the two velocities written as a function of time
    v = v0 - mu * g * t
    omega = Rational(5 * mu * g, 2 * r) * t

    data['correct_answers']['t'] = t_value
    data['correct_answers']['v'] = pl.to_json(v)
    data['correct_answers']['omega'] = pl.to_json(omega)
