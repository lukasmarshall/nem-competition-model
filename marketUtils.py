import os
import csv
import numpy as np
import pickle
import pandas as pd


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
				'price': float(timePeriod['NSW1 Price']),
				'demand':float(timePeriod['NSW1 Scheduled Demand']),
				'nonScheduled':float(timePeriod['NSW1 Non-scheduled']),
				'generation': float(timePeriod['NSW1 Generation']),
				'availability':float(timePeriod['NSW1 Availability']),
				},
			'vic': {
				'price': float(timePeriod['VIC1 Price']),
				'demand':float(timePeriod['VIC1 Scheduled Demand']),
				'nonScheduled':float(timePeriod['VIC1 Non-scheduled']),
				'generation': float(timePeriod['VIC1 Generation']),
				'availability':float(timePeriod['VIC1 Availability']),
				},
			'qld': {
				'price': float(timePeriod['QLD1 Price']),
				'demand':float(timePeriod['QLD1 Scheduled Demand']),
				'nonScheduled':float(timePeriod['QLD1 Non-scheduled']),
				'generation': float(timePeriod['QLD1 Generation']),
				'availability':float(timePeriod['QLD1 Availability']),
				},
			'sa': {
				'price': float(timePeriod['SA1 Price']),
				'demand':float(timePeriod['SA1 Scheduled Demand']),
				'nonScheduled':float(timePeriod['SA1 Non-scheduled']),
				'generation': float(timePeriod['SA1 Generation']),
				'availability':float(timePeriod['SA1 Availability']),
				},
			'tas': {
				'price': float(timePeriod['TAS1 Price']),
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





def getBidStackFromFile(directory, filename, bidStacks):
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


def getBidStacks(state):
	bidStacks = {}
	directory = 'bidstacks/'+state
	for filename in os.listdir(directory):
		if filename.endswith(".csv") or filename.endswith(".py"): 
			bidStacks = getBidStackFromFile(directory, filename, bidStacks)
			continue
		else:
			continue
	return bidStacks


def _calculateHHI(values):
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


# In check which firm has the greatest share in any given time period
def _getMaxShareRetailer(values, retailers):
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


def getHHI():
	maxShareRetailers = getFromPickle('maxShareRetailers.pkl')
	hhi = getFromPickle('hhi.pkl')
	if not hhi:
		categories = ['Cumulative', '-$500', '$0','$15', '$25', '$35', '$50','$100', '$300',  '$500', '$1000','$5000', '$99999']
		bidStacks = getBidStacks('nsw')
		hhi = {}
		maxShareRetailers = {}
		nem = getNem()
		# Calculate HHI for each category
		for i, timeString in enumerate(list(nem)):
			print str(i)+' of '+str(len(list(nem)))
			hhi[timeString] = {}
			for category in categories:
				values = []
				for retailer in list(bidStacks):
					values.append(float(bidStacks[retailer][timeString][category]))
				hhi[timeString][category+"_HHI"] = _calculateHHI(values)  
				if category == 'Cumulative':
					maxShareRetailers[timeString] = _getMaxShareRetailer(values, list(bidStacks))
		saveToPickle(hhi, 'hhi.pkl')
		saveToPickle(hhi, 'maxShareRetailers.pkl')
	return hhi, maxShareRetailers

