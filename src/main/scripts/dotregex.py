#!/usr/bin/env python3
import os
import re

from arpeggio import ParserPython

from grammar import regex

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
        try:
            parse_tree = parser.parse(test_expr)
        except Exception as e:
            print(e)
        else:
            safe = re.sub(r'\W', '_', test_expr)
            os.system(f'dot -Tpng -o{safe}.png regex_parse_tree.dot')
        print('\n' * 5)
    print('Done.')
