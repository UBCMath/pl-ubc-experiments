import prairielearn as pl
from sympy import symbols, var, exp, idiff, simplify, Eq, cos, sin, latex, integrate
import random

def generate(data):
    a = random.randint(2,9)
    var ('a C')
    x = symbols('x',real=True)
    
    q_equation = a*exp(cos(x))*sin(2*x)
    
    data ['params']['q_equation'] = latex (q_equation)
    
    manual_ans = 2*a*exp(cos(x))*(1-cos(x))
    sympy_ans = integrate (q_equation,x)

    #checks if manual and sympy computed answers are the same
    assert (simplify(Eq (sympy_ans, manual_ans)))

    data ['correct_answers']['ans'] = pl.to_json (sympy_ans + C)










