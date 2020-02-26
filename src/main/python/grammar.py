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
    return OneOrMore(match)


def match():
    return [anchor, backref, atom, group]


def anchor():
    return RegExMatch(r'\$|\^|\\[ABbGZz]')


def backref():
    return RegExMatch(r'\\\d+')


def atom():
    return [character_any, character_set, character_category, character_class, unicode, ascii_code, symbol, escaped], \
           Optional(quantifier)


def character_any():
    return RegExMatch(r'\.')


def character_set():
    return '[', Optional('^'), OneOrMore(character_element), ']'


def character_element():
    return [character_category, character_class, character_range]


def character_category():
    return RegExMatch(r'\\p\{[A-Za-z]+\}')


def character_class():
    return RegExMatch(r'\\[DdSsWw]')


def character_range():
    return character, Optional('-', character)


def character():
    return [unicode, ascii_code, symbol_in_range, escaped]


def group():
    return '(', Optional('?:'), alternative, ')', Optional(quantifier)


def quantifier():
    return [zero_or_one, zero_or_more, one_or_more, n_times], Optional('?')


def zero_or_one():
    return '?'


def zero_or_more():
    return '*'


def one_or_more():
    return '+'


def n_times():
    return '{', RegExMatch(r'\d+'), Optional(',', RegExMatch(r'\d+')), '}'


def symbol():
    return RegExMatch(r'[^$()*+,.?\[\]^{|}]')


def symbol_in_range():
    return RegExMatch(r'[^\[\]\-]')


def escaped():
    return RegExMatch(r'\\[^ABbDdGSsuWwxZz]')


def ascii_code():
    return RegExMatch(r'\\x[0-9a-fA-F]{2}?')


def unicode():
    return RegExMatch(r'\\u[0-9a-fA-F]{4}?')
