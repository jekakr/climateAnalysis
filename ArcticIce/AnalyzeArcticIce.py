# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import numpy as np
import scipy
import matplotlib.pyplot as plt
from sets import Set
import csv
import collections
from collections import OrderedDict

def plotData(x, y, style, range, title):
    fig = plt.figure(figsize=(10, 10))
    plt.plot(x,y, style)
    plt.suptitle(title)
    plt.xlabel('year')
    plt.ylabel(range)
    

## The following algorithm smoothes data using n-point sliding box-car 
## smoothing. Stolen from http://users.aims.ac.za/~mike/python/env_modelling.html
## this is a better algorithm because it takes care of the "residuals" by 
## reflecting the data around the endpoints

def smoother(x, n):
     x_smooth = []
     L = len(x)
     store = zeros((n,1), float)  ## array of zeroes for each group of 
     for u in range(0, L-n):      ## used to produce smoothed value
          for v in range(0, n):  ##  add the values and divide by their number
               store[v] = x[u+v]
          av = float(sum(store)) / n  ## repeat for each value at center
          x_smooth.append(av)
     for u in range(L-n,L):  ## this takes care of the "residual" at the end
          for v in range(0, L-u-1):  ## average the values and find the smoothed value
               store[v] = x[u+v]
          av = float(sum(store)) / n
          x_smooth.append(av)
     return x_smooth
                    
def smootherGauss(x, n):
     coeff = [0.067, 0.242, 0.383, 0.242, 0.067]
## these are coefficients corresponding to Gaussian kernel of width 5
## taken from the web page homepages.inf.ed.ac.uk/rbf/HIPR2/gsmooth.htm
     x_smooth = []
     L = len(x)
     store = zeros((n,1), float)  ## array of zeroes for each group of 
     for u in range(0, L-n):      ## used to produce smoothed value
          for v in range(0, n):   ##  add the values multiplied by gaussian coefficients
               store[v] = x[u+v]
          av = 0
          for i in range(0, len(coeff)):
               av += float(coeff[i]) * float(store[i])
          x_smooth.append(av)
     for u in range(L-n,L):  ## this takes care of the "residuals" at the end
          for v in range(0, L-u-1):  ## average the values and find the smoothed value
               store[v] = x[u+v]
          av = 0
          for i in range(0, len(coeff)):
               av += float(coeff[i]*store[i])
          x_smooth.append(av)
     return x_smooth
                            
## in exponential smoothing each value is defined as
## s[0] = x[0] and s[t] = a x[t-1] + (1-a) s[t-1]
## where 0<a<1 is smoothing parameter.  Larger values of a
## give more weight to recent data but smoothing is worse
def smootherExp(x, a):
    x_smooth = []
    L = len(x)
    x_smooth.append(x[0])
    for u in range(1, L):
        store = a * float(x[u-1]) + (1-a) * float(x_smooth[u-1])
        x_smooth.append(store)
    return x_smooth

# <codecell>

infile = open("iceData.txt","r") ## read the data file
content = infile.read()
infile.close()
lines = content.split('\n') ## split up lines
data = []
for each in lines:  ## split each line into separate strings
    if len(each) < 1:
        continue          ## get rid of the empty list at the end
    temp = each.split()
    avg = round((float(temp[1]) + float(temp[2]) + float(temp[3]))/3., 2)  ## round to 2 decimal places
    data.append({'year':int(temp[0]), 'jul':float(temp[1]), 'aug':float(temp[2]), 'sep':float(temp[3]), 'avg':avg})    
    ## data contains year, July, August, September, and average ice extent in square kilometers

# <codecell>

years = []
julyExt = []  ## make plots of the data for the three months and average ice
augExt = []   ## extent over the years to get an idea of what the data looks like 
septExt = []
avgExt = []

colors=['r', 'b', 'c', 'g', 'm', 'y']

for each in data:
    years.append(each['year'])
    julyExt.append(each['jul'])
    augExt.append(each['aug'])
    septExt.append(each['sep'])
    avgExt.append(each['avg'])
    
plotData(years, julyExt, colors[0],'ice extend in square kilometers', 'July ice extent')
plt.ylim(3, 11)
plotData(years, augExt, colors[1],'ice extend in square kilometers', 'August ice extent')
plt.ylim(3, 11)
plotData(years, septExt, colors[2],'ice extend in square kilometers', 'September ice extent')
plt.ylim(3, 11)
plotData(years, avgExt, colors[3],'ice extend in square kilometers', 'Average Summer ice extent')
plt.ylim(3, 11)

# <codecell>

fig = plt.figure(figsize=(10, 10))
plt.xlabel('year')
plt.ylabel('extent of ice in square kilometers')
plt.title('Extent of Arctic ice')
plt.plot(years, julyExt, label='July', color=colors[0])
plt.plot(years, augExt, label='August', color=colors[1])
plt.plot(years, septExt, label='September', color=colors[2])
plt.plot(years, avgExt, label='Three months average', color=colors[3])
plt.legend(loc='lower left')
plt.show()
#plt.savefig("Ice-extent.png")

# <codecell>

avgExtBoxSmooth = smoother(avgExt, 5)  
## data smoothed over interval of 5 years

fig = plt.figure(figsize=(10, 10))
plt.xlabel('year')
plt.ylabel('extent of ice in square kilometers')
plt.title('comparing extent of Arctic ice data with data smoothed with Boxcar filter')
plt.plot(years, avgExt, label='raw data', color=colors[0])
plt.plot(years, avgExtBoxSmooth, label='smoothed data', color=colors[1])
plt.legend(loc='lower left')
plt.show()
#plt.savefig("Ice-extent-Boxcar-smoothed.png")

# <codecell>

avgExtGaussSmooth = smootherGauss(avgExt, 5)  
## data Gausian smoothed over interval of 5 years

fig = plt.figure(figsize=(10, 10))
plt.xlabel('year')
plt.ylabel('extent of ice in square kilometers')
plt.title('comparing extent of Arctic ice data with data smoothed with Gaussian filter')
plt.plot(years, avgExt, label='raw data', color=colors[0])
plt.plot(years, avgExtGaussSmooth, label='smoothed data', color=colors[1])
plt.legend(loc='lower left')
plt.show()
#plt.savefig("Ice-extent-Gaussian-smoothed.png")

# <codecell>

avgExtExpSmooth = smootherExp(avgExt, .7)  
## data smoothed exponentially with emphasis on later years

fig = plt.figure(figsize=(10, 10))
plt.xlabel('year')
plt.ylabel('extent of ice in square kilometers')
plt.title('comparing extent of Arctic ice data with data smoothed with Exponential filter')
plt.plot(years, avgExt, label='raw data', color=colors[0])
plt.plot(years, avgExtExpSmooth, label='smoothed data', color=colors[1])
plt.legend(loc='lower left')
plt.show()
#plt.savefig("Ice-extent-exponential-smoothed.png")

# <codecell>

dx = 5
x = years ## holds values of years
y = avgExt ## holds values of corresponding extents of ice
dy = [] ## five year differences
dydx = [] ## slopes over five years
xmid = [] ## midpoint for each five year interval

for i in range(0, len(y)-dx):
    temp = y[i+dx]-y[i]
    dy.append(temp)
    temp1 = temp/dx
    dydx.append(temp1)
    temp2 = float(x[i+dx]+x[i])/2.
    xmid.append(temp2)

plotData(xmid, dydx, colors[1], 'extent rate in square kilometers per year', 'Rate of change of average ice extent')
#plt.savefig("rate-of-change-of-extent.png")

# <codecell>

rate = []  ## this is the rate of change of Arctic sea ice extent
for i in range(0, len(dydx)):
    temp = [xmid[i], dydx[i]]
    rate.append(temp)

upTo1950 = []
after1950 = []
for each in rate:
    temp = each[1]
    if each[0] < 1950:
        upTo1950.append(temp)
    else:
        after1950.append(temp)

# <codecell>

## compute the area under above curve to find the change in extent of ice
from scipy.integrate import simps, trapz

## dx indicates the spacing of the data along the x axis.

## Compute the area using the composite trapezoidal rule.
#areaUpTo1950 = trapz(upTo1950, dx=1)
#print "area up to 1950 using trapezoidal rule =", areaUpTo1950
#areaAfter1950 = trapz(after1950, dx=1)
#print "area after 1950 using trapezoidal rule =", areaAfter1950
## Compute the area using the composite Simpon's rule.
areaUpTo1950 = simps(upTo1950, dx=1)
#print "area up to 1950 using Simpson's rule =", areaUpTo1950
areaAfter1950 = simps(after1950, dx=1)
ratio = areaAfter1950/areaUpTo1950
print "change in extent of sea ice up to 1950 =", round(areaUpTo1950, 2), "square kilometers"
print "change in extent of sea ice after 1950 =", areaAfter1950, "square kilometers"
print "ratio after 1950 to that before =", round(ratio, 2)

# <codecell>

## look at ratio of extent at the beginning and at the end of Summer
## to see if the distribution appears random or if there are certain
## extraordinary events
ratioJulyToSept = []
for i in range(len(julyExt)):
    temp = float(julyExt[i]) / float(septExt[i])
    ratioJulyToSept.append(temp)
fig = plt.figure(figsize=(10, 10))    
plt.xlabel('ratio of ice extent')
plt.ylabel('number of occurences')
plt.title('histogram ratio of extent of Arctic ice in July to that in September ')
plt.hist(ratioJulyToSept)
plt.show()
#plt.savefig("Ice-extent-histogram-ratio-July-September.png")

# <codecell>

from numpy import *
from matplotlib.pyplot import *

coefficients = polyfit(years, avgExt, 6)
polynomial = poly1d(coefficients)
xs = arange(1860, 2030, 1)
ys = polynomial(xs)
zeroes = roots(coefficients)
#print zeroes
for each in zeroes:    ## find the year at which ice extent goes to zero
    if int(each.real) > 2000:
        zero = int(each.real)
print "according to our fit Arctic ice will melt in the year", zero
fig = plt.figure(figsize=(10, 10))
plot(years, avgExt, 'o')
plot(xs, ys)
ylabel('extent of Arctic sea ice in square kilometers')
xlabel('year')
title('polynomial fit to averaged data for Arctic ice extent ')
show()
#savefig("Ice-extent-polynomial-fit.png")

# <codecell>

## now we use September data after 1979 and make linear fit and a polynomial 
## fit to the data

septExtSat = []
yearSat = []
for each in data:
    if each['year'] >= 1979:
        yearSat.append(each['year'])
        septExtSat.append(each['sep'])

## linear fit or polynomial of degree 1    
coeffLin = polyfit(yearSat, septExtSat, 1)
polynomial = poly1d(coeffLin)
xl = arange(1970, 2080, 1)
yl = polynomial(xl)
zeroes = roots(coeffLin)
#print zeroes
for each in zeroes:
    if int(each.real) > 2020:
        zero = int(each.real)
print "according to linear fit to satellite data Arctic ice will melt in the year", zero
fig = plt.figure(figsize=(10, 10))
plot(yearSat, septExtSat, 'o')
plot(xl, yl)
ylabel('extent of Arctic sea ice in square kilometers')
xlabel('year')
title('linear fit to September satellite data for Arctic ice extent ')
plt.ylim(0, 10)
plt.xlim(1970, 2070)
show()
#savefig("Ice-extent-satellite-linear-fit.png")

coeffPoly = polyfit(yearSat, septExtSat, 3)  ## fit polynomial of degree 3
polynomial = poly1d(coeffPoly)
xp = arange(1970, 2040, 1)
yp = polynomial(xp)
zeroes = roots(coeffPoly)
#print zeroes
for each in zeroes:             ## find the year at which ice extent goes to zero
    if int(each.real) > 2020:
        zero = int(each.real)
print "according to polynomial fit to satellite data Arctic ice will melt in the year", zero
fig = plt.figure(figsize=(10, 10))
plot(yearSat, septExtSat, 'o')
plot(xp, yp)
ylabel('extent of Arctic sea ice in square kilometers')
xlabel('year')
title('polynomial fit to September satellite data for Arctic ice extent ')
plt.ylim(0, 10)
plt.xlim(1970, 2070)
show()
#savefig("Ice-extent-satellite-polynomial-fit.png")

# <codecell>

## this is to locate the features in the data

fig = plt.figure(figsize=(10, 10))
plot(years, avgExt, 'ro')
suptitle('Extent of Arctic ice during cooling periods')
xlabel('year')
ylabel('extent in square kilometers')
plt.xlim(1900, 1960)
plt.ylim(8.5, 9.5)
## put vertical lines at the beginning and end of cooling window
axvline(x=1910)
axvline(x=1919)
axvline(x=1945)
axvline(x=1953)
plt.show()

# <codecell>

## extract the features by fitting a baseline curve to the data 
## that excludes the features, and then subtract the fitted baseline
## from the actual data to only look at the features

baseLine = []
yrsBase = []

for each in data:
    if each['year'] <= 1910:
        baseLine.append(each['avg'])
        yrsBase.append(each['year'])
    elif (each['year'] >= 1919 and each['year'] <= 1945):
        baseLine.append(each['avg'])
        yrsBase.append(each['year'])
    elif each['year'] >= 1953:
        baseLine.append(each['avg'])
        yrsBase.append(each['year'])

plotData(yrsBase, baseLine, colors[1], 'ice extend in square kilometers', 'Average Summer ice extent baseline only')

# <codecell>

coeffPoly = polyfit(yrsBase, baseLine, 6)  ## fit polynomial of degree 3
polynomial = poly1d(coeffPoly)
xp = years  ## we want a function that covers all the years
yp = polynomial(xp)

fig = plt.figure(figsize=(10, 10))
plot(yrsBase, baseLine, 'o')
plot(xp, yp)
ylabel('extent of Arctic sea ice in square kilometers')
xlabel('year')
title('polynomial fit to baseline data for Arctic ice extent ')
show()
#savefig("Ice-extent-baseline-polynomial-fit.png")

# <codecell>

baseLineSubtract = []
for i in range(len(years)):
    temp = avgExt[i] - yp[i]
    baseLineSubtract.append(temp)
    
plotData(years, baseLineSubtract, colors[1], 'ice extend in square kilometers', 'Average Summer ice extent baseline subtracted')
plt.xlim(1900, 1960)

# <codecell>

BaseLineSubtractBoxSmooth = smoother(baseLineSubtract, 3)  
## data smoothed over interval of 3 years

plotData(years, baseLineSubtractBoxSmooth, colors[1], 'ice extend in square kilometers', 'Average Summer ice extent baseline subtracted from data then boxcar smoothed')
plt.xlim(1900, 1960)

# <codecell>

## try subtracting from the smoothed data

baseLineSubtractBoxSmooth = []
for i in range(len(years)):
    temp = avgExtBoxSmooth[i] - yp[i]
    baseLineSubtractBoxSmooth.append(temp)
    
plotData(years, baseLineSubtractBoxSmooth, colors[1], 'ice extend in square kilometers', 'Average Summer ice extent baseline subtracted from boxcar smoothed data')
plt.xlim(1900, 1960)

# <codecell>


