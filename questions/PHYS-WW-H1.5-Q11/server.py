import random

def generate(data):
    inital_pressure = round(random.uniform(1.0, 5.0), 2)
    initial_temperature = random.randint(300, 400)

    data["params"]["initial_pressure"] = inital_pressure
    data["params"]["initial_temperature"] = initial_temperature

    data["correct_answers"]["final_pressure"] = 2 * inital_pressure
    data["correct_answers"]["final_temperature"] = initial_temperature / 2 - 273