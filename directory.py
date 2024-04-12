class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.children = {}
        self.parent = parent  # Reference to the parent directory

    def add_child(self, child):
        self.children[child.name] = child
        child.parent = self  # Set the child's parent to this directory

    def remove_child(self, child_name):
        if child_name in self.children:
            del self.children[child_name]

    def has_child(self, child_name):
        return child_name in self.children

    def get_child(self, child_name):
        return self.children.get(child_name)

    def get_parent(self):
        return self.parent