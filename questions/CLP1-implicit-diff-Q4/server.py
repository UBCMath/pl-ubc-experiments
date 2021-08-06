import prairielearn as pl
from sympy import symbols, var, exp, idiff, simplify, Eq
import random

def generate(data):

    a = random.randint(2, 9)
    b = random.randint(2, 9)
    c = random.randint(2, 9)
    d = random.randint(1, 30)

    data['params']['a'] = a
    data['params']['b'] = b
    data['params']['c'] = c
    data['params']['d'] = d
    
    var('a b c d')
    x = symbols('x',real=True)
    y = symbols('y',real=True)
    
    q_lhs = a*x*y + exp(b*x) + exp(c*y)
    manual_ans = -(b*exp(b*x)+a*y)/(a*x+c*exp(c*y))
    sympy_ans = idiff(q_lhs,y,x)
    
    #checks if manual and sympy computed answers are the same
    assert (simplify(Eq (sympy_ans, manual_ans)))

    data['correct_answers']['ans'] = pl.to_json(manual_ans)