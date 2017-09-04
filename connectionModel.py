import networkGraph
import networkx as nx
import matplotlib.pyplot as plt
import geojson
from geopy.distance import vincenty
import graphistry
import json

graphistry.register(key='555194151a1e7dd59b00ae0c4826d91b3bfbf4afac2239e05ec7180aa6f06e152d43ddea14a3616121b451cf00d150c1')

G = networkGraph.getGraphModel()

for node in list(G.nodes()):
	G.node[node]['node_type'] = 'connection'	


swatch_colors=['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5']
seen_gen_types = []
seen_line_capacities = []
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
	# Check distance against all nodes to find probably corresponding node..
	# This slows things down A LOT because we make the complexity n^2...again.
	nodes = list(G.nodes())
	min_distance = vincenty((feature.geometry.coordinates[0],feature.geometry.coordinates[1]), nodes[0]).meters
	closest_node = nodes[0]
	for node in list(G.nodes()):
		# Get the vincenty distance between a given node and the generator
		distance =  vincenty((feature.geometry.coordinates[0],feature.geometry.coordinates[1]), node).meters
		closest_node = node if distance < min_distance else closest_node
		min_distance = distance if distance < min_distance else min_distance
		
	
	feature.graph = {
		'node':closest_node,
		'node_distance': min_distance
	}

	# G.node[closest_node]
	
	if 'features' not in G.node[closest_node]:
		G.node[closest_node]['generators'] = []
		G.node[closest_node]['generation_capacity'] = 0
		G.node[closest_node]['generation_type'] = ""
		G.node[closest_node]['generation_label'] = ""

	G.node[closest_node]['node_type'] = 'generator'
	
	G.node[closest_node]['generators'].append(json.dumps(feature))
	G.node[closest_node]['num_generators'] = len(G.node[closest_node]['generators'])
	
	if feature['properties']['GENERATIONMW']:
		G.node[closest_node]['generation_capacity'] += float(feature['properties']['GENERATIONMW'])

	# I'm effectively just shoosing whichever was hte last primary fuel type here. Could do better but I want a single type label for each one for coloring purposes.
	
	if feature['properties']['PRIMARYFUELTYPE']:
		fuelType = feature['properties']['PRIMARYFUELTYPE']
		G.node[closest_node]['generation_type'] = fuelType
		if not fuelType in seen_gen_types:
			seen_gen_types.append(fuelType)
		G.node[closest_node]['generation_type_color_code'] = seen_gen_types.index(fuelType)

	if feature['properties']['NAME']:
		G.node[closest_node]['generation_label'] += feature['properties']['NAME']+" "


# print features
for feature in features:
	state = feature.properties['STATE']
	print state
	print feature
	print feature['graph']['node_distance']

# for edge in list(G.edges()):
# 	if not int(edge['capacityKV']) in seen_line_capacities:
# 		seen_line_capacities.append(int(edge['capacityKV']))
# 	G.edge[edge]['capacity_color_code'] = seen_line_capacities.index(int(edge['capacityKV']))
	


plotter = graphistry.bind(
				source='src', 
				destination='dst', 
				node='nodeid', 
				point_size='generation_capacity', 
				edge_color='capacityKV', 
				point_title='generation_label', 
				point_color='generation_type_color_code'
				)
plotter.plot(G)



# genlist = sorted(features, key=lambda k: k['properties']['GENERATIONMW']) 
# for gen in genlist:
# 	print gen.properties['NAME']
# 	print gen['graph']['node_distance']