#!/usr/bin/env python3
import os
import re

from arpeggio import ParserPython
from arpeggio import visit_parse_tree

from grammar import regex
from utils import convert
from visitor import RegExVisitor

if __name__ == '__main__':
    parser = ParserPython(regex, ws='\t ', debug=False)
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
        print('-' * len(test_expr))
        print()

        parse_tree = parser.parse(test_expr)
        result = visit_parse_tree(parse_tree, RegExVisitor(debug=False))
        content = convert(result)
        print(content)

        safe = re.sub(r'\W', '_', test_expr)
        with open(f'{safe}.dot', 'w') as file:
            file.write(content)
        os.system(f'dot -Tpng -o{safe}.png {safe}.dot')
        print('\n' * 3)

    print('Done.')
