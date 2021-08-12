import prairielearn as pl
from sympy import symbols, integrate, atan
import random

def generate(data):
    x = symbols('x')
    C = symbols('C')
    n = random.randint(3, 9)

    data['params']['n'] = n

    I = integrate(x**2*atan(n*x), x) + C

    data['correct_answers']['I'] = pl.to_json(I)