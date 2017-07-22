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




unconnected_features = ['Heron Creek Tee', 'Middleback Tee']




def constructGraph(features):
	G = nx.Graph()
	seen = []
	for feature in features:
		name = feature['properties']['NAME']
		state = feature['properties']['STATE']
		nodes = name.split(' to ')
		origin = nodes[0].strip()
		destination = nodes[len(nodes) - 1].strip()

		

		if not origin.isspace() and not origin == "" and not destination.isspace() and not destination == "" and not state == "Western Australia" and not state == "Northern Territory" and not origin in unconnected_features and not destination in unconnected_features:
			print name
			origin += " "+feature['properties']['STATE']
			destination += " "+feature['properties']['STATE']
			path = feature['geometry']['coordinates'][0] # LIST OF LAT/LONGS FROM START TO FINISH
			origin_coords = {'lat':float(path[0][0]), 'lon':float(path[0][1])}
			dest_coords = {'lat':float(path[len(path) - 1][0]), 'lon':float(path[len(path) - 1][1])}
			edge_info = {'length':float(feature['properties']['SHAPE_Length']), 'object_id':feature['properties']['OBJECTID'], 'path_name':name}
			G.add_node(origin, pos=(origin_coords['lon'], origin_coords['lat']))
			G.add_node(destination, pos=(dest_coords['lon'], dest_coords['lat']))
			G.add_edge(origin, destination, attr_dict=edge_info)
	
	return G



json_file =  open("networkMap/features_edited.geojson")
json_data = geojson.load(json_file)

G = constructGraph(json_data.features)
# print G.nodes()

# print ("Number of connected components: %v",nx.connected_components(G))
counter = 0
for comp in nx.connected_components(G):
	print str(len(comp)) + " " + str(comp)+"\n"
	counter += 1

print "Number of Graphs: "+str(counter)
# Draw the graph
print "Drawing Graph"
# nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=False, node_size=1)
# plt.show()