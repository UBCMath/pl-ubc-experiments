import numpy
import random

def generate(data):

    # Initialize variables
    I = random.randint(1,15)       # current  (A)
    R = random.randint(1,4)        # radius   (m)
    x = random.randint(5,30)       # distance (m)
    v = random.randint(4,8)        # velocity (10e6 m/s)

    data['params']['I'] = I
    data['params']['R'] = R
    data['params']['x'] = x
    data['params']['v'] = v

    # Physical constants
    mu_0 = 4 * numpy.pi * 10e-7 # vacuum permeability (H/m)
    q = 1.60217662 * 10e-19     # elementary charge   (C)

    # Magnetic field strength at P
    # Derivation:
    # dB = (μ0/4π) * (I dl × r_hat / r^2)
    #     r = hypotenuse, r_hat = x-component
    # dB = (μ0/4π) * (I dl × (R / sqrt(x^2+R^2)) / (x^2 + R^2))
    #     Path integrate, across loop of circumference = 2πR
    # B = 2πμ0IR^2 / 4π(R^2+x^2)^(3/2)
    B_P = mu_0 * I * R**2 / 2 / (R**2 + x**2)**1.5
    data['correct_answers']['B_P'] = B_P

    # Magnetic field strength at 0
    # Strongest, due to cross product being 90°
    # Evaluate the above expression at 0
    # B = μ0IR^2 / 2R^3
    B = mu_0 * I / 2 / R
    data['correct_answers']['B_max'] = B

    # Force on electron
    # F = qv × B
    F = q * v * 10e6 * B_P
    data['correct_answers']['F'] = F