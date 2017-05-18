# Implements A-star algorithm for the feature set, which is a conversion of network mapping data from AREMI.
from math import sqrt, pow


def heuristic_cost_estimate(start_x, start_y, goal_x, goal_y):
	# At the moment, just pythagoras ie. straight line distance based on lat-long (so not actually straight line distance, but close)
	start_x = float(start_x)
	start_y = float(start_y)
	goal_x = float(goal_x)
	goal_y = float(goal_y)
	return sqrt(pow(goal_x - start_x, 2) + pow(goal_y - start_y, 2))


def run(features, start, goal):
	closedSet = []
	openSet = [start]

	cameFrom = {}

	gScore = {}
	gScore[start] = 0
