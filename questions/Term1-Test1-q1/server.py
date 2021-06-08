import prairielearn as pl
from sympy import *
import random, copy

def generate (data):
    const = random.randint(1,10)
    data['params']['const'] = const

def grade (data):
    x = symbols ('x')
    const = data['params']['const']
    ans = pl.from_json(data['submitted_answers']['symbolic_math'])
    limit_to_const = limit (ans, x, const)
    f = lambdify (x, ans)
    f_at_const = f(const)
    limit_to_const_inv = limit ((1/ans), x, const)

    continuous = True if (limit_to_const == f_at_const) else False
    limit_qualifies = True if (limit_to_const_inv == oo) else False

        
    if continuous and limit_qualifies:
        data ['score'] = 1
    else:
        data ['score'] = 0
        
        