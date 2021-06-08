import random
import sympy

def generate(data):

    # Generate a random number that determines the middle x-intercept of the function
    n = random.randint(1, 8)
    # Positive or negative?
    sign = 1 if (random.randint(0, 1) == 1) else -1
    l = 0   # left x-intercept
    r = 9   # right x-intercept

    data['params']['n'] = n
    data['params']['sign'] = sign
    data['params']['l'] = l
    data['params']['r'] = r

    # SymPy setup
    x = sympy.Symbol('x', real=True)
    f = sign * (1/18) * (x-n) * (x-l) * (x-r)

    # Calculates 3 integrals
    integral_ln = sympy.integrate(f, (x, l, n))
    integral_nr = sympy.integrate(f, (x, n, r))
    integral_lr = sympy.integrate(f, (x, l, r))

    integrals = {
        "ln": integral_ln,
        "nl": -integral_ln, #  prev integral but bounds flipped
        "nr": integral_nr,
        "rn": -integral_nr, #  prev integral but bounds flipped
        "lr": integral_lr,
        "rl": -integral_lr  #  prev integral but bounds flipped
    }

    # Takes integrated values, sort in descending order
    ranking = list(dict(sorted(integrals.items(), key=lambda item: item[1], reverse=True)).keys())

    # saves the ranking (+1 because index 1)
    data['params']['ln'] = ranking.index('ln') + 1
    data['params']['nl'] = ranking.index('nl') + 1
    data['params']['nr'] = ranking.index('nr') + 1
    data['params']['rn'] = ranking.index('rn') + 1
    data['params']['lr'] = ranking.index('lr') + 1
    data['params']['rl'] = ranking.index('rl') + 1
