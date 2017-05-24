import os
import csv
import numpy as np
import pickle
import pandas as pd


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





def getBidStack(directory, filename, bidStacks):
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