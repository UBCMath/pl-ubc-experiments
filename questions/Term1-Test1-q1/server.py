import prairielearn as pl
from sympy import symbols, limit, oo
import random

def generate (data):
    const = random.randint(1,10)
    data['params']['const'] = const

def grade (data):
    x = symbols ('x')
    const = data['params']['const']
    # stores valid student answer into ans
    ans = pl.from_json(data['submitted_answers']['symbolic_math'])
    # checks whether the second condition is satisfied
    limit_qualifies = ((limit ((1/ans), x, const,'-') == oo) and (limit ((1/ans), x, const,'+') == oo))
    if limit_qualifies:
        limit_to_const = limit (ans, x, const)
        f_at_const = ans.subs (x, const)
        
        # checks whether or not function is continous at x = const
        if (limit_to_const == f_at_const):
            data ['score'] = 1
        else:
            data ['score'] = 0
    else: 
        data ['score'] = 0

        