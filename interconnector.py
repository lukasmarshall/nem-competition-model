import os
import csv
import numpy as np
import pickle

import bokeh
import matplotlib.pyplot as plt
import pandas as pd


# from bokeh.charts import Scatter, output_file, show
from bokeh.plotting import figure, output_file, show
from bokeh.sampledata.autompg import autompg as df





def getNem():

    myFile = open('nem_allstates.csv')
    nemData = csv.DictReader(myFile)
    nem = {}

    for timePeriod in nemData:
        timeString = timePeriod['Time-ending']
		
        nem[timeString]['nem'] = {
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


def chartHHI(nem):
    charts = []
    hhi = []
    price = []
    for category in categories:
        print category
        for timeString in list(nem):
            hhi.append(nem[timeString][category+'_HHI'])
            price.append(nem[timeString]['price'])

        plt.figure()
        plt.plot(hhi, price, 'o', col)
        
        plt.ylabel('price')
        plt.xlabel('hhi')
        plt.title("<="+category+" Band HHI vs Price")
        # plt.draw()
        plt.show()
        # p = figure(plot_width=800, plot_height=400, title="<="+category+" Band HHI vs Price")

        # # add a circle renderer with a size, color, and alpha
        # p.circle(hhi, price, size=2, color="navy", alpha=0.5)
        # output_file(category+"_hhi_scatter.html")
        # show(p)


def getInterconnectorFlows(filename, bidStacks):
	# Reading the file
	df = pd.read_csv(filename, index_col=0)
	# Creating the dict
	flows = df.transpose().to_dict(orient='series')
	return flows









bidStacks = {}
directory = 'interconnectorflows.csv'





# nem = getFromPickle('nem.pkl')
# if not nem:
#     nem = getNem()
#     # Calculate HHI for each category
#     i = 0
#     for timeString in list(nem):
#         print str(i)+' of '+str(len(list(nem)))
#         i += 1
#         for category in categories:
#             values = []
#             for retailer in list(bidStacks):
#                 # print retailer
#                 # print bidStacks[retailer][timeString]
#                 # print category +"  "+ str(bidStacks[retailer][timeString][category])
#                 values.append(float(bidStacks[retailer][timeString][category]))
                
#             hhi = calculateHHI(values)    
#             nem[timeString][category+"_HHI"] = hhi
#             if category == 'Cumulative':
#                 nem[timeString]['maxShareRetailer'] = getMaxShareRetailer(values, list(bidStacks))
#     saveToPickle(nem, 'nem.pkl')


# chartHHI(nem)


        


