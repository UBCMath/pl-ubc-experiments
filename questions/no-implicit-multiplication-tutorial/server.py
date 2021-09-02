import prairielearn as pl
from sympy import cos, latex, Symbol, pretty
import random

def generate(data):
    a = random.randint(5, 10)  # inclusive

    x = Symbol('x')
    f = a*cos(a*x)

    data['params']['a'] = a
    data['params']['formula'] = latex(f)
    # make an implicit multiplication string: 4cos(4x)
    data['params']['str_formula'] = pretty(f, use_unicode=False).replace("*", "")
    data['correct_answers']['sym_1'] = pl.to_json(f)
