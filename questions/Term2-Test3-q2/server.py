import prairielearn as pl
from sympy import symbols, simplify, Rational
import random, copy

def generate (data):
    water = random.randint(5,20)
    flow_in = random.randint(4,10)    
    while (True):
        flow_out = random.randint(1,8)
        if (flow_out != flow_in):
            break
    salt_solution = random.randint(1,8)


    data['params']['water'] = water
    data['params']['flow_in'] = flow_in
    data['params']['flow_out'] = flow_out
    data['params']['salt_solution'] = round(salt_solution*(1/10),1)
    S = symbols("S")
    t = symbols("t")
    net_flow = flow_in - flow_out
    volume = water + net_flow*t
    ans =  simplify (flow_in*salt_solution*(Rational (1,10))) - simplify ((flow_out)*S*(1/volume))
    data['correct_answers']['symbolic_math'] = pl.to_json(ans)
    data['correct_answers']['c3'] = 0
    data['correct_answers']['c4'] = 0