import networkx as nx
import matplotlib.pyplot as plt

import pseudotree as ps

g = ps.dfsTree(ps.g2, 0)
nxg = nx.Graph(g)
pos = nx.spring_layout(nxg, iterations=100)

fig = nx.draw_networkx(nxg, pos, with_labels=True)

plt.show(fig)