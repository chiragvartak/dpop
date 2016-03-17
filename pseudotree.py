"This module constructs the DFS-tree of a graph, which is a pseudotree"
# Assumptions:
# 1. There are no 'isolated' parts of the graph. All vertices are
# connected to every other vertex through some path or the other.

g1 = {1: [2,9],
      2: [1,3,16],
      3: [2,4,7,15],
      4: [3],
      5: [6],
      6: [5,7],
      7: [3,6,8,9],
      8: [7,10],
      9: [1,7,11],
      10: [8,11],
      11: [9,10,16],
      12: [13,16],
      13: [12,14],
      14: [13,15,16],
      15: [3,14],
      16: [2,11,12,14]
      }

# The graph (pseudotree) in the DPOP paper
g2 = {0: [1,2,4,11],
      1: [0,3,4,8],
      2: [0,5,6,12],
      3: [1,7,8],
      4: [0,1,9,10],
      5: [2,11,12],
      6: [2,13],
      7: [3],
      8: [1,3],
      9: [4],
      10: [4],
      11: [0,5],
      12: [2,5],
      13: [6]
      }


def _dfsTreeHelper(graph, node, parent, tree, added):
    if not node in added: # Consider this node only if not already considered
        if parent in tree:
            tree[parent].append(node)
            added[node] = True
        else:
            tree[parent] = [node]
            added[node] = True
        for child in graph[node]:
            _dfsTreeHelper(graph, child, node, tree, added)

    return tree


def dfsTree(graph, startingVertex):
    """Returns the DFS-tree of a graph, given a startingVertex"""
    # Note that the tree that is returned has a different format.
    # It list the children for every node rather than the neighbors.
    # The root node can be found by the 'Nothing' node.
    tree = {}
    added = {} # The collection of nodes already considered
    return _dfsTreeHelper(graph, startingVertex, 'Nothing', tree, added)


def _test():
    x = dfsTree(g1, 1)
    y = {1: [2],
         2: [3],
         3: [4, 7],
         6: [5],
         7: [6, 8],
         8: [10],
         10: [11],
         11: [9, 16],
         12: [13],
         13: [14],
         14: [15],
         16: [12],
         'Nothing': [1]
        }
    assert x == y

    x = dfsTree(g2, 0)
    y = {0: [1, 2],
         1: [3, 4],
         2: [5, 6],
         3: [7, 8],
         4: [9, 10],
         5: [11, 12],
         6: [13],
         'Nothing': [0]
        }
    assert x == y


if __name__ == '__main__':
    _test()
