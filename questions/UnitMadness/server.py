import units
import math

def grade(data):
    submitted_capacitance = data["submitted_answers"]["capacitance"]
    submitted_c_units = units.Unit.from_string(data["submitted_answers"]["c-units"])
    submitted_capacitance = submitted_capacitance * submitted_c_units.multiplier

    submitted_length = data["submitted_answers"]["length"]
    submitted_l_units = units.Unit.from_string(data["submitted_answers"]["l-units"])
    submitted_length *= submitted_l_units.multiplier

    if math.isclose(submitted_capacitance, 1) and submitted_c_units == units.Unit.from_string("F"):
        data["partial_scores"]["capacitance"] = {"score": 1, "weight": 1}
        data["partial_scores"]["c-units"] = {"score": 1, "weight": 1}
    else:
        data["partial_scores"]["capacitance"] = {"score": 0, "weight": 1}
        data["partial_scores"]["c-units"] = {"score": 0, "weight": 1}

    if math.isclose(submitted_length, 1) and submitted_l_units == units.Unit.from_string("m"):
        data["partial_scores"]["length"] = {"score": 1, "weight": 1}
        data["partial_scores"]["l-units"] = {"score": 1, "weight": 1}
    else:
        data["partial_scores"]["length"] = {"score": 0, "weight": 1}
        data["partial_scores"]["l-units"] = {"score": 0, "weight": 1}

    # calculate score
    correct = 0
    variables = data["partial_scores"].keys()
    for name in variables:
        correct += data["partial_scores"][name]["score"]  
    data["score"] = correct / len(variables)
