from sympy import var, latex, Sum, oo, pi, sin

def generate(data):
    var('n')
    data['params']['a'] = latex(Sum(1/n, (n,1,oo)))
    data['params']['b'] = latex(Sum(n**2/(n+1), (n,1,oo)))
    data['params']['c'] = latex(Sum(sin(n), (n,1,oo)))
    data['params']['d'] = latex(Sum(sin(pi*n), (n,1,oo)))