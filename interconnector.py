import os
import csv
import numpy as np
import pickle

import bokeh
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib import colors as mcolors


# from bokeh.charts import Scatter, output_file, show
from bokeh.plotting import figure, output_file, show
from bokeh.sampledata.autompg import autompg as df






def saveToPickle(my_object, fileName):
    print("Pickling my_object to file: "+str(fileName)+"...")
    pickle.dump(my_object, open(fileName, "wb"))
    print ("Saved.")

def getFromPickle(fileName):
    if os.path.isfile(fileName):
        my_object = pickle.load(open(fileName, "rb"))
        return my_object
    else:
        return None

def getNem():
    myFile = open('nem_allstates.csv')
    nemData = csv.DictReader(myFile)
    nem = {}

    for timePeriod in nemData:
        timeString = timePeriod['Time-ending']
		
        nem[timeString] = {
			 'nsw': {
				'price': timePeriod['NSW1 Price'],
				'demand':float(timePeriod['NSW1 Scheduled Demand']),
				'nonScheduled':float(timePeriod['NSW1 Non-scheduled']),
				'generation': float(timePeriod['NSW1 Generation']),
				'availability':float(timePeriod['NSW1 Availability']),
				},
			'vic': {
				'price': timePeriod['VIC1 Price'],
				'demand':float(timePeriod['VIC1 Scheduled Demand']),
				'nonScheduled':float(timePeriod['VIC1 Non-scheduled']),
				'generation': float(timePeriod['VIC1 Generation']),
				'availability':float(timePeriod['VIC1 Availability']),
				},
			'qld': {
				'price': timePeriod['QLD1 Price'],
				'demand':float(timePeriod['QLD1 Scheduled Demand']),
				'nonScheduled':float(timePeriod['QLD1 Non-scheduled']),
				'generation': float(timePeriod['QLD1 Generation']),
				'availability':float(timePeriod['QLD1 Availability']),
				},
			'sa': {
				'price': timePeriod['SA1 Price'],
				'demand':float(timePeriod['SA1 Scheduled Demand']),
				'nonScheduled':float(timePeriod['SA1 Non-scheduled']),
				'generation': float(timePeriod['SA1 Generation']),
				'availability':float(timePeriod['SA1 Availability']),
				},
			'tas': {
				'price': timePeriod['TAS1 Price'],
				'demand':float(timePeriod['TAS1 Scheduled Demand']),
				'nonScheduled':float(timePeriod['TAS1 Non-scheduled']),
				'generation': float(timePeriod['TAS1 Generation']),
				'availability':float(timePeriod['TAS1 Availability']),
				},
		}
    return nem

def getInterconnectorFlows():
	filename = 'interconnectorflows.csv'
	# Reading the file
	df = pd.read_csv(filename, index_col=0)
	# Creating the dict
	flows = df.transpose().to_dict()
	return flows








def chartFlowVsPrice(nem, flows):
	plots = []
	states = {
		'nsw': {'color': '#DC6BAD',}, 
		'qld': {'color': '#8C7AA9',}, 
		'vic': {'color': '#7192BE',}, 
		'sa': {'color': '#E88D67',}, 
		'tas': {'color': '#2F394D',}
		}
	
	for interconnectorAttribute in list(flows[list(flows)[0]]):
		for state in list(states):
			print "charting "+state+" "+ interconnectorAttribute
			flow = []
			price = []
			for time in list(nem):
				price.append(nem[time][state]['price'])
				flow.append(flows[time][interconnectorAttribute])
			
			symbol = 'o'
			if "Export" in interconnectorAttribute:
				symbol = '^'
			elif "Import" in interconnectorAttribute:
				symbol = 'v'
			
			plots.append({
				'x': flow,
				'y': price,
				'xlabel': interconnectorAttribute,
				'ylabel': state+' price',
				'title': interconnectorAttribute +' VS '+state+' Spot Price',
				'symbol': symbol,
				'color':states[state]['color']
			})
	return plots
	


# Handles using arrow keys to move through different subplots. 
# Adapted from this StackOverflow question http://stackoverflow.com/questions/18390461/scroll-backwards-and-forwards-through-matplotlib-plots
curr_plt_index = 0
plots = []
def key_event(e):
	global curr_plt_index

	if e.key == "right":
		curr_plt_index = curr_plt_index + 1
	elif e.key == "left":
		curr_plt_index = curr_plt_index - 1
	else:
		return
	curr_plt_index = curr_plt_index % len(plots)

	ax.cla()
	ax.plot(plots[curr_plt_index]['x'], plots[curr_plt_index]['y'], plots[curr_plt_index]['symbol'], color=plots[curr_plt_index]['color'])
	plt.ylabel(plots[curr_plt_index]['ylabel'])
	plt.xlabel(plots[curr_plt_index]['xlabel'])
	plt.title(plots[curr_plt_index]['title'])
	fig.canvas.draw()

nem = getNem()
flows = getInterconnectorFlows()
plots = chartFlowVsPrice(nem, flows)


fig = plt.figure()
fig.canvas.mpl_connect('key_press_event', key_event)
ax = fig.add_subplot(111)
plt.title("Use the < > arrow keys to scroll through plots.")
plt.show()



