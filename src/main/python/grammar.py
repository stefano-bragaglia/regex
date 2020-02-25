from arpeggio import EOF
from arpeggio import OneOrMore
from arpeggio import Optional
from arpeggio import RegExMatch
from arpeggio import ZeroOrMore


def regex():
    return alternative, EOF


def alternative():
    return sequence, ZeroOrMore('|', sequence)


def sequence():
    return OneOrMore(atom)


def atom():
    return [group, match, backref, anchor]


def group():
    return '(', Optional('?:'), alternative, ')', Optional(quantifier)


def match():
    return [character_set, character_category, character_any, character_class, unicode, character, symbol], \
           Optional(quantifier)


def character_set():
    return '[', Optional('^'), OneOrMore(character_element), ']'


def character_category():
    return RegExMatch(r'\\p\{[a-zA-Z]+\}')


def character_any():
    return '.'


def character_class():
    return ['\\w', '\\W', '\\d', '\\D']


def character_element():
    return [character_range, character_category, character_class]


def character_range():
    return [(unicode, Optional('-', unicode)),
            (character, Optional('-', character)),
            (symbol, Optional('-', symbol))]


def backref():
    return '\\', integer


def anchor():
    return ['\\b', '\\B', '\\A', '\\z', '\\Z', '\\G', '$', '^']


def quantifier():
    return [zero_or_one, zero_or_more, one_or_more, n_times], Optional('?')


def zero_or_one():
    return '?'


def zero_or_more():
    return '*'


def one_or_more():
    return '+'


def n_times():
    return '{', [(',', integer), (integer, Optional(',', Optional(integer)))], '}'


def integer():
    return RegExMatch(r'\d+')


def letters():
    return RegExMatch(r'[a-zA-Z]+')


def symbol():
    return ['\t', '\r', '\n', RegExMatch(r'[\u0020-\uD7FF]'), RegExMatch(r'[\uE000-\uFFFF]')]  # [\x10000-\x10FFFF]


def character():
    return RegExMatch(r'\\x[0-9a-fA-F]{2}')


def unicode():
    return RegExMatch(r'\\u[0-9a-fA-F]{4}')
