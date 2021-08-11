import prairielearn as pl
from sympy import symbols, simplify
import random, copy

def generate (data):
    b = random.randint(2,4)
    vary = random.randint(1,10)
    arr = ["half", "a third", "a quarter"]
    scale = arr [b-2] 

    data['params']['scale'] = scale
    data['params']['vary'] = vary
    H = symbols("H")
    y = symbols("y")
    A = symbols("A")
    c = symbols("c")
    g = symbols("g")
    z = simplify(0)
    
    ans = simplify(g*A*(vary+c*(H/b-y))*(H-y))
    data['correct_answers']['symbolic_math'] = pl.to_json(ans)
    data['correct_answers']['c3'] = pl.to_json(H/b)
    data['correct_answers']['c4'] = pl.to_json(z)
    
    
