# Created to estimate the time of algorithms working

from binary_search_tree.linkedbst import LinkedBST
from random import choice
from time import time


def read_sorted(path):
    """
    Reading the words from file and saving in sorted order
    path: path to file
    return: list with words
    """
    words = []
    with open(path) as f:
        for line in f:
            words.append(line.strip())
    return words


def read_unsorted(path):
    """
    Reading the words from file and saving in unsorted order
    path: path to file
    return: set with words
    """
    words = set()
    with open(path) as f:
        for line in f:
            words.add(line.strip())
    return words


def random_words(words):
    """
    Choosing 10000 random words
    words: list with words
    """
    needed = []
    for i in range(10000):
        needed.append(choice(words))
    return needed


def make_tree(info):
    """
    Filling the Binary Search Tree structure
    info: set with words
    return: Tree
    """
    tree = LinkedBST()
    for i in info:
        tree.add(i)
    return tree


def main():
    """
    Run estimation of algorithms running time
    """
    lst = read_sorted('words.txt')
    needed = random_words(lst)

    # Estimating searching time in list
    start = time()
    for wrd in needed:
        lst.index(wrd)
    print('Searching in list: ', time() - start, 'sec')

    # Estimating searching time in unbalanced tree
    d2 = read_unsorted('words.txt')
    tree = make_tree(d2)
    start = time()
    for wrd in needed:
        tree.find(wrd)
    print('Searching in unbalanced tree: ', time() - start, 'sec')

    # Estimating searching time in balanced tree
    tree.rebalance()
    start = time()
    for wrd in needed:
        tree.find(wrd)
    print('Searching in balanced tree: ', time() - start, 'sec')


if __name__ == '__main__':
    main()
