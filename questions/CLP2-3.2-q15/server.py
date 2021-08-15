from random import randint

def generate(data):
    
    a = randint(2, 7)
    b = randint(2, 9)
    k = randint(4, 8)

    data['params']['a'] = a
    data['params']['b'] = b
    data['params']['k'] = k

    data['params']['a2'] = a**2
    data['params']['a3'] = a**3
    data['params']['a4'] = a**4

    # Geometric series, r = 1/a
    s1 = 1 / (1 - 1/a)
    # Geometric series, r = 1/b
    # Factor out 1/b**k
    s2 = 1 / (b**k) / (1 - 1/b)

    data['correct_answers']['s1'] = s1
    data['correct_answers']['s2'] = s2
    
    