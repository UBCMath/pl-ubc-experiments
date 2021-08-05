import random
import math

def generate(data):

    # Generate parameters
    initial_mass = random.randint(5, 10)
    final_mass = random.randint(1, initial_mass - 1)
    final_time = random.randint(1, 5)

    k = math.log(initial_mass / final_mass) / final_time
    
    half_life = math.log(2) / k

    data["params"]["initial_mass"] = initial_mass
    data["params"]["final_mass"] = final_mass
    data["params"]["final_time"] = final_time
    data["correct_answers"]["half_life"] = half_life