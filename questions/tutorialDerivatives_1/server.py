import prairielearn as pl
import sympy
import random, copy

def generate(data):
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    c = random.randint(1, 10)


    data['params']['a'] = a
    data['params']['b'] = b
    data['params']['c'] = c

    sympy.var('a b c x')

    data['correct_answers']['sin'] = pl.to_json(sympy.diff(sympy.sin(a*x**2), x, 2))
    data['correct_answers']['cos'] = pl.to_json(sympy.diff(sympy.cos(sympy.sqrt(b*x)), x, 2))
    data['correct_answers']['frac'] = pl.to_json(sympy.diff(c/(x+1)**5, x, 2))
    
