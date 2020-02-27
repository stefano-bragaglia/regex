import itertools
import json
import re
from copy import deepcopy
from enum import Enum
from typing import Any
from typing import Dict
from typing import Set

Range = Set[int]

unicode = re.compile(r'\\u([0-9A-Fa-f]{4})')
ascii_code = re.compile(r'\\x([0-9A-Fa-f]{2})')
escape = re.compile(r'\\(.)')

DIGIT = {i for i in range(ord('0'), ord('9') + 1)}
BUT_DIGIT = {i for i in range(0, 65536)} - DIGIT

SPACE = {ord('\t'), ord('\n'), ord('\v'), ord('\f'), ord('\r'), ord(' ')}
BUT_SPACE = {i for i in range(0, 65536)} - SPACE

UPPERCASE = {i for i in range(ord('A'), ord('A') + 1)}
LOWERCASE = {i for i in range(ord('a'), ord('z') + 1)}
UNDERSCORE = {ord('_')}
WORD = {*UPPERCASE, *LOWERCASE, *DIGIT, *UNDERSCORE}
BUT_WORD = {i for i in range(0, 65536)} - WORD


def order(char: str) -> Range:
    match = unicode.match(char)
    if match:
        return {int(match.group(1), 16)}

    match = ascii_code.match(char)
    if match:
        return {int(match.group(1), 16)}

    match = escape.match(char)
    if match and match.group(1) == 'd':
        return DIGIT

    if match and match.group(1) == 'D':
        return BUT_DIGIT

    if match and match.group(1) == 's':
        return SPACE

    if match and match.group(1) == 'S':
        return BUT_SPACE

    if match and match.group(1) == 'w':
        return WORD

    if match and match.group(1) == 'W':
        return BUT_WORD

    if match and match.group(1) == 't':
        return {ord('\t')}

    if match and match.group(1) == 'n':
        return {ord('\n')}

    if match and match.group(1) == 'v':
        return {ord('\v')}

    if match and match.group(1) == 'f':
        return {ord('\f')}

    if match and match.group(1) == 'r':
        return {ord('\r')}

    if match and match.group(1) == ' ':
        return {ord(' ')}

    if match and match.group(1) == ']':
        return {ord(']')}

    if match and match.group(1) == '-':
        return {ord('-')}

    if match:
        return {ord(match.group(1))}

    return {ord(char)}


def normal(value: int) -> str:
    if value == 9:
        return '\\t'

    if value == 10:
        return '\\n'

    if value == 11:
        return '\\v'

    if value == 12:
        return '\\f'

    if value == 13:
        return '\\r'

    if value == 32:
        return '" "'

    return chr(value)


Graph = Dict[str, Any]

counter = itertools.count()


class Font(Enum):
    NORMAL = 'times'
    ITALIC = 'times italic'


class Shape(Enum):
    BOX = 'box'
    DIAMOND = 'diamond'
    ELLIPSE = 'ellipse'
    TRAPEZIUM = 'trapezium'


class Style(Enum):
    DASHED = 'dashed'
    FILLED = 'filled'
    ROUNDED = 'rounded'


class Line(Enum):
    DOT = 'dot'


class Color(Enum):
    BLUE = 'blue'
    GREEN = 'green'
    RED = 'red'


GREEDY = Color.BLUE
NEGATED = Color.RED
REPEATED = Color.GREEN


def empty() -> Graph:
    return {
        'top': None,
        'nodes': {},
        'edges': {},
    }


def add_node(
        label: str,
        graph: Dict = None,
        font: Font = None,
        shape: Shape = None,
        style: Style = None,
        color: Color = None,
        **params: Any,
) -> Graph:
    if graph is None:
        graph = empty()

    ident = next(counter)
    nodes = graph.setdefault('nodes', {})
    node = nodes.setdefault(ident, {'label': label})
    if font:
        node['fontname'] = font.value
    if shape:
        node['shape'] = shape.value
    if style:
        node['style'] = style.value
    if color:
        node['color'] = color.value
    for key, value in params.items():
        if value is not None:
            node[key] = json.dumps(value)
    graph['top'] = ident

    return graph


def add_edge(
        source: int,
        target: int,
        graph: Graph,
        label: str = None,
        line: Line = None,
        color: Color = None,
) -> Graph:
    edges = graph.setdefault('edges', {})
    edge = edges.setdefault(source, {}).setdefault(target, {})
    if label:
        edge['label'] = label
    if color:
        edge['fontcolor'] = color.value
    if line:
        edge['shape'] = line.value
    if color:
        edge['color'] = color.value
    if graph['top'] == target:
        graph['top'] = source

    return graph


def set_top(
        root: int,
        graph: Graph,
) -> Graph:
    graph['top'] = root

    return graph


def merge(
        graph1: Graph,
        graph2: Graph,
) -> Graph:
    top = max([i for i in {g.get('top', None) for g in (graph1, graph2)} if i], default=None)

    nodes = deepcopy(graph1.get('nodes', {}))
    for ident, content in graph2.get('nodes', {}).items():
        node = nodes.setdefault(ident, {})
        for key, value in content.items():
            node[key] = value

    edges = deepcopy(graph1.get('edges', {}))
    for source, neighbours in graph2.get('edges', {}).items():
        for target, content in neighbours.items():
            edge = edges.setdefault(source, {}).setdefault(target, {})
            for key, value in content.items():
                edge[key] = value

    return {
        'top': top,
        'nodes': nodes,
        'edges': edges,
    }


def convert(graph: Graph, title: str = None) -> str:
    lines = []
    for source, node in graph.get('nodes', {}).items():
        params = ' '.join(f'{k}={json.dumps(v)}' for k, v in node.items())
        lines.append(f"\t{source} [{params}];")

        neighbours = graph.get('edges', {}).get(source, {})
        for target, edge in neighbours.items():
            if not edge:
                lines.append(f"\t{source} -> {target};")
            else:
                params = ' '.join(f'{k}={json.dumps(v)}' for k, v in edge.items())
                lines.append(f"\t{source} -> {target} [{params}];")

        lines.append('')
    if 'title':
        lines.append(f"\tlabel=\"{title}\";")
        lines.append(f"\tlabelloc=\"t\";")
    lines = '\n'.join(lines)

    return f"digraph regex_graph {{\n{lines}\n\tfontname=\"times\";\n}}\n"
