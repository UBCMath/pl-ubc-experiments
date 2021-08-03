import prairielearn as pl
from sympy import var, symbols, sin, cos, latex, diff, simplify, Eq
import random, copy

def generate(data):
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    c = random.randint(1, 9)
    var('a b c')
    x = symbols('x',real=True)
    
    q_arr = [sin(a*x**2), cos(b*x), (c/(x+1)**5)]
    manual_ans_arr = [-sin(a*x**2)*4*a**2*x**2+cos(a*x**2)*2*a,-b**2*cos(b*x), (30*c)/(x+1)**7]
    
    #randomly selects 0, 1, or 2 representing the selected index
    index_to_choose = random.randint(0,2)


    selected_q = q_arr[index_to_choose]
    selected_ans = manual_ans_arr [index_to_choose]
    
    data['params']['a'] = a
    data['params']['b'] = b
    data['params']['c'] = c

    #only displays the randomly selected question 
    data['params']['display_this'] = latex(selected_q)
    
    sympy_compute_ans = diff(selected_q,x,2)
    
    #checks whether sympy and manual computed answers match or not, if not error is raised to display the selected question
    assert simplify (Eq (selected_ans,sympy_compute_ans)),selected_q

    data['correct_answers']['ans'] = pl.to_json(sympy_compute_ans)
    
