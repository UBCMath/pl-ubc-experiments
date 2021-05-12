import prairielearn as pl
import sympy
import random

def generate(data):
    x = sympy.symbols('x')
    C = sympy.symbols('C')
    n = random.randint(3, 9)

    data['params']['n'] = n

    I = sympy.integrate(x**2*sympy.atan(n*x), x) + C

    data['correct_answers']['I'] = pl.to_json(I)