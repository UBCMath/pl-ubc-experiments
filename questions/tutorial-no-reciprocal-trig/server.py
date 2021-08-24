from random import randint
from sympy import Symbol, sin, cos, tan
import prairielearn as pl

def generate(data):

    x = Symbol('x')
    a = randint(0, 2)
    trig = ["cot", "sec", "csc"]
    a_trig = [1/tan(x), 1/cos(x), 1/sin(x)]

    data['params']['trig'] = trig[a]
    data['correct_answers']['a_trig'] = pl.to_json(a_trig[a])
