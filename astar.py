# Implements A-star algorithm for the feature set, which is a conversion of network mapping data from AREMI.
# Algorithm from wikipedia on A-Star: https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
from math import sqrt, pow


def heuristic_cost_estimate(start_x, start_y, goal_x, goal_y):
	# At the moment, just pythagoras ie. straight line distance based on lat-long (so not actually straight line distance, but close)
	start_x = float(start_x)
	start_y = float(start_y)
	goal_x = float(goal_x)
	goal_y = float(goal_y)
	return sqrt(pow(goal_x - start_x, 2) + pow(goal_y - start_y, 2))




def constructGraph(features):
	graph = {}
	for feature in features:
		name = feature['properties']['NAME']
		nodes = name.split(' to ')
		origin = nodes[0].strip()
		destination = nodes[len(nodes) - 1].strip()

		if not origin.isspace() and not origin == "" and not destination.isspace() and not destination == "":
			path = feature['geometry']['coordinates'][0]
			length = float(feature['properties']['SHAPE_Length'])
			# length = heuristic_cost_estimate(float(path[0][0]), float(path[0][1]), float(path[len(path) - 1][0]), float(path[len(path) - 1][1]))
			addToGraph(
				graph=graph, 
				origin=origin, 
				destination=destination, 
				length=length, 
				object_id=feature['properties']['OBJECTID'],
				origin_lat=float(path[0][0]),
				origin_lon=float(path[0][1]),
				dest_lat=float(path[len(path) - 1][0]),
				dest_lon=float(path[len(path) - 1][1]),
				path_name = name
			)

			addToGraph(
				graph=graph, 
				origin= destination, 
				destination=origin, 
				length = length, 
				object_id = feature['properties']['OBJECTID'],
				origin_lat= float(path[len(path) - 1][0]),
				origin_lon=float(path[len(path) - 1][1]),
				dest_lat=float(path[0][0]),
				dest_lon=float(path[0][1]),
				path_name = name
			)
	
	return graph




def addToGraph(graph, origin, destination, length, object_id, origin_lat, origin_lon, dest_lat, dest_lon, path_name):
	# The graph is a dict linking node names to lists of neighbours. 
	if origin not in list(graph):
		graph[origin] = {}
		graph[origin]['neighbours'] = {}
		graph[origin]['lat'] = origin_lat
		graph[origin]['lon'] = origin_lon
		graph[origin]['object_id'] = object_id
		graph[origin]['path_name'] = path_name
	# elif: graph[origin]['lon'] != origin_lon or graph[origin]['lat'] != origin_lat:
	# 	print "Lat and Lon not matching! Check! "

	graph[origin]['neighbours'][destination] = {
			'neighbour_name' : destination,
			'path_name': path_name,
			'object_id' : object_id,
			'length': length,
			'lat': dest_lat,
			'lon': dest_lon,
		}
	

def reconstruct_path(cameFrom, current, graph):
	total_path = []
	while current in list(cameFrom):
		total_path.append(graph[current]['neighbours'][cameFrom[current]]['path_name'])
		current = cameFrom[current]

	# print total_path
	return total_path


def run(graph, start, goal):
	print "Start: "+start
	print "Goal: "+goal
	# # Generate the graph
	# graph = constructGraph(features)

	# The set of nodes already evaluated.
	closedSet = []
	# The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
	openSet = [start]
	# For each node, which node it can most efficiently be reached from.
	# If a node can be reached from many nodes, cameFrom will eventually contain the
	# most efficient previous step.
	cameFrom = {}

	#  For each node, the cost of getting from the start node to that node.
	gScore = {key: None for key in list(graph)}
	#  The cost of going from start to start is zero.
	gScore[start] = 0

	#  For each node, the total cost of getting from the start node to the goal
    #  by passing by that node. That value is partly known, partly heuristic.
	fScore = {key: float('inf') for key in list(graph)}
	#  For the first node, that value is completely heuristic.
	fScore[start] = heuristic_cost_estimate(graph[start]['lat'], graph[start]['lon'],graph[goal]['lat'], graph[goal]['lon'])

	while len(openSet) != 0:
		# current := the node in openSet having the lowest fScore[] value
		# Get the union of openSet and fScores, then find the one in that dict with minimum fscore. 
		# print "\nAnother Iteration"
		subset = {k: fScore[k] for k in openSet}
		
		
		current = min(subset, key=subset.get)
		# print subset
		# print "== Current is set to "+current
		# print cameFrom
		if current == goal:
			# print "Current G Score: "+str(gScore[current])
			return reconstruct_path(cameFrom, current, graph)
		
		openSet.remove(current)
		closedSet.append(current)

		
		for neighbour_name in list(graph[current]['neighbours']):
			neighbour = graph[current]['neighbours'][neighbour_name]
			if neighbour_name in closedSet:
				continue
			
			tentative_gScore = gScore[current] + neighbour['length']

			if neighbour_name not in openSet:
				openSet.append(neighbour_name)
			elif tentative_gScore >= gScore[neighbour_name]:
				continue
			
			cameFrom[neighbour_name] = current
			gScore[neighbour_name] = tentative_gScore

			neighbour_lat = neighbour['lat']
			neighbour_lon = neighbour['lon']
			goal_lat = graph[goal]['lat']
			goal_lon = graph[goal]['lon'] 
			heuristicCost = heuristic_cost_estimate(neighbour['lat'], neighbour['lon'], graph[goal]['lat'], graph[goal]['lon'] )
			fScore[neighbour_name]  = gScore[neighbour_name] + heuristicCost
	return None