import geojson
from descartes import PolygonPatch
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import os
import re





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
	


 
json_file =  open("networkMap/features.geojson")
json_data = geojson.load(json_file)

# plt.clf()
ax = plt.figure(figsize=(10, 10)).add_subplot(111)#fig.gca()


m = Basemap(projection='cea',llcrnrlat=-44,urcrnrlat=-16,
		llcrnrlon=135,urcrnrlon=154,resolution='c')
m.drawmapboundary(fill_color='white', zorder=-1)
m.drawparallels(np.arange(-90., 91., 30.), labels=[1, 0, 0, 1], dashes=[1, 1], linewidth=0.25, color='0.5',fontsize=14)
m.drawmeridians(np.arange(0., 360., 60.), labels=[1,0,0,1], dashes=[1, 1], linewidth=0.25, color='0.5',fontsize=14)
m.drawcoastlines(color='0.6', linewidth=1)


toHighlight = []
# Iterate through report, look for occurrences of network feature names, add to list for later highlighting. 
for filename in os.listdir('reports'):
	report = open('reports/'+filename)
	# report = open('sample_report.txt')
	print filename
	lines = []
	foundInThisReport = []
	for line in report:
		lines.append(line)

	
	for feature in json_data.features:
		# print feature['properties']['NAME']
		for line in lines:
			name = feature['properties']['NAME']
			swappedName = swapEndpoints(name) #need to swap because often names are 'x to y' and then written as 'y to x'
			if isNameInLine(name, line):
				if name not in toHighlight and not name.isspace():
					toHighlight.append(name)
					foundInThisReport.append(name)
	print foundInThisReport


print toHighlight
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