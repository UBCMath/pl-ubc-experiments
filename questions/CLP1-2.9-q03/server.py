from random import randint
from sympy import sin, cos, tan, cot, sec, csc, Symbol, latex, Eq
import prairielearn as pl

def generate(data):

    # Generate params
    x = Symbol('x', real=True)
    a0 = randint(0, 3) # choose trig
    a1 = randint(1, 9)
    a2 = randint(-9, 8)
    a2 += 0 if a2 < 0 else 1
    assert a2 != 0
    a3 = a1 * x + a2 # function inside trig
    trig_a = [sin(a3), cos(a3), -sin(a3), -cos(a3)]
    q1 = trig_a[a0] # question

    b0 = randint(0, 3) # randint(0, 3) # choose trig
    b1 = randint(1, 9)
    b2 = randint(3, 5)
    b3 = randint(-9, 8)
    b3 += 0 if b3 < 0 else 1
    b4 = randint(1, b2 - 1)
    b5 = randint(-9, 8)
    b5 += 0 if b5 < 0 else 1
    b6 = b1 * x**b2 + b3 * x**b4 + b5 # polynomial inside trig
    trig_b = [tan(b6), cot(b6), sec(b6), csc(b6)]
    trig_diff = [1/cos(b6)**2, -1/sin(b6)**2, tan(b6)/cos(b6), -1/tan(b6)/sin(b6)] # derivatives of trig_b with respect to b6
    q2 = trig_b[b0] # question

    data['params']['q1'] = latex(q1)
    data['params']['q2'] = latex(q2)

    # Generate solutions
    s1 = a1 * trig_a[(a0+1) % 4] # chain rule, derivative of a3 * derivative of trig_a with respect to a3
    assert Eq(s1, q1.diff(x))
    s2 = (b2 * b1 * x**(b2 - 1) + b4 * b3 * x**(b4 - 1)) * trig_diff[b0] # chain rule, derivative of b6 * trig_diff
    assert Eq((s2-q2.diff(x)).trigsimp().simplify(), 0)
    
    data['correct_answers']['s1'] = pl.to_json(s1)
    data['correct_answers']['s2'] = pl.to_json(s2)
