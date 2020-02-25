import itertools
import json
from copy import deepcopy
from enum import Enum
from typing import Any
from typing import Dict

Graph = Dict[str, Any]

counter = itertools.count()


class Font(Enum):
    NORMAL = 'times'
    ITALIC = 'times italic'


class Shape(Enum):
    BOX = 'box'
    DIAMOND = 'diamond'
    ELLIPSE = 'ellipse'
    POLYGON = 'polygon'


class Style(Enum):
    DASHED = 'dashed'
    FILLED = 'filled'
    ROUNDED = 'rounded'


class Line(Enum):
    DOT = 'dot'


class Color(Enum):
    RED = 'red'


def empty() -> Graph:
    return {
        'top': None,
        'nodes': {},
        'edges': {},
    }


def as_node(
        label: Any,
        graph: Dict = None,
        font: Font = None,
        shape: Shape = None,
        style: Style = None,
        color: Color = None,
) -> Graph:
    if graph is None:
        graph = empty()

    ident = next(counter)
    nodes = graph.setdefault('nodes', {})
    node = nodes.setdefault(ident, {'label': json.dumps(label)})
    if font:
        node['fontname'] = font.value
    if shape:
        node['shape'] = shape.value
    if style:
        node['style'] = style.value
    if color:
        node['color'] = color.value

    return graph


def add_edge(
        source: int,
        target: int,
        graph: Graph,
        label: Any = None,
        line: Line = None,
        color: Color = None,
) -> Graph:
    edges = graph.setdefault('edges', {})
    edge = edges.setdefault('source', {}).setdefault('target', {})
    if label:
        edge['label'] = json.dumps(label)
    if color:
        edge['fontcolor'] = color
    if line:
        edge['shape'] = line
    if color:
        edge['color'] = color
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


def convert(graph: Graph) -> str:
    lines = []
    for source, node in sorted(graph.get('nodes', {}).items(), reverse=True):
        params = ' '.join(f'{k}={json.dumps(v)}' for k, v in node.items())
        lines.append(f"\t{source} [{params}];")

        neighbours = graph.get('edges', {}).get(source, {})
        for target, edge in sorted(neighbours.items(), reverse=True):
            if not edge:
                lines.append(f"\t{source} -> {target};")
            else:
                params = ' '.join(f'{k}={json.dumps(v)}' for k, v in edge.items())
                lines.append(f"\t{source} -> {target} [{params}];")

        lines.append('')
    lines = '\n'.join(lines)

    return f"digraph regex_graph {{\n{lines}\n\tfontname=\"times\"\n}}\n"
