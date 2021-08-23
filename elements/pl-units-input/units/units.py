from __future__ import annotations
from typing import Any

from enum import Enum
import sympy
import re
import ast
import prairielearn as pl

class InvalidUnit(Exception):
    pass

class DisallowedExpression(Exception):
    pass

class DimensionfulQuantity:
    """A quantity and a unit strung together. Represents a number with units.
    
    ...

    Attributes
    ----------
    quantity : Any
        Usually some sort of number. The "Quantity" part.
    
    unit : Unit
        The unit accompanying the number. The "Dimensionful" part.
    
    Methods
    -------
    __eq__(rhs)
        Determines whether this and another DimensionfulQuantity are equal.
    
    sigfig_equals(rhs, digits)
        Determines whether this and another DimensionfulQuantity are equal, comparing only siginificant digits.
    
    relabs_equals(rhs, rtol, atol)
        Determines whether this and another DimensionfulQuantuty are within the relative and absolute tolerances.

    get_index(answer)
        Determines the index where the unit starts.

    from_string(answer)
        Constructs a DimensionfulQuantity from a string.
    
    check_unitless(answer)
        Checks whether the string has no unit portion.
    
    check_numberless(answer)
        Checks whether the string has no number portion.
    """

    def __init__(self, quantity: Any, unit: Unit) -> None:
        """
        Parameters
        ----------
        quantity : Any
            Usually some sort of number. The "Quantity" part.
        
        unit : Unit
            The unit accompanying the number. The "Dimensionful" part.
        """

        self.quantity = quantity
        self.unit = unit

    def __eq__(self, rhs: DimensionfulQuantity) -> bool:
        """Determines whether this and another DimensionfulQuantity are exactly equal.

        Equality is determined by two things:
            - number * multiplier/prefix of unit has to be equal
            - unit has to has same dimensions (i.e. describe the same kind of stuff)
        
        Parameters
        ----------
        rhs : DimensionfulQuantity
            The other DimensionfulQuantity we are comparing to.
        """

        return self.quantity * self.unit.multiplier == rhs.quantity * rhs.unit.multiplier and self.unit == rhs.unit
    
    def sigfig_equals(self, rhs: DimensionfulQuantity, digits: int) -> bool:
        """Determines whether this and another DimensionfulQuantity are equal, comparing only siginificant digits.
        
        Equality is determined by two things:
            - number * multiplier/prefix of unit has to be equal, comparing significant digits.
            - unit has to has same dimensions (i.e. describe the same kind of stuff)
        
        Parameters
        ----------
        rhs : DimensionfulQuantity
            The other DimensionfulQuantity we are comparing to.

        digits : int
            The number of significant digits we are comparing.
        """

        l_val = self.quantity * self.unit.multiplier
        r_val = rhs.quantity * rhs.unit.multiplier
        return pl.is_correct_scalar_sf(r_val, l_val, digits) and self.unit == rhs.unit
    
    def relabs_equals(self, rhs: DimensionfulQuantity, rtol: float, atol: float) -> bool:
        """Determines whether this and another DimensionfulQuantuty are within the relative and absolute tolerances.
        
        Equality is determined by two things:
            - number * multiplier/prefix of unit has to be within rhs' rtol and atol
            - unit has to has same dimensions (i.e. describe the same kind of stuff)
        
        Parameters
        ----------
        rhs : DimensionfulQuantity
            The other DimensionfulQuantity we are comparing to.

        rtol : float
            Relative tolerance.
        
        atol : float
            Absolute tolerance.
        """
        
        l_val = self.quantity * self.unit.multiplier
        r_val = rhs.quantity * rhs.unit.multiplier
        return pl.is_correct_scalar_ra(r_val, l_val, rtol, atol)
    
    @staticmethod
    def get_index(answer: str) -> int:
        """Determines the index where the unit starts.
        
        Determines the index of first character that matches a prefix/unit in the string.
        Returns -1 if not found.

        Parameters
        ----------
        answer : str
            String to search.
        """

        regex = f"(?:({'|'.join(MetricPrefixes.__members__.keys())})?({'|'.join(MetricUnits.__members__.keys())}))|({'|'.join(ImperialUnits.__members__.keys())})"
        regex = re.compile(regex)
        m = re.search(regex, answer) # search for valid alpha/greek for unit start
        return m.start() if m is not None else -1 # get index

    @classmethod
    def from_string(cls, answer: str) -> DimensionfulQuantity:
        """Constructs a DimensionfulQuantity from a string.
        
        Splits a string into the number and the unit part, and parses
        them as a float and a Unit respectively.

        Parameters
        ----------
        answer : str
            String to parse
        """

        i = cls.get_index(answer)
        if i == -1:
            raise DisallowedExpression
        return DimensionfulQuantity(float(answer[:i].strip()), Unit.from_string(answer[i:].strip()))
    
    @classmethod
    def check_unitless(cls, answer: str) -> bool:
        """Checks whether the string has no unit portion.

        Checks whether the string matches a unit/prefix at all.

        Parameters
        ----------
        answer : str
            String to search
        """
        
        i = cls.get_index(answer)
        return i == -1
    
    @classmethod
    def check_numberless(cls, answer: str) -> bool:
        """Checks whether the string has no number portion.

        Checks whether the string preceding the unit/prefix character is empty.

        Parameters
        ----------
        answer : str
            String to search
        """

        i = cls.get_index(answer)
        number = answer[:i].strip()
        return not number

class Unit:
    """A unit with no associated quantity.
    
    ...

    Attributes
    ----------
    multiplier : float
        A multiplier that represents the factor by which quantites in the given unit will differ from quantities in combinations of SI base units.
    
    godel_fraction : sympy.Rational
        A rational number uniquely identifying the unit. A little bit of black math-gic.
    
    Methods
    -------
    _from_prefixed_unit(prefix, unit)
        Create a unit by adding a metric prefix to a base unit.

    _from_single_string(str)
        Parse a string representing a single unit, such as "mT" into units.

    from_string(str)
        Parse a string, such as "pF", "kg", or "N / C", into units.
    """
    def __init__(self, multiplier: float, godel_frac: sympy.Rational) -> None:
        """
        Parameters
        ----------
        multiplier : float
            A multiplier representing the factor by which numbers in this unit would differ from numbers in combinations of SI base units.
        
        godel_frac : sympy.Rational
            A ratio of two Gödel numbers, representing every combination of SI base units uniquely.
        """
        self.multiplier = multiplier
        self.godel_frac = godel_frac

    def __mul__(self, rhs: float | Unit) -> Unit:
        """Multiply two units, or a float by a unit.
        
        Multiplying two units works exactly as expected, N * m = J, A * s = C, etc. Multiplying a unit by a float has the effect of "scaling" that unit, so something like 1000 * g = kg. This float-multiplying capability is mostly to clean up the definition of non-SI units and other odds and ends, and shouldn't be used by the end user.

        Parameters
        ----------
        rhs : float | Unit
            Unit or float to multiply by
        """
        if isinstance(rhs, Unit):
            new_multiplier = self.multiplier * rhs.multiplier
            new_godel_frac = self.godel_frac * rhs.godel_frac
            return Unit(new_multiplier, new_godel_frac)
        else:
            new_multiplier = self.multiplier * rhs
            return Unit(new_multiplier, self.godel_frac)

    def __rmul__(self, lhs: float | Unit) -> Unit:
        """Multiply two units, or a float by a unit.
        
        Multiplying two units works exactly as expected, N * m = J, A * s = C, etc. Multiplying a unit by a float has the effect of "scaling" that unit, so something like 1000 * g = kg. This float-multiplying capability is mostly to clean up the definition of non-SI units and other odds and ends, and shouldn't be used by the end user.

        Parameters
        ----------
        lhs : float | Unit
            Unit or float to multiply by
        """
        if isinstance(lhs, Unit):
            new_multiplier =  lhs.multiplier * self.multiplier
            new_godel_frac = lhs.godel_frac * self.godel_frac
            return Unit(new_multiplier, new_godel_frac)
        else:
            new_multiplier = lhs * self.multiplier
            return Unit(new_multiplier, self.godel_frac)

    def __truediv__(self, rhs: Unit) -> Unit:
        """Divide two units.
        
        Dividing two units works exactly as expected, N / m = Pa, J / C = V, etc.

        Parameters
        ----------
        lhs : Unit
            Unit to divide by
        """
        new_multiplier = self.multiplier / rhs.multiplier
        new_godel_frac = self.godel_frac / rhs.godel_frac
        return Unit(new_multiplier, new_godel_frac)

    def __rtruediv__(self, lhs: Unit) -> Unit:
        """Divide two units.
        
        Dividing two units works exactly as expected, N / m = Pa, J / C = V, etc.

        Parameters
        ----------
        lhs : Unit
            Unit by which to divide
        """
        new_multiplier = lhs.multiplier / self.multiplier
        new_godel_frac = lhs.godel_frac / self.godel_frac
        return Unit(new_multiplier, new_godel_frac)

    def __pow__(self, exp: int) -> Unit:
        """Exponentiate a unit
        
        Exponentiating units works as expected. dm ** 3 = L, etc.

        Parameters
        ----------
        lhs : Unit
            Unit by which to divide
        """
        new_multiplier = self.multiplier ** exp
        new_godel_frac = self.godel_frac ** exp
        return Unit(new_multiplier, sympy.Rational(new_godel_frac))

    def __eq__(self, rhs: Unit) -> bool:
        """Check that two units are equal
        
        This only checks that the dimensions of two units are equal, and makes no other guarantees. Newtons are equal to dynes are equal to foot-pounds. DimensionfulQuantity should be used for comparison, and checking equality of two units directly should probably not be done.

        Parameters
        ----------
        rhs : Unit
            Unit to check equality to
        """
        return self.godel_frac - rhs.godel_frac == 0

    @classmethod
    def _from_prefixed_unit(cls, prefix: SIPrefix, unit: Unit) -> Unit:
        """Create a unit from a prefix and a Unit
        
        This is really just a convenience method so that SI prefixes can be defined using the power of 10 by which they differ from the base unit.

        Parameters
        ----------
        prefix : SIPrefix
            Prefix to apply to the unit.

        unit : Unit
            Unit to apply the prefix to
        """
        new_multiplier = unit.multiplier * 10 ** prefix.value
        return cls(new_multiplier, unit.godel_frac)

    @classmethod
    def _single_from_string(cls, str: str) -> Unit:
        """Parse a string corresponding to a single unit to a Unit.
        
        This is simply a helper function for Unit.from_string, and deals with taking string such as "pF" and "ns" and converting them into Units.

        Parameters
        ----------
        str : str
            String to parse
        """
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
        """Parse a string corresponding to a unit or arithmetic combination of units.
        
        Given a unit, or some group of units combined using multiplication, division, and exponention, and parse into a Unit. This parsing is safe, and uses a whitelist to ensure that arbitrary code execution is not possible.

        Parameters
        ----------
        str : str
            String to parse
        """
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
    N = 1000 * SIBaseUnit.Gram * SIBaseUnit.Metre * SIBaseUnit.Second ** -2
    Pa = 1000 * SIBaseUnit.Gram * SIBaseUnit.Metre ** -1 * SIBaseUnit.Second ** -2
    J = 1000 * SIBaseUnit.Gram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -2
    W = 1000 * SIBaseUnit.Gram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -3
    C = SIBaseUnit.Second * SIBaseUnit.Ampere
    V = 1000 * SIBaseUnit.Gram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -3 * SIBaseUnit.Ampere ** -1
    F = 1000 * SIBaseUnit.Gram ** -1 * SIBaseUnit.Metre ** -2 * SIBaseUnit.Second ** 4 * SIBaseUnit.Ampere ** 2
    O = 1000 * SIBaseUnit.Gram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -3 * SIBaseUnit.Ampere ** -2
    Ω = 1000 * SIBaseUnit.Gram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -3 * SIBaseUnit.Ampere ** -2
    S = 1000 * SIBaseUnit.Gram ** -1 * SIBaseUnit.Metre ** -2 * SIBaseUnit.Second ** 3 * SIBaseUnit.Ampere ** 2
    Wb = 1000 * SIBaseUnit.Gram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -2 * SIBaseUnit.Ampere ** -1
    T = 1000 * SIBaseUnit.Gram * SIBaseUnit.Second ** -2 * SIBaseUnit.Ampere ** -1
    H = 1000 *SIBaseUnit.Gram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -2 * SIBaseUnit.Ampere ** -2

    # some common metric units that are not technically SI
    min = 60 * SIBaseUnit.Second
    h = 3600 * SIBaseUnit.Second
    d = 86400 * SIBaseUnit.Second
    au = 149597870700 * SIBaseUnit.Metre
    L = 1e-3 * SIBaseUnit.Metre ** 3
    eV = 1.602176634e-19 * 1000 * SIBaseUnit.Gram * SIBaseUnit.Metre ** 2 * SIBaseUnit.Second ** -2

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
