import prairielearn as pl
import sympy
import random, copy

def generate(data):
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    c = random.randint(1, 10)
    ind = ['display_a', 'display_b', 'display_c']

    to_true = random.choices (ind, k =1) [0]
    sympy.var('a b c x')
    q_and_a = {
        'display_a' : pl.to_json(sympy.diff(sympy.sin(a*x**2), x, 2)),
        'display_b' : pl.to_json(sympy.diff(sympy.cos(sympy.sqrt(b*x)), x, 2)),
        'display_c' : pl.to_json(sympy.diff(c/(x+1)**5, x, 2))
    }

    data['params']['a'] = a
    data['params']['b'] = b
    data['params']['c'] = c

    data['params']['display_a'] = False
    data['params']['display_b'] = False
    data['params']['display_c'] = False
    #only displays the randomly selected answer 
    data['params'][to_true] = True

    data['correct_answers']['ans'] = q_and_a[to_true]
    
