from __future__ import division
from builtins import hex
from past.utils import old_div
import pydot


def color_name(name):
    rgb = hash(name) % 255, (hash(name) >> 4) % 255, (hash(name) >> 8) % 255
    rgb_hex = "#" + "".join(hex(x)[2:] for x in rgb)
    light = old_div(sum(rgb), 3.0)
    return rgb_hex, "#000000" if light > 127 else "#FAFAFA"


n = 0


def add_nodes(graph, result):
    global n
    n += 1
    root_node = pydot.Node("{}{}".format(result[0], n), label=result[0], style="filled",
                           fillcolor=color_name(result[0])[0], fontcolor=color_name(result[0])[1])
    graph.add_node(root_node)
    for child in result[1]:
        if child[0].isupper():
            child_node = pydot.Node("TOKEN{}".format(n), label="{}('{}')".format(child[0], child[1]),
                                    fillcolor=color_name(child[0])[0], style="filled", fontcolor=color_name(child[0])[1])
            n += 1
            graph.add_node(child_node)
            graph.add_edge(pydot.Edge(root_node, child_node))
        else:
            child_node = add_nodes(graph, child)
            graph.add_node(child_node)
            graph.add_edge(pydot.Edge(root_node, child_node))
    return root_node


def create_pydot_of_tree(result):
    global n
    n = 0
    graph = pydot.Dot(graph_type="digraph", rankdir="LR")
    add_nodes(graph, result)
    return graph
