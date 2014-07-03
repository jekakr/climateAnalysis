# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
from sets import Set
import csv
import collections
from collections import OrderedDict

infile = open("output.txt","r")
content = infile.read()
infile.close()
lines = content.split('\n')
new_lines = []
for each in lines:
    temp = each.replace('NOT NAMED','NOT-NAMED')
    new_lines.append(temp)
hurricane_year = []
hurricane_data = [] ## contains storm id, lat/lon, wind speed/central pressure, and year of the hurricane
for each in new_lines:
    temp = each.split()
    if len(temp) < 1:  ## get rid of any empty lists
        continue
    if 'HURRICANE' in temp[8]:
        hurricane_year.append(int(temp[6]))  ## the year of the hurricane
        hurricane_data.append({'id':int(temp[0]), 'lat':float(temp[2]), 'lon':float(temp[3]), 'ws':int(temp[4]), 'cp':int(temp[5]), 'year':int(temp[6])})

hurricane_decade = {}
for each in hurricane_year:
    val = each // 10 * 10
    if val in hurricane_decade.keys():
        hurricane_decade[val] += 1
    else:
        hurricane_decade[val] = 1
decades = sorted(hurricane_decade.keys())  ## sorting keys in ascending order of decades
for decade in decades:
    print str(decade) + ':' + str(hurricane_decade[decade])
f1 = open('decade1.txt','w')
content = ''
for each in sorted(hurricane_decade.keys()):
    content += str(each) + ', ' + str(hurricane_decade[each]) + '\n'
f1.write(content)
f1.close()

# <codecell>

for each in hurricane_data:
    temp = each['year'] // 10 * 10
    each.update({'dec':temp})
uniqueID = Set()  ## this will record elements that already appeared
for each in hurricane_data:
    temp = each['id']
    uniqueID.add(temp)  ## set of unique identification numbers
#print uniqueID

hurDec = {}  ## use dictionary to count the number of hurricanes in a decade
for decade in decades:
    count = 0
    for each in hurricane_data:
        if each['dec'] == decade:
            count += 1
    hurDec[decade] = count
#print hurDec

# <codecell>

## in order to find minimum central pressure convert all zeros to 9999
for each in hurricane_data:
    if each['cp'] == 0:
        each['cp'] = 9999

minCentPressure = {}
for id in uniqueID:
    minCP = 9999 
    for each in hurricane_data:
        if each['id'] == id:
            if each['cp'] <= minCP:
                minCP = each['cp']
        minCentPressure[id] = minCP
#print minCentPressure

# <codecell>

decadeDict = {}
uniqueHurDecID = {}  ## this will hold unique IDs and their corresponding values of minimum central pressure
for decade in decades:
    seen = Set()
    count = 0
    decID = []
    for each in hurricane_data:
        if each['dec'] == decade:
## in the first step go directly to the else statement
            if each['id'] in seen: ## find minimum for each unique hurricane
                continue
            else:
## here we count each unique hurricane and write its ID with minimum CP
                count += 1
                seen.add(each['id'])
                decID.append(each['id'])
## we now have unique hurricanes, their number in each decade and min CP
    decadeDict[decade] = count
    uniqueHurDecID[decade] = decID
    print "Number of unique hurricanes during "+str(decade)+"s was "+str(count)
#print decadeDict

# <codecell>

#print uniqueHurDecID[2000]

# <codecell>

decIDspeed = {}
for decade in decades:
    temp = {}
    for key in minCentPressure.keys():
        val = minCentPressure[key]
        if key in uniqueHurDecID[decade]:
            temp.update({key:val})
    decIDspeed[decade] = temp
#print decIDspeed

# <codecell>

globalMin = 9999
globalMax = 0
for min in minCentPressure.values():
    if min <= globalMin:
        globalMin = min
    if min >= globalMax and min < 9999:
        globalMax = min
#print globalMin, globalMax

# <codecell>

## record frequency of occurrences within a minimum speed interval binned in intervals of ten
occurrence = {}  
occurDict = {}
for decade in decades:
    freqDict = {}  ## checking that intervals are correct
    frequency = []  ## list of occurrences within each interval
    speed = globalMin
    while speed < globalMax:
        count = 0
        for each in decIDspeed[decade].values():
            if each >= speed and each <= (speed + 10):
                count += 1 
        freqDict[speed] = count  ## check that proper intervals are used
        frequency.append(count)## for each interval, number of occurrences
        speed += 10    ## move on to next interval
    occurDict[decade] = freqDict    
    occurrence[decade] = frequency  ## for each decade corresponding frequencies of occurrences
#print occurDict

# <codecell>

#print occurrence

# <codecell>

sortedOccurrences = sorted(occurrence.keys())
for key in sortedOccurrences:
    print occurrence[key]

# <codecell>


