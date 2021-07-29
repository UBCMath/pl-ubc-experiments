import random
import sympy as sp
import prairielearn as pl

def generate(data):

    # Generate params
    e1 = random.randint(4, 9)
    e2 = random.randint(3, e1 - 1)

    c1 = e1 + 1
    c2 = e2 + 1
    c3 = random.randint(2, 9)
    c4 = random.randint(2, 9)

    data['params']['c1'] = c1
    data['params']['c2'] = c2
    data['params']['c3'] = c3
    data['params']['c4'] = c4
    data['params']['e1'] = e1
    data['params']['e2'] = e2

    while True:
        d1 = random.randint(1, 16)
        d2 = random.randint(2, 5)
        gcd = sp.igcd(d1, d2)
        if gcd == 1 and d1 != d2:
            break
    d3 = random.randint(2, 9)
    d4 = random.randint(2, 9)
    f1 = random.randint(2, 9)
    f2 = random.randint(2, 9)

    data['params']['d1'] = d1
    data['params']['d2'] = d2
    data['params']['d3'] = d3
    data['params']['d4'] = d4
    data['params']['f1'] = f1
    data['params']['f2'] = f2

    x = sp.symbols('x', real=True)
    i1 = sp.Rational(c1, e1+1)*x**(e1+1) + sp.Rational(c2, e2+1)*x**(e2+1) - sp.Rational(c3, 2)*x**2 + c4*x # + C
    i2 = sp.Rational(d1, d2*(f1+1))*x**(f1+1) - sp.Rational(d3, f2+1)*x**(f2+1) - d4*x # + C

    f1_s = c1*x**e1 + c2*x**e2 - c3*x + c4
    f2_s = sp.Rational(d1, d2)*x**f1 - d3*x**f2 - d4
    i1_s = sp.integrate(f1_s, x)
    i2_s = sp.integrate(f2_s, x)

    assert sp.simplify(sp.Eq(i1, i1_s))
    assert sp.simplify(sp.Eq(i2, i2_s))

    data['correct_answers']['integral-1'] = pl.to_json(i1)
    data['correct_answers']['integral-2'] = pl.to_json(i2)
