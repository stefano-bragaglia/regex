import itertools
from copy import deepcopy
from json import dumps
from typing import Any
from typing import Dict

from arpeggio import OneOrMore
from arpeggio import Optional
from arpeggio import PTNodeVisitor
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
    return character


# Character Classes
def character_group():
    return '[', Optional(character_group_negative_modifier), OneOrMore(character_group_item), ']'


def character_group_negative_modifier():
    return '^'


def character_group_item():
    return [
        character_class, character_class_from_unicode_category, character_range,
        character_excluding_closed_square_bracket]


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
    return character, Optional('-', character)


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


def character():
    # return [RegExMatch(r'\#x9'), RegExMatch(r'\#xA'), RegExMatch(r'\#xD'), RegExMatch(r'[\#x20-\#xD7FF]'),
    #         RegExMatch(r'[\#xE000-\#xFFFD]'), RegExMatch(r'[\#x10000-\#x10FFFF]')]
    return [RegExMatch(r'\u0009'), RegExMatch('\u000A'), RegExMatch('\u000D'),
            RegExMatch(r'[\u0020-\uD7FF]'), RegExMatch(r'[\uE000-\uFFFD]'),
            # RegExMatch(r'[\u10000-\u10FFFF]')
            ]


def character_excluding_closed_square_bracket():
    return [RegExMatch(r'\u0009'), RegExMatch(r'\u000A'), RegExMatch(r'\u000D'),
            RegExMatch(r'[\u0020-\u005C]'), RegExMatch(r'[\u005E-\uD7FF]'), RegExMatch(r'[\uE000-\uFFFD]'),
            # RegExMatch(r'[\u10000-\u10FFFF]')
            ]


# noinspection PyMethodMayBeStatic
class RegExVisitor(PTNodeVisitor):

    def visit_regex(self, node, children) -> Any:
        if len(children) == 1:
            return children[0]

        # TODO else probably don't needed?
        return node

    def visit_expression(self, node, children) -> Any:
        graph = create_node(
            'alternative',
            fontname=ITALIC,
            shape=DIAMOND,
            style=ROUNDED,
        )
        ident = graph['top']
        for child in children:
            graph = create_edge(ident, child['top'], graph=merge(graph, child))
        graph['top'] = ident

        return graph

    # Anything that can be on one side of the alternation.
    def visit_subexpression(self, node, children) -> Any:
        graph = create_node(
            'sequence',
            fontname=ITALIC,
            shape=BOX,
            style=ROUNDED,
        )
        ident = graph['top']
        for child in children:
            graph = create_edge(ident, child['top'], graph=merge(graph, child))
        graph['top'] = ident

        return graph

    def visit_subexpression_item(self, node, children) -> Any:
        return children[0]

    # Grouping Constructs
    def visit_group(self, node, children) -> Any:
        return node

    def visit_group_non_capturing_modifier(self, node, children) -> Any:
        return node

    # Match
    def visit_match(self, node, children) -> Any:
        graph = create_node(
            'atom',
            fontname=ITALIC,
            shape=ELLIPSE,
            graph=empty(),
        ) if len(children) == 1 else children[1]
        ident = graph['top']
        graph = create_edge(ident, children[0]['top'], graph=merge(graph, children[0]))
        graph['top'] = ident

        return graph

    def visit_match_item(self, node, children) -> Any:
        return children[0]

    def visit_match_any_character(self, node, children) -> Any:
        return node

    def visit_match_character_class(self, node, children) -> Any:
        return node

    def visit_match_character(self, node, children) -> Any:
        return create_node(
            dumps(children[0]),
            shape=BOX,
            graph=empty(),
        )

    # Character Classes
    def visit_character_group(self, node, children) -> Any:
        return node

    def visit_character_group_negative_modifier(self, node, children) -> Any:
        return node

    def visit_character_group_item(self, node, children) -> Any:
        return node

    def visit_character_class(self, node, children) -> Any:
        return node

    def visit_character_class_any_word(self, node, children) -> Any:
        return node

    def visit_character_class_any_word_inverted(self, node, children) -> Any:
        return node

    def visit_character_class_any_decimal_digit(self, node, children) -> Any:
        return node

    def visit_character_class_any_decimal_digit_inverted(self, node, children) -> Any:
        return node

    def visit_character_class_from_unicode_category(self, node, children) -> Any:
        return node

    def visit_unicode_category_name(self, node, children) -> Any:
        return node

    def visit_character_range(self, node, children) -> Any:
        return node

    # Quantifiers
    def visit_quantifier(self, node, children) -> Any:
        return children[0]

    def visit_quantifier_type(self, node, children) -> Any:
        return children[0]

    def visit_lazy_modifier(self, node, children) -> Any:
        return node

    def visit_zero_or_more_quantifier(self, node, children) -> Any:
        graph = create_node(
            'atom*',
            fontname=ITALIC,
            shape=ELLIPSE,
            style=DASHED,
            graph=empty(),
        )
        return create_edge(
            graph['top'],
            graph['top'],
            label='*',
            shape=DOT,
            color=RED,
            graph=graph,
        )

    def visit_one_or_more_quantifier(self, node, children) -> Any:
        graph = create_node(
            'atom+',
            fontname=ITALIC,
            shape=ELLIPSE,
            graph=empty(),
        )

        return create_edge(
            graph['top'],
            graph['top'],
            label='+',
            shape=DOT,
            color=RED,
            graph=graph,
        )

    def visit_zero_or_one_quantifier(self, node, children) -> Any:
        return create_node(
            'atom?',
            fontname=ITALIC,
            shape=ELLIPSE,
            style=DASHED,
            graph=empty(),
        )

    def visit_range_quantifier(self, node, children) -> Any:
        graph = create_node(
            f"atom{{{','.join(children)}}}",
            fontname=ITALIC,
            shape=ELLIPSE,
            style=DASHED if int(children[0]) < 1 else None,
            graph=empty(),
        )

        return create_edge(
            graph['top'],
            graph['top'],
            f"{{{','.join(children)}}}",
            shape=DOT if max(int(c) for c in children) else None,
            color=RED if max(int(c) for c in children) else None,
            graph=graph,
        )

    # Anchors
    def visit_start_of_string_anchor(self, node, children) -> Any:
        return node

    def visit_anchor(self, node, children) -> Any:
        return node

    def visit_anchor_word_boundary(self, node, children) -> Any:
        return node

    def visit_anchor_non_word_boundary(self, node, children) -> Any:
        return node

    def visit_anchor_start_of_string_only(self, node, children) -> Any:
        return node

    def visit_anchor_end_of_string_only_not_newline(self, node, children) -> Any:
        return node

    def visit_anchor_end_of_string_only(self, node, children) -> Any:
        return node

    def visit_anchor_previous_match_end(self, node, children) -> Any:
        return node

    def visit_anchor_end_of_string(self, node, children) -> Any:
        return node

    # Backreferences
    def visit_backreference(self, node, children) -> Any:
        return node

    # Misc
    def visit_integer(self, node, children) -> Any:
        return node

    def visit_letters(self, node, children) -> Any:
        return node


ITALIC = 'times italic'
BOX = 'box'
DIAMOND = 'diamond'
ELLIPSE = 'ellipse'
DASHED = 'dashed'
DOT = 'dot'
ROUNDED = 'rounded'
RED = 'red'

counter = itertools.count()


def empty() -> Dict:
    return {'top': None, 'nodes': {}, 'edges': {}}


def create_node(
        label: str,
        fontname: str = None,
        shape: str = None,
        style: str = None,
        color: str = None,
        graph: Dict = None,
) -> Dict:
    if graph is None:
        graph = empty()

    ident = next(counter)
    graph['top'] = ident
    node = graph['nodes'].setdefault(ident, {'label': label})
    if fontname:
        node['fontname'] = fontname
    if shape:
        node['shape'] = shape
    if style:
        node['style'] = style
    if color:
        node['color'] = color

    return graph


def create_edge(
        source: int,
        target: int,
        label: str = None,
        shape: str = None,
        color: str = None,
        graph: Dict = None,
) -> Dict:
    if graph is None:
        graph = empty()

    edge = graph['edges'].setdefault(source, {}).setdefault(target, {})
    if label:
        edge['label'] = label
    if shape:
        edge['shape'] = shape
    if color:
        edge['color'] = color
    if graph['top'] == target:
        graph['top'] = source

    return graph


def merge(graph1: Dict, graph2: Dict) -> Dict:
    nodes = deepcopy(graph1['nodes'])
    for ident, node in graph2['nodes'].items():
        nodes[ident] = node
    edges = deepcopy(graph1['edges'])
    for source, tail in graph2['edges'].items():
        for target, content in tail.items():
            edge = edges.setdefault(source, dict()).setdefault(target, dict())
            for key, value in content.items():
                edge[key] = value

    return {'top': max(i for i in (graph1['top'], graph2['top']) if i is not None), 'nodes': nodes, 'edges': edges}


def convert(graph: Dict) -> str:
    nodes = []
    for ident, node in graph.get('nodes', dict()).items():
        params = ' '.join(f'{l}={dumps(v)}' for l, v in node.items())
        nodes.append(f"\t{ident} [{params}];")
    nodes = '\n'.join(nodes)
    if nodes:
        nodes += '\n'

    space = '\n' if graph['nodes'] and graph['edges'] else ''

    edges = []
    for source, adjacency in graph.get('edges', dict()).items():
        for target, edge in adjacency.items():
            if edge:
                params = ' '.join(f'{l}={dumps(v)}' for l, v in edge.items())
                edges.append(f"\t{source} -> {target} [{params}];")
            else:
                edges.append(f"\t{source} -> {target};")
    edges = '\n'.join(edges)
    if edges:
        edges += '\n'

    return f"""digraph regex_graph {{\n{nodes}{space}{edges}\n\tfontname="times"\n}}\n"""
