import prairielearn as pl
import sympy
import random, copy

def generate(data):
        # Sample two random integers between 5 and 10 (inclusive)
    a = random.randint(5, 10)
    b = random.randint(5, 10)
    c = random.randint(5, 10)
    d = random.randint(5, 10)

    data['params']['a'] = a
    data['params']['b'] = b
    data['params']['c'] = c
    data['params']['d'] = d

    sympy.var('a b x')
    z = a*sympy.sin(x)+b*sympy.cos(x)
    data['correct_answers']['symbolic_math'] = pl.to_json(z)
    
