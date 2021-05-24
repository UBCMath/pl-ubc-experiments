import sympy
import random

def generate(data):
    x = sympy.symbols('x', real=True)
    n = random.randint(1, 9)

    data['params']['n'] = n

    f = sympy.Piecewise((x**2-n, x < 0), (x**2+n, x > 0))

    # answers currently hard-coded because I can't figure out how to "pl.to_json"-ify sympy integers
    # if possible, using sympy.limit?
    data['correct_answers']['lim-L'] = -n
    data['correct_answers']['lim-R'] = n