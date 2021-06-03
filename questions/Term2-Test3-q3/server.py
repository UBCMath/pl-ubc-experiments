import prairielearn as pl
import sympy
import random, copy

def generate (data):
    b = random.randint(2,4)
    vary = random.randint(1,10)
    arr = ["half", "a third", "a quarter"]
    scale = arr [b-2] 

    data['params']['scale'] = scale
    data['params']['vary'] = vary
    H = sympy.symbols("H")
    y = sympy.symbols("y")
    A = sympy.symbols("A")
    c = sympy.symbols("c")
    g = sympy.symbols("g")
    z = sympy.simplify(0)
    
    ans = sympy.simplify(g*A*(vary+c*(H/b-y))*(H-y))
    data['correct_answers']['symbolic_math'] = pl.to_json(ans)
    data['correct_answers']['c3'] = pl.to_json(H/b)
    data['correct_answers']['c4'] = pl.to_json(z)
    
    
