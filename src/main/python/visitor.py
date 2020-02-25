import json
from typing import Any

from arpeggio import PTNodeVisitor

from utils import add_edge
from utils import add_node
from utils import Font
from utils import merge
from utils import set_top
from utils import Shape
from utils import Style


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
        for child in children:
            graph = merge(graph, child)
            graph = add_edge(graph['top'], child['top'], graph)

        return graph

    def visit_atom(self, node, children) -> Any:
        return children[0]

    def visit_anchor(self, node, children) -> Any:
        return node

    def visit_backref(self, node, children) -> Any:
        return node

    def visit_match(self, node, children) -> Any:
        graph = add_node(
            'atom',
            font=Font.ITALIC,
            shape=Shape.ELLIPSE,
        ) if len(children) == 1 else children[1]
        ident = graph['top']
        graph = add_edge(
            ident,
            children[0]['top'],
            merge(graph, children[0]),
        )
        set_top(ident, graph)

        return graph

    def visit_character_class(self, node, children) -> Any:
        return node

    def visit_character_category(self, node, children) -> Any:
        return node

    def visit_character_set(self, node, children) -> Any:
        return node

    def visit_character_elem(self, node, children) -> Any:
        return node

    def visit_character_range(self, node, children) -> Any:
        return node

    def visit_group(self, node, children) -> Any:
        return node

    def visit_quantifier(self, node, children) -> Any:
        graph = children[0]
        if len(children) > 1 and children[1] == '?':
            graph['filled'] = Style.FILLED.value

        return graph

    def visit_zero_or_one(self, node, children) -> Any:
        return add_node(
            'atom?',
            font=Font.ITALIC,
            shape=Shape.ELLIPSE,
            style=Style.DASHED,
            min=0,
            max=1,
        )

    def visit_zero_or_more(self, node, children) -> Any:
        return add_node(
            'atom*',
            font=Font.ITALIC,
            shape=Shape.ELLIPSE,
            style=Style.DASHED,
            min=0,
        )

    def visit_one_or_more(self, node, children) -> Any:
        return add_node(
            'atom+',
            font=Font.ITALIC,
            shape=Shape.ELLIPSE,
            style=Style.DASHED,
            min=1,
        )

    def visit_n_times(self, node, children) -> Any:
        min = None if children[1] == ',' else children[1]
        max = None if children[-1] == ',' else children[-1]

        return add_node(
            f"atom{''.join(children)}",
            font=Font.ITALIC,
            shape=Shape.ELLIPSE,
            style=Style.DASHED,
            min=min,
            max=max,
        )

    # def visit_integer(self, node, children) -> Any:
    #     return node

    # def visit_letters(self, node, children) -> Any:
    #     return node

    def visit_symbol(self, node, children) -> Any:
        return add_node(json.dumps(children[0]), shape=Shape.BOX)

    def visit_character(self, node, children) -> Any:
        return node

    def visit_unicode(self, node, children) -> Any:
        return node
