from __future__ import print_function
import re
import parseit
import pprint
from future.builtins import input
import time

tokens = {
    "%WHITE": re.compile("\s+"),
    "AOP": re.compile("[+-]"),
    "MOP": re.compile("[*/]"),
    "NUM": re.compile("\d+"),
    "POWER": re.compile("\^"),
    "LETTER": re.compile("[a-z]"),
    "LPAREN": re.compile("\("),
    "RPAREN": re.compile("\)"),
    "DEL": re.compile("del"),
    "PRINT": re.compile("print"),
    "EQUALS": re.compile("="),
}

rules = {
    "root": [["stmt", ["stmt", "*"]]],
    "stmt": [
        ["assign_stmt"],
        ["del_stmt"],
        ["print_stmt"]
    ],
    "assign_stmt": [
        ["LETTER", "EQUALS", "expr"]
    ],
    "del_stmt": [
        ["DEL", "LETTER"]
    ],
    "print_stmt": [
        ["PRINT", "LETTER"]
    ],
    "expr": [
        ["mul_expr"],
        ["expr", "AOP", "mul_expr"]
    ],
    "mul_expr": [
        ["atom"],
        ["mul_expr", "MOP", "atom"]
    ],
    "atom": [
        ["LETTER"],
        ["NUM"],
        ["LPAREN", "expr", "RPAREN"]
    ]
}

input_str = ""
with open("stresstest_in.txt") as f:
    input_str = f.read()

start = time.time()
tree = parseit.parse(input_str, tokens, rules)
end = time.time()
duration = end - start
print("Parsed stresstest_in.txt in {} seconds".format(duration))
pprint.pprint(tree)

try:
    import parseit.treeify
    if input("Do you want to create a tree? [yN]").lower() in ("n", ""):
        exit(0)
    graph = parseit.treeify.create_pydot_of_tree(tree)
    graph.write_png("tree_stress.png")
except ImportError:
    print("pydot is not installed on this system, so skipping creating the tree.png file")
