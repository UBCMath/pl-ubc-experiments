# CLP1 3.2 Q10

  
Given that the pig is drinking water at a rate ($\frac {dV}{dt}$), find how fast the water level height is changing ($\frac {dh}{dt}$).

Problem source: https://secure.math.ubc.ca/~CLP/CLP1/clp_1_dc_problems.pdf
(TYPESET  ON  WEDNESDAY  5TH  MAY, 2021)


## Converting given parameters into centimeter

- $w$ (width at the top) from meters into cm (multiply by 100)
- $l$ (length of trough) from meters into cm (multiply by 100)
Other variables:
- $h$ (height of trough)
- $b$ (base of trough)
- now_height (height of water aka $h_{water}$)


  
## Calculations
Volume of water in trough
$$ V = lh\frac {b+w_{water}}{2} $$
Using similar triangles from cross section of trapezoid:
$$w_{water} = b+\frac{w-b}{h} h_{water}$$
Plug $w_{water}$ into $V$ to get:
$$ V = lh_{water}(2b +\frac {(w-b)h_{water}}{h})$$
$$ = blh_{water}+\frac {1}{2h}lh_{water}^2(w-b)$$
Take the derivative of $V$ to get $\frac {dV}{dt}$ (server.py trusts numpy to do this).
Plug in the given height of water (now_height ) into $h_{water}$. 
Solve for $\frac {dh}{dt}$ in terms of $\frac {cm}{s}$. 

Note the answer is positive because the question is phrased like this: "*how fast is the height decreasing?*"
