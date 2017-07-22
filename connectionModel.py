import networkGraph
import networkx as nx
import matplotlib.pyplot as plt

G = networkGraph.getGraphModel()

# print ("Number of connected components: %v",nx.connected_components(G))
counter = 0
unconnected = []
for comp in nx.connected_components(G):
	print str(len(comp)) + " " + str(comp)+"\n"
	counter += 1
	if len(comp) < 100:
		for node in comp:
			unconnected.append(node)

# Loop through all edges, if in an unconnected set then print.
for n1, n2, names in G.edges(data='node_names'):
	if n1 in unconnected or n2 in unconnected:
		print names
		print n1
		print n2

print "Number of Graphs: "+str(counter)
# Draw the graph
print "Drawing Graph"

nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=False, node_size=1)
plt.show()