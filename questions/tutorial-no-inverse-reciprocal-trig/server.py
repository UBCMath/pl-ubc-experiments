from random import randint
from sympy import Symbol, asin, acos, atan
import prairielearn as pl

def generate(data):

    x = Symbol('x')
    a = randint(0, 2)
    trig = ["arccot", "arcsec", "arccsc"]
    alt = ["acot", "asec", "acsc"]
    a_trig = [atan(1/x), acos(1/x), asin(1/x)]

    data['params']['inv'] = trig[a]
    data['params']['alt'] = alt[a]
    data['correct_answers']['a_inv'] = pl.to_json(a_trig[a])
