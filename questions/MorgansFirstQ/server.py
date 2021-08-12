import prairielearn as pl
from sympy import symbols, integrate
import random

def generate(data):
    x = symbols("x")
    C = symbols("C")
    n = random.randint(1, 5)
    
    data["params"]["n"] = n

    I = integrate(n/(x**3-1), x) + C

    data["correct_answers"]["integral"] = pl.to_json(I)
