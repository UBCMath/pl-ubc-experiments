#  CLP1 1.7 Q23


Evaluate the integral using integration by parts. Use $C$ as the constant of integration.

Problem from: https://secure.math.ubc.ca/~CLP/CLP2/clp_2_ic_problems.pdf

  

##  $\displaystyle \int ae^{\cos (x)}\sin(2x)\,dx$
  

Use $\sin(2x) =2\sin(x)\cos(x)$ to simplify:

$$\displaystyle \int ae^{\cos (x)}\sin(2x)\,dx =2a \displaystyle \int e^{\cos (x)}\sin(x)\cos(x)\,dx $$

Use the substitution $w=\cos(x), dw = -\sin(x) dx$:
$$=-2a \displaystyle \int we^{w}\,dw$$

Then, use IBP with $u=w, dv = e^{w}dw, du = dw, v = e^{w}$ to simplify:

$$=2ae^{w}(1-w)+C = 2ae^{\cos(x)}(1-\cos(x))+C$$