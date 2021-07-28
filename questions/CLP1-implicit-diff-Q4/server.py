import prairielearn as pl
import sympy as s
import random, copy

def generate(data):

    a = random.randint(2, 9)
    b = random.randint(2, 9)
    c = random.randint(2, 9)
    d = random.randint(1, 30)

    data['params']['a'] = a
    data['params']['b'] = b
    data['params']['c'] = c
    data['params']['d'] = d
    
    s.var('a b c d')
    x = s.symbols('x',real=True)
    y = s.symbols('y',real=True)
    
    q_lhs = a*x*y + s.exp(b*x) + s.exp(c*y)
    manual_ans = -(b*s.exp(b*x)+a*y)/(a*x+c*s.exp(c*y))
    sympy_ans = s.idiff(q_lhs,y,x)
    
    #checks if manual and sympy computed answers are the same
    assert (s.simplify(s.Eq (sympy_ans, manual_ans)))

    data['correct_answers']['ans'] = pl.to_json(manual_ans)