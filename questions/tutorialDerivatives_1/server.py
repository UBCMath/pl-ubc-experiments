import prairielearn as pl
import sympy
import random, copy

def generate(data):
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    c = random.randint(1, 9)
    sympy.var('a b c x')
    ind = [sympy.sin(a*x**2), sympy.cos(b*x), (c/(x+1)**5)]


    choose_one = pl.to_json(random.choices (ind, k =1) [0])

    data['params']['a'] = a
    data['params']['b'] = b
    data['params']['c'] = c

    #only displays the randomly selected question 
    data['params']['display_this'] = sympy.latex(pl.from_json(choose_one))

    data['correct_answers']['ans'] = pl.to_json(sympy.diff(pl.from_json(choose_one),x,2))
    
