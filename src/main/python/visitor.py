from typing import Any

from arpeggio import PTNodeVisitor


# noinspection PyMethodMayBeStatic
from utils import as_node


class RegExVisitor(PTNodeVisitor):

    def visit_regex(self, node, children) -> Any:
        return node

    def visit_alternative(self, node, children) -> Any:
        return node

    def visit_sequence(self, node, children) -> Any:
        return node

    def visit_atom(self, node, children) -> Any:
        return node

    def visit_anchor(self, node, children) -> Any:
        return node

    def visit_backref(self, node, children) -> Any:
        return node

    def visit_match(self, node, children) -> Any:
        return node

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
        return node

    def visit_zero_or_one(self, node, children) -> Any:
        return node

    def visit_zero_or_more(self, node, children) -> Any:
        return node

    def visit_one_or_more(self, node, children) -> Any:
        return node

    def visit_n_times(self, node, children) -> Any:
        return node

    def visit_integer(self, node, children) -> Any:
        return node

    def visit_letters(self, node, children) -> Any:
        return node

    def visit_symbol(self, node, children) -> Any:
        return as_node()

    def visit_character(self, node, children) -> Any:
        return node

    def visit_unicode(self, node, children) -> Any:
        return node
