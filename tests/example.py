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
pprint.pprint(result)

try:
    import parseit.treeify
    graph = parseit.treeify.create_pydot_of_tree(result)
    graph.write_png("tree.png")
except ImportError:
    print "pydot is not installed on this system, so skipping creating the tree.png file"