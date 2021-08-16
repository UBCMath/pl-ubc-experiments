import prairielearn as pl
from sympy import symbols, Rational
import random

def generate(data):
    a = random.choices ([9,11,13,15])[0]
    b = 2
    
    data['params']['a'] = a
    data['params']['b'] = b
    
    x = symbols('x')
    
    data['correct_answers']['num'] = a/b
    data['correct_answers']['int_value'] = round(a/b)
    data['correct_answers']['sym'] = pl.to_json(Rational(a/b))

    
