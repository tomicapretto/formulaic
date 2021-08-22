from enum import Enum
from numbers import Number
from typing import Callable, Iterable, Union

from .term import Term


class Operator:
    """
    Specification for how an operator in a formula string should behave.

    Attributes:
        symbol: The operator for which the configuration applies.
        arity: The number of arguments that this operator consumes.
        precedence: How tightly this operator binds its arguments (the higher
            the number, the more tightly it binds). Operators with higher
            precedence will be evaluated first.
        associativity: One of 'left', 'right', or 'none'; indicating how
            operators of the same precedence should be evaluated in the absence
            of explicit grouping parentheses. If left associative, groups are
            formed from the left [e.g. a % b % c -> ((a % b) % c)]; and
            similarly for right.
        fixity: One of 'prefix', 'infix', or 'postfix'; indicating how the
            operator is positioned relative to its arguments. If 'prefix', the
            operator comes before its arguments; if 'infix', the operator comes
            between its arguments (and there must be exactly two of them); and
            if 'postfix', the operator comes after its arguments.
        to_terms: A callable that maps the arguments pass to the operator to
            an iterable of `Term` instances.
    """

    class Associativity(Enum):
        LEFT = "left"
        RIGHT = "right"
        NONE = "none"

    class Fixity(Enum):
        PREFIX = "prefix"
        INFIX = "infix"
        POSTFIX = "postfix"

    def __init__(
        self,
        symbol: str,
        *,
        arity: int,
        precedence: Number,
        associativity: Union[str, Associativity] = "none",
        fixity: Union[str, Fixity] = "infix",
        to_terms: Callable[..., Iterable[Term]] = None,
    ):
        self.symbol = symbol
        self.arity = arity
        self.precedence = precedence
        self.associativity = associativity
        self.fixity = fixity
        self._to_terms = to_terms

    @property
    def associativity(self):
        return self._associativity

    @associativity.setter
    def associativity(self, associativity):
        self._associativity = Operator.Associativity(associativity or "none")

    @property
    def fixity(self):
        return self._fixity

    @fixity.setter
    def fixity(self, fixity):
        self._fixity = Operator.Fixity(fixity)

    def to_terms(self, *args):
        if self._to_terms is None:
            raise RuntimeError(f"`to_terms` is not implemented for '{self.symbol}'.")
        return self._to_terms(*args)

    def __repr__(self):
        return self.symbol