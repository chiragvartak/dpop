"This module constructs the DFS-tree of a graph, which is a pseudotree."
# Assumptions:
# 1. There are no 'isolated' parts of the graph. All vertices are
# connected to every other vertex through some path or the other.


def dfsTree(graph, startingVertex):
    """Returns the DFS-tree of a graph, given a startingVertex"""
    # Note that the tree that is returned has a different format.
    # It list the children for every node rather than the neighbors.
    # The root node can be found by the 'Nothing' node.
    
    added = {} # The collection of nodes already considered
    tree = dfsTreeHelper(graph, startingVertex, 'Nothing', {}, added)
    
    # Create empty lists as children of leaf nodes
    for node in graph:
        if node not in tree:
            tree[node] = []

    return tree


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


def get_parents(pstree):
    "Given a pseudo-tree (dfsTree), get the parents for each node as a dict."
    parents = {}
    for node, children in pstree.iteritems():
        for child in children:
            parents[child] = node
    return parents


def assign_depths(pstree):
    """
    Returns a dict of depths assigned to all the nodes in the pseudo-tree
    (dfsTree) 'pstree'.
    """
    depths = {}
    assign_depths_helper(depths, pstree, 'Nothing', -1)
    return depths


def assign_depths_helper(depths, pstree, node, value):
    depths[node] = value
    children = []
    try:
        children = pstree[node]
    except KeyError:
        return depths
    for child in children:
        assign_depths_helper(depths, pstree, child, value+1)
    return depths


def get_relatives(graph, pstree):
    """Get the p, pp, pc of the 'graph', given its 'pstree'. Children are given
    by the 'pstree' itself."""

    parents = get_parents(pstree)
    depths = assign_depths(pstree)
    pseudo_children = {}
    pseudo_parents = {}

    for node_id in pstree:
        if node_id == 'Nothing':
            continue

        p = parents[node_id]
        c = pstree[node_id]
        pp = []
        pc = []
        pseudo_relatives = set(graph[node_id]) - set([p]) - set(c)
        pseudo_relatives = list(pseudo_relatives)
        for relative in pseudo_relatives:
            if depths[node_id] < depths[relative]:
                pc.append(relative)
            else:
                pp.append(relative)

        pseudo_parents[node_id] = pp
        pseudo_children[node_id] = pc

    return (parents, pseudo_parents, pseudo_children)
