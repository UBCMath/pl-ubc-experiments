import prairielearn as pl
import sympy
import random, copy

def generate(data):
    # create random integers between 5 and 10 (inclusive)
    a = random.randint(5, 10)
    b = random.randint(5, 10)

    data['params']['a'] = a
    data['params']['b'] = b

    sympy.var('x')

    data['correct_answers']['sin'] = pl.to_json(sympy.diff(sympy.sin(x**2), x, 2))
    data['correct_answers']['cos'] = pl.to_json(sympy.diff(sympy.cos(sympy.sqrt(x)), x, 2))
    data['correct_answers']['frac'] = pl.to_json(sympy.diff(1/(x+1)**5, x, 2))
    
