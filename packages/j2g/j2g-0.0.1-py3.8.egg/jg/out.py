version = "0.0.1"
author = "jeack_chen@hotmail.com"
github_url = "https://github.com/jeackchn/jg"

# def schema_graph(schema, title):
#     """
#     :param schema:
#         schema ref：http://json-schema.org/
#     :param title:
#          schema.title or title or 'root', graph root name
#     :return: graphviz.Digraph
#         digraph_obj.view() show schema graph
#         digraph_obj.save_to(self, filename=None, directory=None)
#     """
#     from .schema_graph import SchemaGraph
#     return SchemaGraph(schema, title).g


def json_graph(json, title):
    """
    :param json:
        json data
    :param title:
         title graph root name
    :return: graphviz.Digraph
        digraph_obj.view() show schema graph
        digraph_obj.save_to(self, filename=None, directory=None)
    """
    from .json_graph import JsonGraph
    return JsonGraph(json, title).g
