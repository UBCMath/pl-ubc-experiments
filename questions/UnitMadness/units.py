from enum import Enum
import re
import sympy
import ast

# An arbitrary SIUnit, possibly composed of an arbitrary combination of base units.
class Unit:
    def __init__(self, multiplier, dimensions):
        self.multiplier = multiplier
        self.dimensions = dimensions

    def __mul__(self, other):
        multiplier = self.multiplier * other.multiplier
        dimensions = self.dimensions * other.dimensions
        return Unit(multiplier, dimensions)

    def __truediv__(self, other):
        multiplier = self.multiplier / other.multiplier
        dimensions = self.dimensions / other.dimensions
        return Unit(multiplier, dimensions)

    def __rmul__(self, other):
        multiplier = other.multiplier * self.multiplier
        dimensions = other.dimensions * self.dimensions
        return Unit(multiplier, dimensions)

    def __rtruediv__(self, other):
        multiplier = other.multiplier / self.multiplier
        dimensions = other.dimensions / self.dimensions
        return Unit(multiplier, dimensions)

    def __pow__(self, exp):
        multiplier = self.multiplier ** exp
        dimensions = self.dimensions ** exp
        return Unit(multiplier, dimensions)

    # Importantly, equality only checks that the units are the same, i.e. Newtons are equal to dynes.
    # i.e. equality checks for dimensionally equal units.
    def __eq__(self, other):
        return sympy.Eq(self.dimensions, other.dimensions)

    # Parse a non-compound SI unit from a string (i.e. "pF" or "kN" or "mg", but not "C/V").
    @classmethod
    def single_from_string(cls, str):
        # First, we create a regex that matches units and their prefixes.
        regex = re.compile(f"({'|'.join(PREFIXES.keys())})?({'|'.join(BASE_UNITS.keys())}|{'|'.join(DERIVED_UNITS.keys())})")
        match = re.match(regex, str)

        # If there is no match, the string must not represent a valid unit.
        if not match:
            raise ValueError(f"{str} is not a valid SI unit.")
        
        # Since the regex matched, it is guaranteed that none of the below will raise a KeyError.

        # The prefix can just be obtained from the PREFIXES dictionary.
        if not match.group(1):
            multiplier = 1
        else:
            multiplier = PREFIXES[match.group(1)].value
        # The underlying unit is in either the BASE_UNITS or the DERIVED_UNITS dictionary.
        dimensions = (BASE_UNITS|DERIVED_UNITS)[match.group(2)].dimensions

        return cls(multiplier, dimensions)

    @classmethod
    def from_string(cls, str):
        tree = ast.parse(str, mode="eval")
        whitelist = (ast.Expression, ast.Name, ast.Load, ast.BinOp, ast.Mult, ast.Div, ast.Pow, ast.Constant)
        CheckWhitelist(whitelist).visit(tree)
        UnitTransform().visit(tree)
        ast.fix_missing_locations(tree)
        return eval(compile(tree, '<ast>', 'eval'), None, None)

# A multiplier disguised as a unit.
class Multiplier(Unit):
    def __init__(self, multiplier):
        # dimensionless multiplier
        super().__init__(multiplier, 1)

# A single, pure SIUnit, having only a prefix and an underlying base unit, such as "ns" or "kg", but not "pF".
class PureSIUnit(Unit):
    def __init__(self, prefix, unit):
        # Pure SI Units have an exponent equal to the assigned enum value of their prefix, and a Gödel fraction equal to the unit's prime.
        self.prefix = prefix
        self.unit = unit
        super().__init__(prefix.value, sympy.sympify(unit.value))

# An SI Base Unit, one of "s", "m", "g", "A", "K", "mol", or "cd".
class SIBaseUnit(Unit, Enum):
    # The base units all have an exponent of 0, and their Gödel fraction is equal to their assigned enum prime.
    def __init__(self, prime):
        # gram is initialized as a multiplier of 1/1000, since kg is base unit
        if prime == 5:
            super().__init__(1e-3, 5)
        else:
            super().__init__(1, sympy.sympify(prime))
    
    # All of the SI Base units are assigned a prime number.
    Second = 2
    Metre = 3
    Gram = 5
    Ampere = 7
    Kelvin = 11
    Mole = 13
    Candela = 17

    @classmethod
    def from_string(cls, str):
        if BASE_UNITS[str]:
            return BASE_UNITS[str]
        else:
            raise ValueError(f"{str} is not a valid SI base unit.")

# An SI Prefix, ranging from yotta to yocto.
class SIPrefix(Enum):
    Yotta = 1e24
    Zetta = 1e21
    Exa = 1e18
    Peta = 1e15
    Tera = 1e12
    Giga = 1e9
    Mega = 1e6
    Kilo = 1e3
    Hecto = 1e2
    Deca = 1e1
    Unit = 1e0
    Deci = 1e-1
    Centi = 1e-2
    Milli = 1e-3
    Micro = 1e-6
    Nano = 1e-9
    Pico = 1e-12
    Femto = 1e-15
    Atto = 1e-18
    Zepto = 1e-21
    Yocto = 1e-24

    @classmethod
    def from_string(cls, str):
        if not str:
            return cls.Unit
        else:
            if PREFIXES[str]:
                return PREFIXES[str]
            else:
                raise ValueError(f"{str} is not a valid SI prefix.")

class UnitTransform(ast.NodeTransformer):
    def visit_Name(self, node):
        return ast.copy_location(
            ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='Unit', ctx=ast.Load()),
                    attr='single_from_string',
                    ctx=ast.Load()
                ),
                args=[ast.Constant(value=node.id)],
                keywords=[]
            ),
            node
        )

class CheckWhitelist(ast.NodeVisitor):
    def __init__(self, whitelist):
        self.whitelist = whitelist
    def visit(self, node):
        if not isinstance(node, self.whitelist):
            raise Exception(f"{ast.dump(node, indent=4)}")
        return super().visit(node)

# All of the SI Prefixes.
PREFIXES = {
    "Y": SIPrefix.Yotta,
    "Z": SIPrefix.Zetta,
    "E": SIPrefix.Exa,
    "P": SIPrefix.Peta,
    "T": SIPrefix.Tera,
    "G": SIPrefix.Giga,
    "M": SIPrefix.Mega,
    "k": SIPrefix.Kilo,
    "h": SIPrefix.Hecto,
    "da": SIPrefix.Deca,
    "d": SIPrefix.Deci,
    "c": SIPrefix.Centi,
    "m": SIPrefix.Milli,
    "μ": SIPrefix.Micro,
    "n": SIPrefix.Nano,
    "p": SIPrefix.Pico,
    "f": SIPrefix.Femto,
    "a": SIPrefix.Atto,
    "z": SIPrefix.Zepto,
    "y": SIPrefix.Yocto
}

# All of the Base Units.
BASE_UNITS = {
    "s": SIBaseUnit.Second,
    "m": SIBaseUnit.Metre,
    "g": SIBaseUnit.Gram,
    "A": SIBaseUnit.Ampere,
    "K": SIBaseUnit.Kelvin,
    "mol": SIBaseUnit.Mole,
    "cd": SIBaseUnit.Candela
}

# A fairly large selection of derived units.
DERIVED_UNITS = {
    "rad": SIBaseUnit.Metre / SIBaseUnit.Metre,
    "sr": SIBaseUnit.Metre**2 / SIBaseUnit.Metre**2,
    "Hz": SIBaseUnit.Second**-1,
    "N": PureSIUnit(SIPrefix.Kilo, SIBaseUnit.Gram) * SIBaseUnit.Metre * SIBaseUnit.Second**-2,
    "Pa": PureSIUnit(SIPrefix.Kilo, SIBaseUnit.Gram) * SIBaseUnit.Metre**-1 * SIBaseUnit.Second**-2,
    "J": PureSIUnit(SIPrefix.Kilo, SIBaseUnit.Gram) * SIBaseUnit.Metre**2 * SIBaseUnit.Second**-2,
    "W": PureSIUnit(SIPrefix.Kilo, SIBaseUnit.Gram) * SIBaseUnit.Metre**2 * SIBaseUnit.Second**-3,
    "C": SIBaseUnit.Second * SIBaseUnit.Ampere,
    "V": PureSIUnit(SIPrefix.Kilo, SIBaseUnit.Gram) * SIBaseUnit.Metre**2 * SIBaseUnit.Second**-3 * SIBaseUnit.Ampere**-1,
    "F": PureSIUnit(SIPrefix.Kilo, SIBaseUnit.Gram)**-1 * SIBaseUnit.Metre**-2 * SIBaseUnit.Second**4 * SIBaseUnit.Ampere**2,
    "Ω": PureSIUnit(SIPrefix.Kilo, SIBaseUnit.Gram) * SIBaseUnit.Metre**2 * SIBaseUnit.Second**-3 * SIBaseUnit.Ampere**-2,
    "S": PureSIUnit(SIPrefix.Kilo, SIBaseUnit.Gram)**-1 * SIBaseUnit.Metre**-2 * SIBaseUnit.Second**3 * SIBaseUnit.Ampere**2,
    "Wb": PureSIUnit(SIPrefix.Kilo, SIBaseUnit.Gram) * SIBaseUnit.Metre**2 * SIBaseUnit.Second**-2 * SIBaseUnit.Ampere**-1,
    "T": PureSIUnit(SIPrefix.Kilo, SIBaseUnit.Gram) * SIBaseUnit.Second**-2 * SIBaseUnit.Ampere**-1,
    "H": PureSIUnit(SIPrefix.Kilo, SIBaseUnit.Gram) * SIBaseUnit.Metre**2 * SIBaseUnit.Second**-2 * SIBaseUnit.Ampere**-2,
}

# A small sample of imperial units (grrrrrrr!)
IMPERIAL_UNITS = {
    "in": Multiplier(0.0254) * SIBaseUnit.Metre,
    "ft": Multiplier(0.3048) * SIBaseUnit.Metre
}
