import prairielearn as pl
import sympy
import random

def generate(data):
    x = sympy.symbols("x")

    # generate a list of variables to be used in creating the rational
    random_parameters = random.choices([i for i in range(-5, 6) if i!=0], k=8)

    # generate a random rational expression
    numerator = (random_parameters[0]*x+random_parameters[1])*(random_parameters[2]*x+random_parameters[3])
    denominator = (random_parameters[4]*x+random_parameters[5])*(random_parameters[6]*x+random_parameters[7])
    rational = numerator/denominator

    # ensure that the randomly chosen limit isn't at a discontinuity in the rational
    limit = random.choices([n for n in range(-5, 6) if denominator.subs(x, n)!=0])[0]

    # (ax+b)(cx+d) = acx^2 + (ad+bc)x + bd
    data["params"]["num_a"] = random_parameters[0]*random_parameters[2]
    data["params"]["num_b"] = random_parameters[0]*random_parameters[3] + random_parameters[1]*random_parameters[2]
    data["params"]["num_c"] = random_parameters[1]*random_parameters[3]

    data["params"]["denom_a"] = random_parameters[4]*random_parameters[6]
    data["params"]["denom_b"] = random_parameters[4]*random_parameters[7] + random_parameters[5]*random_parameters[6]
    data["params"]["denom_c"] = random_parameters[5]*random_parameters[7]

    data["params"]["limit"] = limit

    data["correct_answers"]["limit"] = pl.to_json(rational.subs(x, limit))