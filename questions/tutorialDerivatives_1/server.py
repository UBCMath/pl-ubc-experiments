import prairielearn as pl
import sympy
import random, copy

def generate(data):
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    c = random.randint(1, 9)
    sympy.var('a b c x')
    ind = [pl.to_json(sympy.sin(a*x**2)), pl.to_json(sympy.cos(b*x)), pl.to_json((c/(x+1)**5)) ]


    to_true = random.choices (ind, k =1) [0]

    data['params']['a'] = a
    data['params']['b'] = b
    data['params']['c'] = c

    #only displays the randomly selected question 
    data['params']['display_this'] = sympy.latex(pl.from_json(to_true))

    data['correct_answers']['ans'] = pl.to_json(sympy.diff(pl.from_json(to_true),x,2))
    
