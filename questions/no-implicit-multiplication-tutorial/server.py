import prairielearn as pl
from sympy import cos, latex, Symbol
import random

def generate(data):
    a = random.randint(5, 10)  # inclusive

    x = Symbol('x')
    
    data['params']['a'] = a
    data['params']['formula'] = latex(a*cos(a*x))
    data['correct_answers']['sym_1'] = pl.to_json(a*cos(a*x))

    
