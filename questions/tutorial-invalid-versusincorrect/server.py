import prairielearn as pl
from sympy import symbols, Rational
import random
import math

def generate(data):
    a = random.choice([9, 11, 13, 15])
    b = 2

    data['params']['a'] = a
    data['params']['b'] = b

    x = symbols('x')

    q = Rational(a, b)
    # .round has round-to-even behaviour, then convert to ‘int‘
    n = int(Rational(a, b).round())

    data['correct_answers']['num'] = a/b
    data['correct_answers']['num_f'] = a/b
    data['correct_answers']['int_value'] = n
    data['correct_answers']['sym'] = pl.to_json(q)
