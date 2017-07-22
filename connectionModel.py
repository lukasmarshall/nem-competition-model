import networkGraph
import networkx as nx
import matplotlib.pyplot as plt

G = networkGraph.getGraphModel()

networkGraph.examineConnectedSubgraphs(G)

print "Drawing Graph"
nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=False, node_size=1)
plt.show()