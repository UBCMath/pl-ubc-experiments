import prairielearn as pl
import sympy
import random

def generate(data):
    x = sympy.symbols("x")
    C = sympy.symbols("C")
    n = random.randint(1, 5)
    
    data["params"]["n"] = n

    I = sympy.integrate(n/(x**3-1), x) + C

    data["correct_answers"]["integral"] = pl.to_json(I)
