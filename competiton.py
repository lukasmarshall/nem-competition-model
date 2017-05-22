import os
import csv
import numpy as np
import pickle

import bokeh
import matplotlib.pyplot as plt


# from bokeh.charts import Scatter, output_file, show
from bokeh.plotting import figure, output_file, show
from bokeh.sampledata.autompg import autompg as df


categories = ['Cumulative', '-$500', '$0','$15', '$25', '$35', '$50','$100', '$300',  '$500', '$1000','$5000', '$99999']




def addBidStack(directory, filename, bidStacks):
    path = os.path.join(directory, filename)
    myFile = open(path)
    retailer = filename.split('.')[0]
    print retailer

    # Input data is normalised to kWh/kWp or MWh / MWp (equivalent)
    lines = csv.DictReader(myFile)
    stack = {}
    for line in lines:
        stack[line['Time-ending']] = line

    bidStacks[retailer] = stack
    return bidStacks


def getNem():
    myFile = open('nem.csv')
    nemData = csv.DictReader(myFile)
    nem = {}
    for timePeriod in nemData:
        timeString = timePeriod['Time-ending']
        nem[timeString] = {
            'price': timePeriod['NSW1 Price'],
            'demand':float(timePeriod['NSW1 Scheduled Demand']),
            'nonScheduled':float(timePeriod['NSW1 Non-scheduled']),
            'generation': float(timePeriod['NSW1 Generation']),
            'availability':float(timePeriod['NSW1 Availability']),
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
        plt.plot(hhi, price, 'o')
        
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





  
def calculateHHI(values):
    mysum = 0
    hhi = 0
    for value in values:
        mysum += float(value)
    if mysum > 0:
        for val in values:
            fraction = float(val) / float(mysum)
            percent = fraction * 100.0
            hhi += percent*percent
        return hhi
    else:
        return 0



# In the main loop, check which firm has the greatest share in any given time period, chart against price.
def getMaxShareRetailer(values, retailers):
    maxShareRetailer = retailers[0]
    maxShare = 0
    mysum = 0
    for value in values:
        mysum += float(value)
    if mysum > 0:
        for i in range(len(values)):
            fraction = float(values[i]) / float(mysum)
            if fraction > maxShare:
                maxShare = fraction
                maxShareRetailer = retailers[i]
        return maxShareRetailer
    else:
        return None











bidStacks = {}
directory = 'bidstacks'
for filename in os.listdir(directory):
    if filename.endswith(".csv") or filename.endswith(".py"): 
        bidStacks = addBidStack(directory, filename, bidStacks)
        continue
    else:
        continue




nem = getFromPickle('nem.pkl')
if not nem:
    nem = getNem()
    # Calculate HHI for each category
    i = 0
    for timeString in list(nem):
        print str(i)+' of '+str(len(list(nem)))
        i += 1
        for category in categories:
            values = []
            for retailer in list(bidStacks):
                # print retailer
                # print bidStacks[retailer][timeString]
                # print category +"  "+ str(bidStacks[retailer][timeString][category])
                values.append(float(bidStacks[retailer][timeString][category]))
                
            hhi = calculateHHI(values)    
            nem[timeString][category+"_HHI"] = hhi
            if category == 'Cumulative':
                nem[timeString]['maxShareRetailer'] = getMaxShareRetailer(values, list(bidStacks))
    saveToPickle(nem, 'nem.pkl')


chartHHI(nem)


        


