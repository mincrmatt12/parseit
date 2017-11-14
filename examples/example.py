from __future__ import print_function
import pprint, re, parseit, collections

token_types = {
    "OP": re.compile("[+-]"),
    "NUM": re.compile("\d+"),
    "POWER": re.compile("\^"),
    "LETTER": re.compile("[a-z]"),
    "LPAREN": re.compile("\("),
    "RPAREN": re.compile("\)"),
    "%WHITE": re.compile("[ \t]+"),
}
rules = collections.OrderedDict(
    poly_expr=[
        ["multi_poly"],
        ["LPAREN", "multi_poly", "RPAREN", ["OP", "LPAREN", "multi_poly", "RPAREN", "*"]]
    ],
    multi_poly=[
        ["LPAREN", "multi_poly", "RPAREN", "LPAREN", "multi_poly", "RPAREN"],
        ["NUM", "LPAREN", "polynomial", "RPAREN"],
        ["polynomial"]
    ],
    polynomial=[
        ["term", ["OP", "term", "*"]]
    ],
    term=[
        [["NUM", "?"], ["var", "*"]]
    ],
    var=[
        ["LETTER", ["POWER", "NUM", "?"]]
    ]
)
result = parseit.parse("((2(1ab + c^3))(2ab^4 + a - 3)) + (2ab + 3a^4 - 2)", token_types, rules, "poly_expr")
# expected result is: ('poly_expr',
# [('multi_poly',
#   [('multi_poly',
#     [('NUM', '2', 2),
#      ('polynomial',
#       [('term',
#         [('NUM', '1', 4),
#          ('var', [('LETTER', 'a', 5)]),
#          ('var', [('LETTER', 'b', 6)])]),
#        ('OP', '+', 8),
#        ('term', [('var', [('LETTER', 'c', 10), ('NUM', '3', 12)])])])]),
#    ('multi_poly',
#     [('polynomial',
#       [('term',
#         [('NUM', '2', 16),
#          ('var', [('LETTER', 'a', 17)]),
#          ('var', [('LETTER', 'b', 18), ('NUM', '4', 20)])]),
#        ('OP', '+', 22),
#        ('term', [('var', [('LETTER', 'a', 24)])]),
#        ('OP', '-', 26),
#        ('term', [('NUM', '3', 28)])])])]),
#  ('OP', '+', 32),
#  ('multi_poly',
#   [('polynomial',
#     [('term',
#       [('NUM', '2', 35),
#        ('var', [('LETTER', 'a', 36)]),
#        ('var', [('LETTER', 'b', 37)])]),
#      ('OP', '+', 39),
#      ('term',
#       [('NUM', '3', 41),
#        ('var', [('LETTER', 'a', 42), ('NUM', '4', 44)])]),
#      ('OP', '-', 46),
#      ('term', [('NUM', '2', 48)])])])])
pprint.pprint(result)

try:
    import parseit.treeify

    graph = parseit.treeify.create_pydot_of_tree(result)
    graph.write_png("tree.png")
except ImportError:
    print("pydot is not installed on this system, so skipping creating the tree.png file")
