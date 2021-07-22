import random

def generate(data):

    # Initialize variables
    m1 = random.randint(1,5)     # mass 1           (kg)
    m2 = random.randint(m1+1,10)   # mass 2           (kg)
    M = random.randint(1,10)     # mass of pulley   (kg)
    R = random.randint(1,10)     # radius of pulley (m)

    data['params']['m1'] = m1
    data['params']['m2'] = m2
    data['params']['mp'] = M
    data['params']['r'] = R

    # Physical constants
    g = 9.81   # acceleration due to gravity on Earth's surface (m/s^2)
    data['params']['g'] = g

    # Acceleration of the system, massless pulley
    # m2 > m1, pulley rotates clockwise

    # For m2 (2nd law)
    # m2*a = m2*g - T
    #    T = m2*g - m2*a

    # For m1 (2nd law)
    # m1*a = T - m1*g
    #    T = m1*g + m1*a

    # For T
    # m2*g - m2*a = m1*g + m1*a
    # m2*g - m1*g = m2*a + m1*a
    a1 = g * (m2-m1) / (m2+m1)
    data['correct_answers']['a1'] = a1

    # Acceleration of the system, pulley with mass
    
    # For m2 (2nd law)
    # m2*a = m2*g - T2
    #   T2 = m2*g - m2*a

    # For m1 (2nd law)
    # m1*a = T1 - m1*g
    #   T1 = m1*g + m1*a

    # For M (torques)
    #                         τ = Iα
    #               R*(T2 - T1) = (1/2)MR^2 * a/R
    #                   T2 - T1 = Ma/2
    # m2*g - m2*a - m1*g - m1*a = Ma/2
    #         a*(M/2 + m1 + m2) = g*(m2 - m1)
    a2 = g * (m2 - m1) / (M/2 + m1 + m2)
    data['correct_answers']['a2'] = a2