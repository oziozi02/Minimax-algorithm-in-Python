



class NTreeNode:
    def __init__(self, parent, values_length, action):
        self.parent = parent
        self.values = [0] * values_length
        self.children = []
        self.action = action

    def add_child(self, child_node):
        self.children.append(child_node)
    
    def append_value(self, value):
        self.values.append(value)

    def set_values(self, values):
        self.values = values

    def set_value_at_index(self, index, value):
        self.values[index] = value

    def get_parent(self):
        return self.parent

    