
class MiniMaxTree:
    def __init__(self, value=None, children=None, action=None):
        self.value = value
        self.children = children if children is not None else []
        self.action = action

    def add_child(self, child_node):
        self.children.append(child_node)

    def set_value(self, value):
        self.value = value
