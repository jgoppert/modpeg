from parsimonious.nodes import NodeVisitor


class ModelicaPrinter(NodeVisitor):

    def __init__(self):
        print

    def generic_visit(self, node, visited_children):
        print '{:20s}|\t{:s}'.format(
            node.expr_name, node.full_text[node.start:node.end])

    def visit_(self, node, visitied_children):
        pass

    def visit__(self, node, visitied_children):
        pass
