import prairielearn as pl
import sympy
import random, copy

def generate (data):
    const = random.randint(1,10)
    data['params']['const'] = const

def grade (data):
    x = sympy.symbols ('x')
    const = data['params']['const']
    ans = pl.from_json(data['submitted_answers']['symbolic_math'])
    limit_to_const = sympy.limit (ans, x, const)
    f = sympy.lambdify (x, ans)
    f_at_const = f(const)
    limit_to_const_inv = sympy.limit ((1/ans), x, const)

    continuous = True if (limit_to_const == f_at_const) else False
    limit_qualifies = True if (limit_to_const_inv == sympy.oo) else False

        
    if continuous and limit_qualifies:
        data ['score'] = 1
    else:
        data ['score'] = 0
        
        