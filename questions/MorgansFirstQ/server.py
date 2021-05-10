import prairielearn as pl
import sympy
import random

def generate(data):
    x = sympy.symbols("x")
    n = random.randint(1, 5)
    
    data["params"]["n"] = n

    I = sympy.integrate(n/(x**3-1), x)

    data["correct_answers"]["integral"] = pl.to_json(I)
