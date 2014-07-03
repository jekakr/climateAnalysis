## read data into arrays of floats by year
def readData(textData):
        infile = open(textData,"r") ## read the data file
        content = infile.read()
        infile.close()
        lines = content.split('\n') ## split up lines

        data = []
        for each in lines:  ## split each line into separate strings
                if len(each) < 1:
                        continue          ## get rid of the empty list 
                                          ##at the end
                temp = each.split()
                data.append(temp)    ## data contains lists of data 
                                         ##for each year
## latitude, longitude, january - december rainfall in millimeters 
        floatData = []
        for each in data:
                tempLine = []
                for element in each:
                        temp = float(element)
                        tempLine.append(temp)
                floatData.append(tempLine)
        return floatData

def precipDuringYear(year):  ## read data during the year of interest
	temp = readData("PrecipData/precip."+str(year))
	return temp
## list of data for each year

precip = precipDuringYear(1965)
print precip[10]
print len(precip)
