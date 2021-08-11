import prairielearn as pl
from sympy import Symbol, limit, oo, Eq, lambdify
import random, copy

def generate (data):
    const = random.randint(1,10)
    data['params']['const'] = const
    

def grade (data):
    x = Symbol('x', real=True)
    const = data['params']['const']
    ans = pl.from_json(data['submitted_answers']['symbolic_math'])
    limit_qualifies = ((limit ((1/ans), x, const,'-') == oo) and (limit ((1/ans), x, const,'+') == oo))
    
    if limit_qualifies:
        limit_to_const = limit (ans, x, const)
        f_at_const = ans.subs (x, const)

        if (limit_to_const == f_at_const):
            data ['score'] = 1
        else:
            data ['score'] = 0
    else: 
        data ['score'] = 0

        