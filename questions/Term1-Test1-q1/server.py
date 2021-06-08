import prairielearn as pl
import sympy
import random, copy
from sympy.calculus.util import continuous_domain

def generate (data):
    const = random.randint(1,10)
    data['params']['const'] = const

def grade (data):
    x = sympy.symbols ('x')
    const = data['params']['const']
    ans = pl.from_json(data['submitted_answers']['symbolic_math'])
    limit_qualifies = ((sympy.limit ((1/ans), x, const,'-') == sympy.oo) and (sympy.limit ((1/ans), x, const,'+') == sympy.oo))
    if limit_qualifies:
        limit_to_const = sympy.limit (ans, x, const)
        f = sympy.lambdify (x, ans)
        f_at_const = f(const)
        if (limit_to_const == f_at_const):
            data ['score'] = 1
        else:
            data ['score'] = 0
    else: 
        data ['score'] = 0

        