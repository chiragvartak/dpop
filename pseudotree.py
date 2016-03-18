"This module constructs the DFS-tree of a graph, which is a pseudotree"
# Assumptions:
# 1. There are no 'isolated' parts of the graph. All vertices are
# connected to every other vertex through some path or the other.


def dfsTreeHelper(graph, node, parent, tree, added):
    if not node in added: # Consider this node only if not already considered
        if parent in tree:
            tree[parent].append(node)
            added[node] = True
        else:
            tree[parent] = [node]
            added[node] = True
        for child in graph[node]:
            dfsTreeHelper(graph, child, node, tree, added)

    return tree


def dfsTree(graph, startingVertex):
    """Returns the DFS-tree of a graph, given a startingVertex"""
    # Note that the tree that is returned has a different format.
    # It list the children for every node rather than the neighbors.
    # The root node can be found by the 'Nothing' node.
    tree = {}
    added = {} # The collection of nodes already considered
    return dfsTreeHelper(graph, startingVertex, 'Nothing', tree, added)
