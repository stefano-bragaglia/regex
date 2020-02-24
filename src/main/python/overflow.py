from arpeggio import Optional
from arpeggio import RegExMatch
from arpeggio import ZeroOrMore


class Multiplicity(object):

    def __init__(self, min_occurs: int = 1, max_occurs: int = 1):
        self._min_occurs = min_occurs
        self._max_occurs = max_occurs
        self._greedy = True

    @property
    def min_occurs(self) -> int:
        return self._min_occurs

    @property
    def max_occurs(self) -> int:
        return self._max_occurs

    @property
    def greedy(self) -> bool:
        return self._greedy

    def is_unbounded(self) -> bool:
        return self._max_occurs is None or self._max_occurs < 0

    def is_repeating(self) -> bool:
        return self._max_occurs is None or self._max_occurs > 1


def expression():
    return alternative, ZeroOrMore('|', alternative)


def alternative():
    return atom, Optional(quantifier)


def atom():
    return [group, charset, any_char, start_of, end_of]  # TODO literals?


def group():
    return '(', expression, ')'


def charset():
    return '[', ']'


def quantifier():
    return ['?', '+', '*', ('{', Optional(integer, ','), integer, '}')]


def integer():
    return RegExMatch(r'[0-9]+')
