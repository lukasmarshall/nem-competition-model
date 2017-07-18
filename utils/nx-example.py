import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# Add a single node
G.add_node(1)

# Add a list of nodes
G.add_nodes_from([2,3])


# Add an edge between 1 and 2 and associate it with an object
G.add_edge(1,2, object={'number':2})
# You can do this for nodes and whole graphs also.
# Weight is a special attribute and is used by graph algos. 

# add an 'nbunch' of nodes (iterable container of nodes)
H = nx.path_graph(10)
G.add_nodes_from(H)

# Add an edge from 1 to 2
G.add_edge(1,2)

# Add an edge tuple
e = (2,3)
G.add_edge(*e) # the * unpacks the edge tuple. cool. 

# Add edges from a list
G.add_edges_from([(1,2), (1,3)])

# Add eges from an 'ebunch' iterable container of edges
G.add_edges_from(H.edges())

# Remove some nodes
G.remove_nodes_from([2,3])

# Print the nodes:
print G.nodes()

# Print the edges
print G.edges()

# Draw the graph
nx.draw(G)
plt.show()