from random import randint
from sympy import Symbol, Eq, factor, latex

def generate(data):

    # initialize variables
    a = randint(1, 9)
    b = randint(1, 9)
    c = randint(1, 9)

    data['params']['c'] = c

    # For f(x) to be continuous, left and right must be equal at c
    # Substitute in c for x:
    # c^2 + k = a * (c - b)
    #       k = a * (c - b) - c^2
    k_ans = a * (c - b) - c**2

    data['correct_answers']['k'] = k_ans

    # generate functions
    x = Symbol('x', real=True)
    k = Symbol('k', real=True)

    f_l = x**2 + k
    f_r = factor(a * (x - b))
    l = f_l.subs(x, c).subs(k, k_ans)
    r = f_r.subs(x, c).subs(k, k_ans)
    
    assert Eq(l, r)

    data['params']['f_r'] = latex(f_r)
