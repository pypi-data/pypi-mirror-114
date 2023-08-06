from ast import NodeVisitor


class Visit(NodeVisitor):
    def __init__(self):
        self.names = []

    def visit_ImportFrom(self, node):
        self.names.extend(
            alias.asname or alias.name
            for alias in node.names
        )
