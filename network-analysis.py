import networkx as nx
import matplotlib.pyplot as plt
import geojson

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









def constructGraph(features):
	G = nx.Graph()
	
	for feature in features:
		name = feature['properties']['NAME']
		
		nodes = name.split(' to ')
		origin = nodes[0].strip()
		destination = nodes[len(nodes) - 1].strip()

		if not origin.isspace() and not origin == "" and not destination.isspace() and not destination == "":
			print name
			path = feature['geometry']['coordinates'][0]
			length = float(feature['properties']['SHAPE_Length'])
			# Need to figure out a way to change origin coords or check them because they vary slightly and infer different nodes.
			# Node attributes must be hashable.Maybe a separate lookup table? Just gonna keep em here for now. 
			# origin_coords = {'lat':float(path[0][0]), 'lon':float(path[0][1])}
			# dest_coords = {'lat':float(path[len(path) - 1][0]), 'lon':float(path[len(path) - 1][1])}
			# edge_info = {'length':length, 'object_id':feature['properties']['OBJECTID'], 'path_name':name}
			G.add_node(origin)
			G.add_node(destination)
			G.add_edge(origin, destination)
	
	return G



json_file =  open("networkMap/features.geojson")
json_data = geojson.load(json_file)

G = constructGraph(json_data.features)
print G.nodes()

# Draw the graph
print "Drawing Graph"
nx.draw(G)
plt.show()