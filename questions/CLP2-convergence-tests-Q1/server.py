import random
import sympy

def generate(data):
    sympy.var('n')
    data['params']['a'] = sympy.latex(sympy.Sum(1/n, (n,1,sympy.oo)))
    data['params']['b'] = sympy.latex(sympy.Sum(n**2/(n+1), (n,1,sympy.oo)))
    data['params']['c'] = sympy.latex(sympy.Sum(sympy.sin(n), (n,1,sympy.oo)))
    data['params']['d'] = sympy.latex(sympy.Sum(sympy.sin(sympy.pi*n), (n,1,sympy.oo)))