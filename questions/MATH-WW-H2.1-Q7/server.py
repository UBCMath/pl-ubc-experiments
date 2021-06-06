import random
import sympy

def generate(data):

    # Generate a random number that determines the middle x-intercept of the function
    n = random.randint(1, 8)
    l = 0   # left x-intercept
    r = 9   # right x-intercept

    data['params']['n'] = n
    data['params']['l'] = l
    data['params']['r'] = r

    # SymPy setup
    x = sympy.Symbol('x', real=True)
    f = (1/18)*(x-n)*(x-l)*(x-r)

    # Calculates 6 integrals
    integrals = [
        ["ln", sympy.integrate(f, (x, l, n))],
        ["nl", sympy.integrate(f, (x, n, l))],
        ["nr", sympy.integrate(f, (x, n, r))],
        ["rn", sympy.integrate(f, (x, r, n))],
        ["lr", sympy.integrate(f, (x, l, r))],
        ["rl", sympy.integrate(f, (x, r, l))]
    ]

    # Takes integrated values, sort in descending order
    values = list(map(lambda a : a[1], integrals))
    values.sort(reverse=True)
    
    def matching(v):
        for i in integrals:
            if v == i[1]:
                return i[0]
        return ""
    
    # maps the integral names onto the sorted list
    ranking = list(map(matching, values))

    # saves the ranking (+1 because index 1)
    data['params']['ln'] = ranking.index('ln') + 1
    data['params']['nl'] = ranking.index('nl') + 1
    data['params']['nr'] = ranking.index('nr') + 1
    data['params']['rn'] = ranking.index('rn') + 1
    data['params']['lr'] = ranking.index('lr') + 1
    data['params']['rl'] = ranking.index('rl') + 1
