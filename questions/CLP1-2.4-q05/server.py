import random
import sympy as s
import prairielearn as pl

def generate(data):

    # Generate params
    a1 = random.randint(2, 9)
    a2 = random.randint(3, 8)
    a3 = random.randint(2, 9)
    a4 = random.randint(2, a2 - 1)

    assert a2 != a4

    b1 = random.randint(2, 9)
    b2 = random.randint(2, 8)
    while True:
        b3 = random.randint(1, 16)
        b4 = random.randint(2, 5)
        gcd = s.igcd(b3, b4)
        if gcd == 1 and b3 != b4:
            break
    while True:
        b6 = random.randint(3, 7)
        b5 = random.randint(2, b6 - 1)
        gcd = s.igcd(b5, b6)
        if gcd == 1 and b5 != b6:
            break

    assert b3 != b4
    assert b5 != b6
    assert b4 != 1
    assert b6 != 1

    data['params']['a1'] = a1
    data['params']['a2'] = a2
    data['params']['a3'] = a3
    data['params']['a4'] = a4

    data['params']['b1'] = b1
    data['params']['b2'] = b2
    data['params']['b3'] = b3
    data['params']['b4'] = b4
    data['params']['b5'] = b5
    data['params']['b6'] = b6

    # Evaluate function
    x = s.symbols('x', real=True)
    a = (a1 * a2) * x**(a2-1) + (a3 * a4) * x**(a4-1)
    b = (b1 * b2) * x**(b2-1) + s.Rational(b3 * b5, b4 * b6) * x**(s.Rational(b5, b6) - 1)

    f = a1 * x**a2 + a3 * x**a4
    g = b1 * x**b2 + s.Rational(b3, b4) * x**s.Rational(b5, b6)
    a_s = s.diff(f)
    b_s = s.diff(g)

    assert s.simplify(s.Eq(a, a_s))
    assert s.simplify(s.Eq(b, b_s))

    data['correct_answers']['a'] = pl.to_json(a)
    data['correct_answers']['b'] = pl.to_json(b)
