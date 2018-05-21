# The part of tic-tac-toe game
# Created to process decision making for bot-player


class Tree:
    """
    Represents a Tree Data Structure
    """

    def __init__(self, root):
        self._root = root
        self._children = list()

    def add(self, value):
        """
        Adding an element to the children
        value: value to add
        """
        self._children.append(Tree(value))

    def __iter__(self):
        """
        Iterating elements in self.children
        return: child one by one
        """
        for i in self._children:
            yield i

    def get_children(self):
        """
        return: list with children
        """
        return self._children

    def get_root(self):
        """
        return: root value
        """
        return self._root
