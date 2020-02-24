import os
import re

from arpeggio import EOF
from arpeggio import OneOrMore
from arpeggio import Optional
from arpeggio import ParserPython
from arpeggio import RegExMatch
from arpeggio import ZeroOrMore


def regex():
    return alternative, EOF


def alternative():
    return sequence, ZeroOrMore('|', sequence)


def sequence():
    return OneOrMore(atom)


def atom():
    return [anchor, backref, match, group]


def anchor():
    return ['\\b', '\\B', '\\A', '\\z', '\\Z', '\\G', '$', '^']


def backref():
    return '\\', integer


def match():
    return ['.', character_class, character_category, character_set, symbol, character, unicode], Optional(quantifier)


def character_class():
    return ['\\w', '\\W', '\\d', '\\D']


def character_category():
    return RegExMatch(r'\\p\{[a-zA-Z]+\}')


def character_set():
    return '[', Optional('^'), OneOrMore(character_elem), ']'


def character_elem():
    return [character_class, character_category, character_range]  # | Char /* excluding ] */


def character_range():
    return [(symbol, Optional('-', symbol)),
            (character, Optional('-', character)),
            (unicode, Optional('-', unicode))]


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


if __name__ == '__main__':
    parser = ParserPython(regex, ws='\t ', debug=True)
    os.system(f'dot -Tpng -oregex_model.png regex_parser_model.dot')
    for test_expr in (
            "abc?",
            "ab+c",
            "(ab)+c",
            "[^-a\\-f-z\"\\]aaaa-]?",
            "abc|d",
            "a?",
            ".*?(a|b){,9}?",
            "(XYZ)|(123)",
    ):
        print(test_expr)
        print('=' * len(test_expr))
        parse_tree = parser.parse(test_expr)
        safe = re.sub(r'\W', '_', test_expr)
        os.system(f'dot -Tpng -o{safe}.png regex_parse_tree.dot')
        print('\n' * 5)
    print('Done.')
