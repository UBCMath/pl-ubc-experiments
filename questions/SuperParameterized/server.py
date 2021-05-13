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

    # a bit of weirdness necessary to avoid "+-" instead of just "-". this may not be a good way to do this
    data["params"]["num_sign1"] = "" if data["params"]["num_b"] < 0 else "+"
    data["params"]["num_sign2"] = "" if data["params"]["num_c"] < 0 else "+"
    data["params"]["denom_sign1"] = "" if data["params"]["denom_b"] < 0 else "+"
    data["params"]["denom_sign2"] = "" if data["params"]["denom_c"] < 0 else "+"

    data["params"]["limit"] = limit

    data["correct_answers"]["limit"] = pl.to_json(rational.subs(x, limit))
