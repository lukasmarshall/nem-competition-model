import os
import csv
import numpy as np
import pickle

import bokeh
import matplotlib.pyplot as plt
import pandas as pd



import marketUtils




# Generates data for plotting, returns as dict, is then plotted when key_event function is called. 

def chartFlowVsPrice(nem, flows):
	plots = []
	states = {
		'nsw': {'color': '#DC6BAD',}, 
		'qld': {'color': '#8C7AA9',}, 
		'vic': {'color': '#7192BE',}, 
		'sa': {'color': '#E88D67',}, 
		'tas': {'color': '#2F394D',}
		}
	
	attributes = list(flows[list(flows)[0]])
	attributes.sort()
	for interconnectorAttribute in attributes:
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
				'title': interconnectorAttribute +' vs '+state.upper()+' Spot Price',
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




nem = marketUtils.getNem()
flows = marketUtils.getInterconnectorFlows()
plots = chartFlowVsPrice(nem, flows)

fig = plt.figure()
fig.canvas.mpl_connect('key_press_event', key_event)
ax = fig.add_subplot(111)
plt.title("Use the < > arrow keys to scroll through plots.")
plt.show()



