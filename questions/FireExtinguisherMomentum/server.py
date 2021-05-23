import random
def generate(data):
    # two constants to randomize momentum equation. question will ask about p = const * t^2 at t = t
    t = random.randint(3, 5)
    const  = random.randint(10, 30)

    # I wanted the "not enough information" possibility to be correct. it's easier, so only appears 10% of the time. this is a hacky bit of code and I don't like it
    question = random.choices(["how much force is acting on her", "what is her acceleration"], weights=[0.9, 0.1])[0]

    data["params"]["t"] = t
    data["params"]["const"] = const
    data["params"]["question"] = question

    data["params"]["incorrect1"] = f"{const * t ** 2} N"
    data["params"]["incorrect2"] = f"{const * t} N"
    data["params"]["incorrect3"] = f"{2 * const} N"

    if question == "what is her acceleration":
        data["params"]["correct"] = "Can't be determined without knowing her mass."
        data["params"]["incorrect4"] = f"{2 * const * t} N"
    else:
        data["params"]["correct"] = f"{2 * const * t} N"
        data["params"]["incorrect4"] = "Can't be determined without knowing her mass."
