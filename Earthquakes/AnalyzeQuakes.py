# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
from sets import Set
import csv
import collections
from collections import OrderedDict

infile = open("data","r") ## read the data file
content = infile.read()
infile.close()
lines = content.split('\n') ## split up lines
#print lines

data = []
for each in lines:  ## split each line into separate strings
    if len(each) < 1:
        continue          ## get rid of the empty list at the end
    temp = each.split()
    dec = int(temp[0]) // 10 * 10
## data contains lists of data for each year
    data.append({'year':int(temp[0]), 'lat':float(temp[1]), 'lon':float(temp[2]), 'depth':float(temp[3]), 'mag':float(temp[4]), 'dec':dec})     
#print data
## data contains year, lattitude, longitude, depth, magnitude and decade it occurs in 

# <codecell>

import math

#import sys
#center = list(raw_input('Enter lattitude, longitude to compute distance from')) 
#dates = list(raw_input('Enter start year, end year (between 1900 and 2008)'))
#thr_in = float(raw_input('Enter the magnitude threshold'))

#start = dates[0]
#end = dates[1]
#thr = float(thr_in)
seattle = [47.62, -122.333]
start = 1900
end = 2008
thr = 5.0

allQuakes = []
for each in data:
    if each['year'] >= start and each['year'] <= end:
        if each['mag'] >= thr:
            allQuakes.append(each)
            
def distance(origin, destination):  ## function to compute 
    lat1, lon1 = origin             ## distance between two coordinates
    lat2, lon2 = destination
    radius = 6373.0 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = (radius * c)/1.6 # in miles
    
    return d

## IMPORTANT: change seattle to center for user input
centerLoc = seattle
neighborQuake = {}
for each in allQuakes:
    quakeLoc = [each['lat'], each['lon']]
    quakeMag = each['mag']
    quakeYear = each['year']
    dist = distance(centerLoc, quakeLoc)
    if dist <= 100:
        neighborQuake[quakeYear] = [quakeMag, tuple(quakeLoc)]
        
orderedYears = sorted(neighborQuake.keys())
for year in orderedYears:
    print "In year "+ str(year)+ " earthquake of magnitude "+ str(neighborQuake[year][0])+ " struck at location "+str(neighborQuake[year][1])
    
print 'There were ' + str(len(neighborQuake)) + ' earthquakes of magnitude ' + str(thr) + ' or higher between the years ' + str(start) + ' and ' + str(end) + ' within 100 miles of the location '+str(tuple(centerLoc))

# <codecell>

## find how many earthquakes occur each decade with magnitude above 5 and 
## plot average magnitude on bubble chart with frequency represented by the
## size of the bubble

avgMagDepthFreq = {}
decade = 1900
while decade <= 2000:
    count = 0
    avgMag = 0
    avgDepth = 0
    for each in data:
        if each['mag'] >= 5.0:
            if each['dec'] == decade:
                count += 1
                avgMag += each['mag']
                avgDepth += each['depth']
    avgMag = round(avgMag/count, 2)  
    avgDepth = round(avgDepth/count, 2) 
    avgMagDepthFreq[decade] = [avgMag, avgDepth, count]
    decade += 10
print avgMagDepthFreq

# <codecell>

orderedKeys = sorted(avgMagDepthFreq.keys())
for key in orderedKeys:
    print [str(avgMagDepthFreq[key][2]),key,avgMagDepthFreq[key][0],avgMagDepthFreq[key][1],avgMagDepthFreq[key][2]]

# <codecell>


