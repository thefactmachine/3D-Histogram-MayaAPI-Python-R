import csv
def fnReadMainData():
    fileRandomFile = csv.reader(open("/Users/zurich/Google Drive/SITES/FactMachine-Final/3D-Histogram/histogram.csv","rU")) 
    lstRandom = []
    for lstLine in fileRandomFile:
        lstRandom.append(lstLine)
    return(lstRandom)
    
