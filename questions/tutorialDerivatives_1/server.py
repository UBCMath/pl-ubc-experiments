import prairielearn as pl
import sympy
import random, copy

def generate(data):
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    c = random.randint(1, 9)
    sympy.var('a b c')
    x = sympy.symbols('x',real=True)
    
    q_arr = [sympy.sin(a*x**2), sympy.cos(b*x), (c/(x+1)**5)]
    manual_ans_arr = [-sympy.sin(a*x**2)*4*a**2*x**2+sympy.cos(a*x**2)*2*a,-b**2*sympy.cos(b*x), (30*c)/(x+1)**7]
    
    #randomly selects 0, 1, or 2 representing the selected index
    index_to_choose = random.randint(0,2)


    selected_q = q_arr[index_to_choose]
    selected_ans = manual_ans_arr [index_to_choose]
    
    data['params']['a'] = a
    data['params']['b'] = b
    data['params']['c'] = c

    #only displays the randomly selected question 
    data['params']['display_this'] = sympy.latex(selected_q)
    
    sympy_compute_ans = sympy.diff(selected_q,x,2)
    
    #checks whether sympy and manual computed answers match or not, if not error is raised to display the selected question
    assert sympy.simplify (sympy.Eq (selected_ans,sympy_compute_ans)),selected_q

    data['correct_answers']['ans'] = pl.to_json(sympy_compute_ans)
    
