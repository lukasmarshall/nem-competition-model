import geojson
from descartes import PolygonPatch
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import os
import re
import astar





# Often the line descriptions in reports are 'x to y' while the naming is 'y to x' - test the swapped version. 


def swapEndpoints(name):
	if ' to ' in name:
		points = name.split(' to ')
		if len(points) == 2:
			swapped = points[1].strip()+' to '+points[0].strip()
			return swapped
		else:
			# There are 3 places (in the entire dataset) where it's 'x to y to z' - probably not worth the effort. 
			# print "Weird: "+name
			return name
	else:
		 return name

def isNameInLine(name, line):
	# Naming format in geoJSON is 'x to y' for multiple places, but not in reports often. 
	if ' to ' in name:
		points = name.split(' to ')
		if len(points) == 2:
			swapped = points[1].strip()+' to '+points[0].strip()
			m = re.search(points[0].strip()+'.{0,8}'+points[1].strip(), line)
			ms = re.search(points[1].strip()+'.{0,8}'+points[0].strip(), line) #swapped-around version because often format is 'x to y' while file goes 'y to x'
			if m or ms:
				return True
			else:
				return False
		else:
			# There are 3 places (in the entire dataset) where it's 'x to y to z' - probably not worth the effort. 
			# print "Weird: "+name
			return False
	else:
		 return name in line
	


def getNodeNames(features):
	nodeNames = []
	for feature in features:
		name = feature['properties']['NAME']
		# print name
		nodes = name.split(' to ')
		for node in nodes:
			# print node
			node = node.strip()
			if node not in nodeNames and not node.isspace() and not node == "":
				nodeNames.append(node)
	return nodeNames

# Checks if an origin and destiantion are mentioned close to each other in the line. 
def checkPotentialPath(node1, node2, line):
	m = re.search(node1+'.{0,8}'+node2, line)
	ms = re.search(node2+'.{0,8}'+node1, line)
	if m or ms:
		return True
	else:
		return False

 
json_file =  open("networkMap/features.geojson")
json_data = geojson.load(json_file)

# Get a list of all the node names
nodeNames = getNodeNames(json_data.features)
# print nodeNames
# List of path names for highlighting. 
toHighlight = []

graph = astar.constructGraph(json_data.features)
# Iterate through report, look for occurrences of network feature names, add to list for later highlighting. 
for filename in os.listdir('reports'):
	report = open('reports/'+filename)
	print filename
	lines = []
	foundInThisReport = []
	for line in report:
		lines.append(line)
	
	# for feature in json_data.features:
	# 	for line in lines:
	# 		# # Simple, old version without a-star.
	# 		# name = feature['properties']['NAME']
	# 		# swappedName = swapEndpoints(name) #need to swap because often names are 'x to y' and then written as 'y to x'
	# 		# if isNameInLine(name, line):
	# 		# 	if name not in toHighlight and not name.isspace():
	# 		# 		toHighlight.append(name)
	# 		# 		foundInThisReport.append(name)
			

	for line in lines:
		# New complex version with a-star. 

		nodeShortList = []
		for node in nodeNames:
			if node in line and not node in nodeShortList:
				nodeShortList.append(node)
		
		for node1 in nodeShortList:
			for node2 in nodeShortList:
				if checkPotentialPath(node1, node2, line):
					print "Running Astar on "+node1 + " <> "+ node2
					path = astar.run(graph, node1, node2)
					if path:
						for pathName in path:
							if pathName not in toHighlight:
								toHighlight.append(pathName)
								foundInThisReport.append(pathName)

	print foundInThisReport

print "Total Paths to Highlight: "
print toHighlight

# ==========================================
# ==========================================
# Charting / Graphing
# ==========================================
# ==========================================
ax = plt.figure(figsize=(10, 10)).add_subplot(111)#fig.gca()

# Base Plotting Setup. 
m = Basemap(projection='cea',llcrnrlat=-44,urcrnrlat=-16,
		llcrnrlon=135,urcrnrlon=154,resolution='c')
m.drawmapboundary(fill_color='white', zorder=-1)
m.drawparallels(np.arange(-90., 91., 30.), labels=[1, 0, 0, 1], dashes=[1, 1], linewidth=0.25, color='0.5',fontsize=14)
m.drawmeridians(np.arange(0., 360., 60.), labels=[1,0,0,1], dashes=[1, 1], linewidth=0.25, color='0.5',fontsize=14)
m.drawcoastlines(color='0.6', linewidth=1)



# Loop through the features and draw them on the map 
i = 0
toLabel = list(toHighlight)
for feature in json_data.features:
	# print str(i)+" of "+str(len(json_data.features))
	i += 1
	# print feature
	if feature['geometry']['type'] == "MultiLineString":
		coordlist = feature['geometry']['coordinates'][0]
		
		x = []
		y = []
		for coord in coordlist:
			lat = coord[0]
			lon = coord[1]
			# my_x,my_y = m(lon, lat)
			coord = m(lon, lat)
			# print coord
			# m.plot(my_x,my_y,'bo', markersize=24)
			x.append(coord[0])
			y.append(coord[1])

		# m.plot(x,y,linewidth=1.5,color='r')
		# Line stuff
		if feature['properties']['NAME'] in toHighlight:
			print "Highlighting "+feature['properties']['NAME']
			m.plot(x,y,linewidth=1.5,color='r')
			# Only label once - sometimes lines span multiple features. 
			if feature['properties']['NAME'] in toLabel:
				plt.text(x[len(x) // 2], y[len(y) // 2], feature['properties']['NAME'])
				toLabel.remove(feature['properties']['NAME'])
			# lineObject = Line2D(x, y, color='r', visible=True,  zorder=0.2, label=feature['properties']['NAME']  )
		else:
			color = 'b'
			m.plot(x,y,linewidth=1.5,color='b')
			# lineObject = Line2D(x, y, color='b', visible=True,  zorder=0.2  )
		
		# ax.add_line(lineObject)



plt.draw()
plt.show()