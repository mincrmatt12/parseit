import pprint, re, parseit, collections

import pydot

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


def color_name(name):
    rgb = hash(name) % 255, (hash(name) >> 4) % 255, (hash(name) >> 8) % 255
    rgb_hex = "#" + "".join(hex(x)[2:] for x in rgb)
    light = sum(rgb) / 3.0
    return rgb_hex, "#000000" if light > 127 else "#FAFAFA"


graph = pydot.Dot(graph_type="digraph")

n = 0


def add_nodes(graph, result):
    global n
    n += 1
    root_node = pydot.Node("{}{}".format(result[0], n), label=result[0], style="filled", fillcolor=color_name(result[0])[0], fontcolor=color_name(result[0])[1])
    graph.add_node(root_node)
    for child in result[1]:
        if child[0].isupper():
            child_node = pydot.Node("TOKEN{}".format(n), label="{}('{}')".format(child[0], child[1]))
            n += 1
            graph.add_node(child_node)
            graph.add_edge(pydot.Edge(root_node, child_node))
        else:
            child_node = add_nodes(graph, child)
            graph.add_node(child_node)
            graph.add_edge(pydot.Edge(root_node, child_node))
    return root_node


add_nodes(graph, result)

graph.write_png("tree.png")
