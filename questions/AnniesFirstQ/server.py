import prairielearn as pl
import sympy
import random, copy

def generate(data):
    # create random integers between 5 and 10 (inclusive)
    a = random.randint(5, 10)
    b = random.randint(5, 10)

    data['params']['a'] = a
    data['params']['b'] = b

    sympy.var('a b x')
    z = a*sympy.sin(x)+b*sympy.cos(x)
    data['correct_answers']['symbolic_math'] = pl.to_json(z)
    
