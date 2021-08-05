# CLP1 3.4 Q7

Use a constant approximation and linear approximation to approximate value of $b^{a}$, where $b = (10+(1/10)*b_0)$ and $b_0$ is a random integer from 1 to 4.
 
Combination of problems 3.4.1 Q5 and 3.4.2 Q7 from: https://secure.math.ubc.ca/~CLP/CLP1/clp_1_dc_problems.pdf


## Constant approximation

  
$b$ is close to 10, so raise 10 to power of a.


## Linear approximation


If $f(x) = x^{a}$, then $f(b)=b^{a}$, which is the value we want to estimate.

Take the linear approximation of $f(x)$ about $x = 10$:

$$f(10) = 10^{a}$$

$$f'(x) = ax^{a-1}$$

$$f'(10) = a10^{a-1}$$

$$f(b) \approx f(10) + f'(10)(b-10)$$

$$ \approx  10^{a}+a10^{a-1}(b-10) $$

