from arpeggio import OneOrMore
from arpeggio import Optional

from arpeggio import RegExMatch
from arpeggio import ZeroOrMore


def regex():
    return Optional(start_of_string_anchor), expression


def expression():
    return subexpression, ZeroOrMore('|', expression)


# Anything that can be on one side of the alternation.
def subexpression():
    return OneOrMore(subexpression_item)


def subexpression_item():
    return [match, group, anchor, backreference]


# Grouping Constructs
def group():
    return '(', Optional(group_non_capturing_modifier), expression, ')', Optional(quantifier)


def group_non_capturing_modifier():
    return '?:'


# Match
def match():
    return match_item, Optional(quantifier)


def match_item():
    return [match_any_character, match_character_class, match_character]


def match_any_character():
    return '.'


def match_character_class():
    return [character_group, character_class, character_class_from_unicode_category]


def match_character():
    return char


# Character Classes
def character_group():
    return '[', Optional(character_group_negative_modifier), OneOrMore(character_group_item), ']'


def character_group_negative_modifier():
    return '^'


def character_group_item():
    return [
        character_class, character_class_from_unicode_category, character_range, char_excluding_closed_square_bracket]


def character_class():
    return [
        character_class_any_word, character_class_any_word_inverted, character_class_any_decimal_digit,
        character_class_any_decimal_digit_inverted]


def character_class_any_word():
    return '\\w'


def character_class_any_word_inverted():
    return '\\W'


def character_class_any_decimal_digit():
    return '\\d'


def character_class_any_decimal_digit_inverted():
    return '\\D'


def character_class_from_unicode_category():
    return '\\p{', unicode_category_name, '}'


def unicode_category_name():
    return letters


def character_range():
    return char, Optional('-', char)


# Quantifiers
def quantifier():
    return quantifier_type, Optional(lazy_modifier)


def quantifier_type():
    return [zero_or_more_quantifier, one_or_more_quantifier, zero_or_one_quantifier, range_quantifier]


def lazy_modifier():
    return '?'


def zero_or_more_quantifier():
    return '*'


def one_or_more_quantifier():
    return '+'


def zero_or_one_quantifier():
    return '?'


def range_quantifier():
    return '{', range_quantifier_lower_bound, Optional(',', Optional(range_quantifier_upper_bound)), '}'


def range_quantifier_lower_bound():
    return integer


def range_quantifier_upper_bound():
    return integer


# Anchors
def start_of_string_anchor():
    return '^'


def anchor():
    return [anchor_word_boundary, anchor_non_word_boundary, anchor_start_of_string_only,
            anchor_end_of_string_only_not_newline, anchor_end_of_string_only, anchor_previous_match_end,
            anchor_end_of_string]


def anchor_word_boundary():
    return '\\b'


def anchor_non_word_boundary():
    return '\\B'


def anchor_start_of_string_only():
    return '\\A'


def anchor_end_of_string_only_not_newline():
    return '\\z'


def anchor_end_of_string_only():
    return '\\Z'


def anchor_previous_match_end():
    return '\\G'


def anchor_end_of_string():
    return '$'


# Backreferences

def backreference():
    return '\\', integer


# Misc
def integer():
    return RegExMatch(r'[0-9]+')


def letters():
    return RegExMatch(r'[a-zA-Z]+')


def char():
    # return [RegExMatch(r'\#x9'), RegExMatch(r'\#xA'), RegExMatch(r'\#xD'), RegExMatch(r'[\#x20-\#xD7FF]'),
    #         RegExMatch(r'[\#xE000-\#xFFFD]'), RegExMatch(r'[\#x10000-\#x10FFFF]')]
    return [RegExMatch(r'\u0009'), RegExMatch('\u000A'), RegExMatch('\u000D'),
            RegExMatch(r'[\u0020-\uD7FF]'), RegExMatch(r'[\uE000-\uFFFD]'),
            # RegExMatch(r'[\u10000-\u10FFFF]')
            ]


def char_excluding_closed_square_bracket():
    return [RegExMatch(r'\u0009'), RegExMatch(r'\u000A'), RegExMatch(r'\u000D'),
            RegExMatch(r'[\u0020-\u005C]'), RegExMatch(r'[\u005E-\uD7FF]'), RegExMatch(r'[\uE000-\uFFFD]'),
            # RegExMatch(r'[\u10000-\u10FFFF]')
            ]
