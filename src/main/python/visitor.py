from typing import Any

from arpeggio import PTNodeVisitor

from utils import add_edge
from utils import add_node
from utils import BUT_DIGIT
from utils import BUT_SPACE
from utils import BUT_WORD
from utils import DIGIT
from utils import Font
from utils import GREEDY
from utils import Line
from utils import merge
from utils import NEGATED
from utils import normal
from utils import order
from utils import REPEATED
from utils import Shape
from utils import SPACE
from utils import Style
from utils import WORD


# noinspection PyMethodMayBeStatic
class RegExVisitor(PTNodeVisitor):

    def visit_regex(self, node, children) -> Any:
        return children[0]

    def visit_alternative(self, node, children) -> Any:
        if len(children) == 1:
            return children[0]

        graph = add_node('alternative', font=Font.ITALIC, shape=Shape.DIAMOND, style=Style.ROUNDED)
        for child in children:
            graph = merge(graph, child)
            graph = add_edge(graph['top'], child['top'], graph)

        return graph

    def visit_sequence(self, node, children) -> Any:
        if len(children) == 1:
            return children[0]

        graph = add_node('sequence', font=Font.ITALIC, shape=Shape.BOX, style=Style.ROUNDED)
        source = graph['top']

        label, style = None, None
        for child in children:
            target = child['top']
            root = child['nodes'][target]

            if root['label'] == 'atom':
                ident = next((k for k in child['edges'][target]), None)
                atom = child['nodes'][ident]
                if label is None:
                    label = atom['label']
                    style = Style.FILLED if 'style' in atom else None
                else:
                    label = label + atom['label']
                    style = style and (Style.FILLED if 'style' in atom else None)

            else:
                if label is not None:
                    node = add_node(label, shape=Shape.BOX, style=style)
                    tgt = node['top']
                    node = merge(node, add_node('atom', font=Font.ITALIC, shape=Shape.ELLIPSE))
                    src = node['top']
                    node = add_edge(src, tgt, node)

                    graph = merge(graph, node)
                    graph = add_edge(source, src, graph)
                    label, style = None, None

                graph = merge(graph, child)
                graph = add_edge(source, target, graph)

        if label is not None:
            node = add_node(label, shape=Shape.BOX, style=style)
            tgt = node['top']
            node = merge(node, add_node('atom', font=Font.ITALIC, shape=Shape.ELLIPSE))
            src = node['top']
            node = add_edge(src, tgt, node)

            graph = merge(graph, node)
            graph = add_edge(source, src, graph)

            # graph = merge(graph, child)
            # graph = add_edge(source, target, graph)

        return graph

    def visit_match(self, node, children) -> Any:
        return children[0]

    def visit_anchor(self, node, children) -> Any:
        return add_node(node.value, shape=Shape.BOX, style=Style.FILLED)

    def visit_backref(self, node, children) -> Any:
        return add_node(node.value, shape=Shape.BOX, style=Style.FILLED)

    def visit_atom(self, node, children) -> Any:
        params = {
            'label': f"atom{children[1]['label'] if len(children) > 1 else ''}",
            'font': Font.ITALIC,
            'shape': Shape.ELLIPSE,
        }
        if len(children) > 1:
            for key, value in children[1].items():
                if key not in ('label', 'line') and value is not None:
                    params[key] = value
        graph = add_node(**params)
        if len(children) > 1 and 'line' in children[1]:
            params = {k: v for k, v in children[1].items() if k != 'style' and v is not None}
            graph = add_edge(graph['top'], graph['top'], graph, **params)

        source, target = graph['top'], children[0]['top']
        graph = merge(graph, children[0])
        graph = add_edge(source, target, graph, )

        return graph

    def visit_character_any(self, node, children) -> Any:
        return add_node(node.value, shape=Shape.BOX, style=Style.FILLED)

    def visit_character_set(self, node, children) -> Any:
        negated = children[0] == '^'
        if negated:
            children = children[1:]

        classes, values = set(), set()
        if children[0] in ['-', ']']:
            values.add(ord(children[0]))
            children = children[1:]
        for child in children:
            if isinstance(child, dict):
                ident = child['top']
                label = child['nodes'][ident]['label']
                try:
                    values.update(order(label))
                except TypeError:
                    classes.add(label)
            else:
                values.update(child)

        graph = add_node(
            f"{'^' if negated else ''}charset",
            font=Font.ITALIC,
            shape=Shape.TRAPEZIUM,
            color=NEGATED if negated else None,
        )
        source = graph['top']

        for class_ in sorted(classes):
            child = add_node(class_, shape=Shape.BOX, style=Style.FILLED)
            graph = merge(graph, child)
            graph = add_edge(source, child['top'], graph)

        for group, symbol in [
            (BUT_SPACE, '\\S'),
            (BUT_DIGIT, '\\D'),
            (BUT_WORD, '\\W'),
            (WORD, '\\w'),
            (DIGIT, '\\d'),
            (SPACE, '\\s'),
        ]:
            if group in values:
                child = add_node(symbol, shape=Shape.BOX, style=Style.FILLED)
                graph = merge(graph, child)
                graph = add_edge(source, child['top'], graph)
                values -= group

        start, last = None, None
        for value in sorted(values):
            if last is None:
                start, last = value, value
            elif value == last + 1:
                last = value
            else:
                label = normal(start) if last == start else f"{normal(start)}-{normal(last)}"
                child = add_node(label, shape=Shape.BOX)
                graph = merge(graph, child)
                graph = add_edge(source, child['top'], graph)
                start, last = None, None

        if last is not None:
            label = normal(start) if last == start else f"{normal(start)}-{normal(last)}"
            child = add_node(label, shape=Shape.BOX)
            graph = merge(graph, child)
            graph = add_edge(source, child['top'], graph)

        return graph

    def visit_character_element(self, node, children) -> Any:
        return children[0]

    def visit_character_category(self, node, children) -> Any:
        return add_node(node.value, shape=Shape.BOX, style=Style.FILLED)

    def visit_character_class(self, node, children) -> Any:
        return add_node(node.value, shape=Shape.BOX, style=Style.FILLED)

    def visit_character_range(self, node, children) -> Any:
        values = sorted({v for c in children for v in c})

        return {i for i in range(values[0], values[-1] + 1)}

    def visit_character(self, node, children) -> Any:
        ident = children[0]['top']
        char = children[0]['nodes'][ident]['label']
        if char == '" "':
            char = ' '

        return order(char)

    def visit_group(self, node, children) -> Any:
        params = {
            'label': f"group{children[1]['label'] if len(children) > 1 else ''}",
            'font': Font.ITALIC,
            'shape': Shape.ELLIPSE,
        }
        if len(children) > 1:
            for key, value in children[1].items():
                if key not in ('label', 'line') and value is not None:
                    params[key] = value
        graph = add_node(**params)
        if len(children) > 1 and 'line' in children[1]:
            params = {k: v for k, v in children[1].items() if k != 'style' and v is not None}
            graph = add_edge(graph['top'], graph['top'], graph, **params)

        source, target = graph['top'], children[0]['top']
        graph = merge(graph, children[0])
        graph = add_edge(source, target, graph, )

        return graph

    def visit_quantifier(self, node, children) -> Any:
        if len(children) > 1 and children[-1] == '?':
            children[0]['label'] += '?'
            children[0]['color'] = GREEDY

        return children[0]

    def visit_zero_or_one(self, node, children) -> Any:
        return {
            'label': '?',
            'style': Style.DASHED,
        }

    def visit_zero_or_more(self, node, children) -> Any:
        return {
            'label': '*',
            'style': Style.DASHED,
            'line': Line.DOT,
            'color': REPEATED,
        }

    def visit_one_or_more(self, node, children) -> Any:
        return {
            'label': '+',
            'line': Line.DOT,
            'color': REPEATED,
        }

    def visit_n_times(self, node, children) -> Any:
        return {
            'label': f"{{{','.join(children)}}}",
            'style': Style.DASHED if int(children[0]) == 0 else None,
            'line': Line.DOT if len(children) > 1 and int(children[1]) > 1 or int(children[0]) > 1 else None,
            'color': REPEATED if len(children) > 1 and int(children[1]) > 1 or int(children[0]) > 1 else None,
        }

    def visit_symbol(self, node, children) -> Any:
        return add_node(normal(ord(node.value)), shape=Shape.BOX)

    def visit_symbol_in_range(self, node, children) -> Any:
        return add_node(normal(ord(node.value)), shape=Shape.BOX)

    def visit_escaped(self, node, children) -> Any:
        return add_node(node.value, shape=Shape.BOX)

    def visit_escaped_in_range(self, node, children) -> Any:
        return add_node(node.value, shape=Shape.BOX)

    def visit_ascii_code(self, node, children) -> Any:
        return add_node(normal(int(node.value[2:], 16)), shape=Shape.BOX)

    def visit_unicode(self, node, children) -> Any:
        return add_node(normal(int(node.value[2:], 16)), shape=Shape.BOX)
