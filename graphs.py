import pygraphviz as pgv

def draw_graph(graph, filename):
    "Draw the 'graph' and save the picture to a file named 'filename'."
    G = pgv.AGraph()
    for node, neighbors in graph.iteritems():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)#, style='dashed')
    # Among all the six tried progs for generating layouts, neato seems the
    # best for graphs.
    G.layout(prog='neato')
    G.draw(filename)

def draw_tree(tree, filename):
    "Draw the 'tree' and save the picture to a file named 'filename'."
    G = pgv.AGraph()
    for node, children in tree.iteritems():
        for child in children:
            G.add_edge(node, child)
    # The prog dot is simply the best for generating tree layouts.
    G.layout(prog='dot')
    G.draw(filename)

def draw_pstree(graph, pstree, filename, layout='before'):
    """Draw the pseudotree 'pstree' of the 'graph'. and save the picture to a
    file called 'filename'. Layout can be 'before' or 'after'; try both the
    options and see which diagram you like best."""
    # First layout the pstree
    G = pgv.AGraph(remincross=True)
    for node, children in pstree.iteritems():
        for child in children:
            G.add_edge(node, child)
    if layout == 'before':
        G.layout(prog='dot')

    # Then add the remaining edges without changing the layout
    for node, neighbors in graph.iteritems():
        for neighbor in neighbors:
            if not G.has_edge(node, neighbor):
                G.add_edge(node, neighbor, constraint='false', style='dashed')
    if layout == 'after':
        G.layout(prog='dot')

    G.draw(filename)

if __name__ == '__main__':
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

    draw_graph(g1, 'g1.png')

    g1_pstree = {1: [2],
         2: [3],
         3: [4, 7],
         4: [],
         5: [],
         6: [5],
         7: [6, 8],
         8: [10],
         9: [],
         10: [11],
         11: [9, 16],
         12: [13],
         13: [14],
         14: [15],
         15: [],
         16: [12],
         'Nothing': [1]
        }

    draw_tree(g1_pstree, 'g1_tree.png')
    draw_pstree(g1, g1_pstree, 'g1_pstree.png', layout='after')

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

    draw_graph(g2, 'g2.png')

    g2_pstree = {0: [1, 2],
         1: [3, 4],
         2: [5, 6],
         3: [7, 8],
         4: [9, 10],
         5: [11, 12],
         6: [13],
         7: [],
         8: [],
         9: [],
         10: [],
         11: [],
         12: [],
         13: [],
         'Nothing': [0]
        }

    draw_tree(g2_pstree, 'g2_tree.png')
    draw_pstree(g2, g2_pstree, 'g2_pstree.png')
