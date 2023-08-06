import functools
from graphviz import Digraph
from .misc import TableHelper


def node_name(parent):
    return f'{parent.replace(":", "_")}' if ':' in parent else f'{parent}_0'


@functools.singledispatch
def js_graph(js, g, parent):
    node = node_name(parent)
    g.node(node, label=str(js))
    g.edge(parent, node)


@js_graph.register(list)
def _(js, g, parent):
    tab = TableHelper(node_name(parent), '&#91;', '&#93;')
    for k, v in enumerate(js):
        js_graph(v, g, tab.append(k, k))
    tab.done(g, parent)


@js_graph.register(dict)
def _(js, g, parent):
    tab = TableHelper(node_name(parent), '{', '}')
    for k, v in js.items():
        js_graph(v, g, tab.append(k, k))
    tab.done(g, parent)


class JsonGraph:
    def __init__(self, js, title):
        self.js = js
        self.g = Digraph(title, node_attr={'shape': 'plaintext'})

        root = 'struct0'
        self.g.node(root, label=title, shape='doublecircle')
        js_graph(js, self.g, root)


if __name__ == '__main__':
    import json

    with open("../demo/demo1.json", 'r') as f:
        j = json.loads(f.read())
        dot = JsonGraph(j, 'root').g
        dot.render("../demo/demo1.gv", format="pdf")
