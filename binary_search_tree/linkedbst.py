"""
File: linkedbst.py
Author: Ken Lambert
"""

from binary_search_tree.abstractcollection import AbstractCollection
from binary_search_tree.bstnode import BSTNode
from binary_search_tree.linkedstack import LinkedStack
from binary_search_tree.linkedqueue import LinkedQueue


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        current = self._root
        traversal = [current.data]
        tracking = LinkedStack()
        tracking.push(current.right)
        tracking.push(current.left)
        while not tracking.isEmpty():
            current = tracking.pop()
            traversal.append(current.data)
            for i in (current.right, current.left):
                if i:
                    tracking.push(i)
        return iter(traversal)

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""

        traversal = []

        def recurse(node):
            if node.left or node.right:
                recurse(node.left)
                recurse(node.right)
                traversal.append(node.data)
            else:
                traversal.append(node.data)

        recurse(self._root)
        return iter(traversal)

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        node = self._root
        traversal = [node.data]
        tracking = LinkedQueue()
        tracking.add(node)
        while not tracking.isEmpty():
            node = tracking.pop()
            for i in (node.left, node.right):
                if i:
                    traversal.append(i.data)
                    tracking.add(i)

        return iter(traversal)

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self, root=None):
        '''
        return: int, the height of tree
        '''
        if not root:
            root = self._root

        def height1(top):
            if top and (top.left or top.right):
                height = height1(top.left)
                height2 = height1(top.right)
                return max(height, height2) + 1
            else:
                return 0

        return height1(root)

    def isBalanced(self):
        '''
        return: True if tree is balanced
        '''

        def height1(top):
            """
            Helping-function to find a sub-height
            top: the root of the tree
            """
            if top and (top.left or top.right):
                height = height1(top.left)
                height2 = height1(top.right)
                return max(height, height2) + 1
            else:
                return 0

        def balance(top):
            """
            Recursive function to find out whether the tree is balanced
            top: the root
            """
            if not top:
                return True
            h1 = height1(top.left)
            h2 = height1(top.right)
            if abs(h1 - h2) <= 1 and balance(top.left) and \
                    balance(top.right):
                return True
            return False

        return balance(self._root)

    def rangeFind(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        low: lower limit
        high: higher limit
        return: all values in tree between the low and high
        '''

        lst = []
        for item in self.inorder():
            if low <= item <= high:
                lst.append(item)
            elif item > high:
                break
        return lst

    def rebalance(self):
        '''
        Rebalances the tree.
        return: None
        '''
        new = []
        elements = [i for i in self.inorder()]

        def middle(values):
            """
            values: list with values
            return: middle value in the values
            """
            return values[int((len(values) - 1) / 2)]

        def half(values, mid=None):
            """
            Separating the list on two halfs
            values: list with values
            mid: the separator
            return: two lists
            """
            if not mid:
                mid = middle(values)
            p1 = []
            while values[0] < mid:
                p1.append(values.pop(0))
            return p1, values

        root = middle(elements)
        new = [root]
        ind = elements.index(root)
        elements.pop(ind)

        def recurse(values):
            """
            Recursive function to balance the tree
            values: list with tree values
            """
            if len(values) > 1:
                half1, half2 = half(values)

                if half1 and half2:
                    mid1, mid2 = middle(half1), middle(half2)
                    el1, el2 = mid1, mid2
                    in1, in2 = half1.index(el1), half2.index(el2)
                    new.append(half1.pop(in1))
                    new.append(half2.pop(in2))
                    recurse(half1)
                    recurse(half2)

                elif half1:
                    el1 = middle(half1)
                    in1 = half1.index(el1)
                    new.append(half1.pop(in1))
                    recurse(half1)

                elif half2:
                    el1 = middle(half2)
                    in1 = half2.index(el1)
                    new.append(half2.pop(in1))
                    recurse(half2)
            elif values:
                new.append(values[0])

        recurse(elements)
        self._root = BSTNode(new[0])
        for i in new[1:]:
            self.add(i)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        """

        def recurse(nod):
            if nod:
                if nod.data < item:
                    return recurse(nod.right)
                elif nod.data > item:
                    if nod.left and nod.left.data > item:
                        return recurse(nod.left)
                    elif nod.left and nod.left.data == item:
                        return nod.left.data
                    else:
                        return nod.data

        return recurse(self._root)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        """

        def recurse(nod):
            if nod:
                if nod.data > item:
                    return recurse(nod.left)
                elif nod.data < item:
                    if nod.right and nod.right.data < item:
                        return recurse(nod.right)
                    elif nod.right and nod.right.data == item:
                        return nod.right.data
                    else:
                        return nod.data

        return recurse(self._root)
