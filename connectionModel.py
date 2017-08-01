import networkGraph
import networkx as nx
import matplotlib.pyplot as plt
import geojson
from geopy.distance import vincenty

G = networkGraph.getGraphModel()

# networkGraph.examineConnectedSubgraphs(G)

# print "Drawing Graph"
# nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=False, node_size=1)
# plt.show()


json_file =  open("generatorMap/generators.geojson")
json_data = geojson.load(json_file)
features = json_data.features

# Hold the unconnected points.
unconnected = []
connected = []

# The maximum distance 2 points can be apart to be considered the same node (in meters) 
COLOCATION_DISTANCE = 300


non_nem_states = ["Western Australia", "Northern Territory"]
features[:] = [feature for feature in features if feature.get('properties').get('STATE') not in non_nem_states]

# for index, feature in features:
# 	state = feature.properties['STATE']
# 	if state == "Western Australia" or state == "Northern Territory":
# 		features.remove(feature)

# Iterate through each generator.
for feature in features:
	state = feature.properties['STATE']
	# print feature.properties['NAME']
	# print feature.geometry.coordinates
	# print feature.properties['GENERATIONMW']

	capacity = float(feature.properties['GENERATIONMW']) if feature.properties['GENERATIONMW'] else 0
	# print feature.properties['NAME']
	# print feature.geometry.coordinates
	# Associate with a graph node.
	# Check distance against all  nodes to find probably corresponding node..
	# This slows things down A LOT because we make the complexity n^2...again.
	nodes = list(G.nodes())
	min_distance = vincenty((feature.geometry.coordinates[0],feature.geometry.coordinates[1]), nodes[0]).meters
	closest_node = nodes[0]
	for node in list(G.nodes()):
		# Get the vincenty distance between a given node and the generator
		distance =  vincenty((feature.geometry.coordinates[0],feature.geometry.coordinates[1]), node).meters
		min_distance = distance if distance < min_distance else min_distance
		closest_node = node if distance < min_distance else closest_node
	
	feature.graph = {
		'node':closest_node,
		'node_distance': min_distance
	}


# print features
for feature in features:
	state = feature.properties['STATE']
	print state
	print feature
	print feature['graph']['node_distance']
# genlist = sorted(features, key=lambda k: k['properties']['GENERATIONMW']) 
# for gen in genlist:
# 	print gen.properties['NAME']
# 	print gen['graph']['node_distance']