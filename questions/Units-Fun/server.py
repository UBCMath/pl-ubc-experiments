import math
import re

# From Wikipedia:
#   The derived units in the SI are formed by powers, products, or quotients of the
#   base units and are potentially unlimited in number.

# To compare these units, we can represent these units as rational numbers. We know
# all integers can be factorized down to prime numbers, and therefore every unit can
# be represented as fractions, the composite of base units, as primes.

# initializes the base units as first 7 prime numbers
BASE_UNITS = {
        "s": 2,
        "m": 3,
        "kg": 5,
        "A": 7,
        "K": 11,
        "mol": 13,
        "cd": 17
    }

def numberify_base(unit):
    # splits strings into cells of base units, replaces them with number
    components = list(map((lambda a : str(BASE_UNITS.get(a.strip(), a))), re.split("[*\/^()]", unit)))
    # retain the operations
    operations = list(re.sub("[^*\/^()]", "", unit))
    # join together numbers and operations
    string = "".join([j for i in zip(components, operations) for j in i]) + str(components[-1])
    return eval(string.replace("^", "**")) # no security concern, since only used in DERIVED_UNITS?

# initializes the derived units as numberified powers of base unit primes
DERIVED_UNITS = {
    "rad": 1,
    "sr": 1,
    "Hz": numberify_base("1/s"),
    "N": numberify_base("kg*m/s^2"),
    "Pa": numberify_base("kg/(m*s^2)"),
    "J": numberify_base("kg*m^2/s^2"),
    "W": numberify_base("kg*m^2/s^3"),
    "C": numberify_base("A*s"),
    "V": numberify_base("kg*m^2/(A*s^3)"),
    "F": numberify_base("A^2*s^4/kg/m^2"),
    "O": numberify_base("kg*m^2/s^3/A^2"), # decided that Ω = O
    "Ω": numberify_base("kg*m^2/s^3/A^2"),
    "S": numberify_base("A^2*s^3/kg/m^2"),
    "Wb": numberify_base("kg*m^2/A/s^2"),
    "T": numberify_base("kg/s^2/A"),
    "H": numberify_base("kg*m^2/s^2/A^2"),
    "lm": numberify_base("cd"),
    "lx": numberify_base("cd/m^2"),
    "Bq": numberify_base("1/s"),
    "Gy": numberify_base("m^2/s^2"),
    "Sv": numberify_base("m^2/s^2"),
    "kat": numberify_base("mol/s")
}

# combined base and derived units
UNITS = BASE_UNITS.copy()
UNITS.update(DERIVED_UNITS)

def numberify(unit):
    # splits strings into cells of base units, replaces them with number
    components = list(map((lambda a : str(UNITS.get(a.strip(), a))), re.split("[*\/^()]", unit)))
    # retain the operations
    operations = list(re.sub("[^*\/^()]", "", unit))
    # join together numbers and operations
    string = "".join([j for i in zip(components, operations) for j in i]) + str(components[-1])
    return eval(string.replace("^", "**"))

def parse(data):
    # checks whether a string is an integer
    def is_int(s):
        if s[0] in ('-','+'):
            return s[1:].isdigit()
        return s.isdigit()

    for answer in data['submitted_answers']:
        if answer not in data['format_errors']:
            unit = data['submitted_answers'][answer]
            # checks whether components are valid units or integers
            components = (list(map(lambda a : a.strip(), re.split("[*\/^()]", unit))))
            for i in components:
                if i not in UNITS and i != "" and not is_int(i):
                    data['format_errors'][answer] = i + " is not a valid unit."
                    break

def grade(data):
    # sample answer
    data['params']['t'] = "s"
    data['params']['F'] = "N"
    data['params']['j'] = "A/m^2"


    # check whether they are identical or numerically same
    for answer in data['submitted_answers']:
        sample = data['params'][answer]
        ans = data['submitted_answers'][answer]
        if sample == ans or math.isclose(numberify(sample), numberify(ans)):
            data['partial_scores'][answer] = {'score': 1, 'weight': 1}
        else:
            data['partial_scores'][answer] = {'score': 0, 'weight': 1}
    
    # calculate score
    correct = 0
    variables = data['partial_scores'].keys()
    for name in variables:
        correct += data['partial_scores'][name]['score']  
    data['score'] = correct / len(variables)
