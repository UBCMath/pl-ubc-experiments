import prairielearn as pl
import sympy as sp
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
    
    sp.var('a b c d')
    x = sp.symbols('x',real=True)
    y = sp.symbols('y',real=True)
    
    q_lhs = a*x*y + sp.exp(b*x) + sp.exp(c*y)
    manual_ans = -(b*sp.exp(b*x)+a*y)/(a*x+c*sp.exp(c*y))
    sympy_ans = sp.idiff(q_lhs,y,x)
    
    #checks if manual and sympy computed answers are the same
    assert (sp.simplify(sp.Eq (sympy_ans, manual_ans)))

    data['correct_answers']['ans'] = pl.to_json(manual_ans)