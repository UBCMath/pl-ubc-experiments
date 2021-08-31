import prairielearn as pl
from sympy import cos, latex, var
import random

def generate(data):
    # create a random integer between 5 and 10 (inclusive)
    a = random.randint(5, 10)

    var('x')
    
    data['params']['a'] = a
    data['params']['formula'] = latex(a*cos(a*x))
    data['correct_answers']['sym_1'] = pl.to_json(a*cos(a*x))

    
