from __future__ import annotations
from typing import Any

from enum import Enum
import sympy
import re
import ast

class InvalidUnit(Exception):
    pass

class DisallowedExpression(Exception):
    pass

class DimensionfulQuantity:
    def __init__(self, quantity: Any, unit: Unit) -> None:
        self.quantity = quantity
        self.unit = unit

    def __eq__(self, rhs: DimensionfulQuantity) -> bool:
        return self.quantity * self.unit.multiplier == rhs.quantity * rhs.unit.multiplier and self.unit == rhs.unit
    
    @classmethod
    def from_tuple(cls, tup: Tuple[Any, Unit]) -> DimensionfulQuantity:
        return DimensionfulQuantity(tup[0], Unit.from_string(tup[1]))
    
    @classmethod
    def from_string(cls, answer: str) -> DimensionfulQuantity:
        m = re.search(r'[a-z|A-Z|Ω|μ]', answer, re.I) # search for valid alpha/greek for unit start
        i = m.start() if m is not None else -1 # get index
        if i == -1:
            raise DisallowedExpression
        return DimensionfulQuantity(float(answer[:i].strip()), Unit.from_string(answer[i:].strip()))

class Unit:
    def __init__(self, multiplier: float, godel_frac: sympy.Rational) -> None:
        # factor by which quantities in given units will differ from quantities in SI base units
        self.multiplier = multiplier
        # Gödel fraction representing the unit's dimensions
        self.godel_frac = godel_frac

    def __mul__(self, rhs: float | Unit) -> Unit:
        # for ergonomics, it turns out to be nice to be able to multiply units by floats to represent scaling
        if isinstance(rhs, Unit):
            new_multiplier = self.multiplier * rhs.multiplier
            new_godel_frac = self.godel_frac * rhs.godel_frac
            return Unit(new_multiplier, new_godel_frac)
        else:
            new_multiplier = self.multiplier * rhs
            return Unit(new_multiplier, self.godel_frac)

    def __rmul__(self, lhs: float | Unit) -> Unit:
        if isinstance(lhs, Unit):
            new_multiplier =  lhs.multiplier * self.multiplier
            new_godel_frac = lhs.godel_frac * self.godel_frac
            return Unit(new_multiplier, new_godel_frac)
        else:
            new_multiplier = lhs * self.multiplier
            return Unit(new_multiplier, self.godel_frac)

    def __truediv__(self, rhs: Unit) -> Unit:
        new_multiplier = self.multiplier / rhs.multiplier
        new_godel_frac = self.godel_frac / rhs.godel_frac
        return Unit(new_multiplier, new_godel_frac)

    def __rtruediv__(self, lhs: Unit) -> Unit:
        new_multiplier = lhs.multiplier / self.multiplier
        new_godel_frac = lhs.godel_frac / self.godel_frac
        return Unit(new_multiplier, new_godel_frac)

    def __pow__(self, exp: int) -> Unit:
        new_multiplier = self.multiplier ** exp
        new_godel_frac = self.godel_frac ** exp
        return Unit(new_multiplier, sympy.Rational(new_godel_frac))

    def __eq__(self, rhs: Unit) -> bool:
        return self.godel_frac - rhs.godel_frac == 0

    @classmethod
    def _from_prefixed_unit(cls, prefix: SIPrefix, unit: Unit) -> Unit:
        new_multiplier = unit.multiplier * 10 ** prefix.value
        return cls(new_multiplier, unit.godel_frac)

    @classmethod
    def _single_from_string(cls, str: str) -> Unit:
        # here be dragons
        regex = f"(?:({'|'.join(MetricPrefixes.__members__.keys())})?({'|'.join(MetricUnits.__members__.keys())}))|({'|'.join(ImperialUnits.__members__.keys())})"
        regex = re.compile(regex)

        match = re.fullmatch(regex, str)

        if not match:
            raise InvalidUnit

        if match[3]:
            return ImperialUnits[match[3]].value
        else:
            if match[1]:
                return cls._from_prefixed_unit(MetricPrefixes[match[1]].value, MetricUnits[match[2]].value)
            else:
                return MetricUnits[match[2]].value

    @classmethod
    def from_string(cls, str: str) -> Unit:
        tree = ast.parse(str, mode="eval")
        whitelist = (ast.Expression, ast.Name, ast.Load, ast.BinOp, ast.Mult, ast.Div, ast.Pow, ast.Constant)
        CheckWhitelist(whitelist).visit(tree)
        UnitTransform().visit(tree)
        ast.fix_missing_locations(tree)
        return eval(compile(tree, '<ast>', 'eval'), None, None)

class SIBaseUnit(Unit, Enum):
    def __init__(self, godel_number: int) -> None:
        # all base units have a multiplier of 1, and their Gödel fraction is just their assigned Gödel number
        super().__init__(1, sympy.Rational(godel_number))
    Second = 2
    Metre = 3
    Gram = 5
    Ampere = 7
    Kelvin = 11
    Mole = 13
    Candela = 17

    # defining this as a constant makes life a bit easier when it comes to defining derived units
    Kilogram = 1000 * Gram

class SIPrefix(Enum):
    Yotta = 24
    Zetta = 21
    Exa = 18
    Peta = 15
    Tera = 12
    Giga = 9
    Mega = 6
    Kilo = 3
    Hecto = 2
    Deca = 1
    Unit = 0
    Deci = -1
    Centi = -2
    Milli = -3
    Micro = -6
    Nano = -9
    Pico = -12
    Femto = -15
    Atto = -18
    Zepto = -21
    Yocto = -24

class UnitTransform(ast.NodeTransformer):
    def visit_Name(self, node):
        return ast.copy_location(
            ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='Unit', ctx=ast.Load()),
                    attr='_single_from_string',
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
            raise DisallowedExpression
        return super().visit(node)

class MetricUnits(Enum):
    s = SIBaseUnit.Second
    m = SIBaseUnit.Metre
    g = SIBaseUnit.Gram
    A = SIBaseUnit.Ampere
    K = SIBaseUnit.Kelvin
    mol = SIBaseUnit.Mole
    cd = SIBaseUnit.Candela
    rad = SIBaseUnit.Metre / SIBaseUnit.Metre
    sr = SIBaseUnit.Metre ** 2 / SIBaseUnit.Metre ** 2
    Hz = SIBaseUnit.Second ** -1
    N = SIBaseUnit.Kilogram * SIBaseUnit.Metre * SIBaseUnit.Second ** -2
    Pa = SIBaseUnit.Kilogram * SIBaseUnit.Metre ** -1 * SIBaseUnit.Second ** -2
    J = SIBaseUnit.Kilogram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -2
    W = SIBaseUnit.Kilogram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -3
    C = SIBaseUnit.Second * SIBaseUnit.Ampere
    V = SIBaseUnit.Kilogram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -3 * SIBaseUnit.Ampere ** -1
    F = SIBaseUnit.Kilogram ** -1 * SIBaseUnit.Metre ** -2 * SIBaseUnit.Second ** 4 * SIBaseUnit.Ampere ** 2
    O = SIBaseUnit.Kilogram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -3 * SIBaseUnit.Ampere ** -2
    Ω = SIBaseUnit.Kilogram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -3 * SIBaseUnit.Ampere ** -2
    S = SIBaseUnit.Kilogram ** -1 * SIBaseUnit.Metre ** -2 * SIBaseUnit.Second ** 3 * SIBaseUnit.Ampere ** 2
    Wb = SIBaseUnit.Kilogram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -2 * SIBaseUnit.Ampere ** -1
    T = SIBaseUnit.Kilogram * SIBaseUnit.Second ** -2 * SIBaseUnit.Ampere ** -1
    H = SIBaseUnit.Kilogram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -2 * SIBaseUnit.Ampere ** -2

    # some common metric units that are not technically SI
    min = 60 * SIBaseUnit.Second
    h = 3600 * SIBaseUnit.Second
    d = 86400 * SIBaseUnit.Second
    au = 149597870700 * SIBaseUnit.Metre
    L = 10e-3 * SIBaseUnit.Metre ** 3
    eV = 1.602176634e-19 * SIBaseUnit.Kilogram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -2

class MetricPrefixes(Enum):
    Y = SIPrefix.Yotta
    Z = SIPrefix.Zetta
    E = SIPrefix.Exa
    P = SIPrefix.Peta
    T = SIPrefix.Tera
    G = SIPrefix.Giga
    M = SIPrefix.Mega
    k = SIPrefix.Kilo
    h = SIPrefix.Hecto
    da = SIPrefix.Deca
    d = SIPrefix.Deci
    c = SIPrefix.Centi
    m = SIPrefix.Milli
    μ = SIPrefix.Micro
    n = SIPrefix.Nano
    p = SIPrefix.Pico
    f = SIPrefix.Femto
    a = SIPrefix.Atto
    z = SIPrefix.Zepto
    y = SIPrefix.Yocto

class ImperialUnits(Enum):
    ft = 0.3048 * SIBaseUnit.Metre
    yd = 0.9144 * SIBaseUnit.Metre
    mi = 1609.344 * SIBaseUnit.Metre
    acre = 4046.8564224 * SIBaseUnit.Metre ** 2
    oz = 28.349523125 * SIBaseUnit.Gram
    lb = 453.59237 * SIBaseUnit.Gram
