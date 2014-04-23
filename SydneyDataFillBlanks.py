import csv
import os
import math

'''
This program processes Sydney temperature observations from 1.1.1859 ~
13.5.2012.  There are 56016 temperature observations. 

The program converts 3 date components to a date in 'dd-mm-yy' format

The program also inserts some missing temperature observations.  It
does this, where necesseary, by creating a new value to insert from 
extropolating the 3 previous temperature observtions.
'''


def main():
    def fnProcessLine(lstRawData):                                              #gets a row of raw data and returns the good bits
        lstProcessedData = []
        intYear = int(lstRawData[2])                                            #get year 
        intMonth = int(lstRawData[3])  
        intDay = int(lstRawData[4])  
        strDate = fnConstructDate(intDay, intMonth, intYear)
        fltTemp = float(lstRawData[5]) if lstRawData[5] <> '' else 'NA'
        return([intDay, intMonth, intYear, strDate, fltTemp])
        
    def fnNumberTo2DigitString(intNumber):                                      #gets 1 and returns '01', gets 12 returns '12'
        if intNumber < 10:
            strReturnValue = '0' + str(intNumber)
        else:
            strReturnValue = str(intNumber)
        return(strReturnValue)

    def fnConstructDate(intDay, intMonth, intYear):                             #takes 3 integers and constructs 'dd-mm-yy' date
        return(fnNumberTo2DigitString(intDay) + '-' + \
        fnNumberTo2DigitString(intMonth) + '-' + str(intYear))
    
    def fnRd2(fltHighPrecision):                                                #rounds to two decimal places
        fltExpand = fltHighPrecision * 100
        return(math.ceil(fltExpand)/100)
   
    def fnFillinBlanks(lstData):
        for i in range(3, len(lstData)):                                       #this interpolates missing temperatures. The first 3 values are okay                  
            fltTminus1 = lstData[i-1][4] * 12/21                               #yesterdays temperature (weighted by 12/21)
            fltTminus2 = lstData[i-2][4] * 6/21                                #day before yesterdays temperture  (weighted by 6/21)
            fltTminus3 = lstData[i-3][4] * 3/21                                #3 days ago temperature (weigted by 3/21)
            fltValueToInsert = fnRd2(fltTminus1 + fltTminus2 + fltTminus3)     #calculate the value to insert
            if  lstData[i][4] == 'NA':
                lstData[i][4] = fltValueToInsert
        return(lstData)
 
    def fnReadFile():
        dir = os.path.dirname(__file__)                                        #get current path
        strFileName = os.path.join(dir, 'SydneyOriginalData.csv')              #create path
        fileDataFile = csv.reader(open(strFileName,"rU"))                      #read the data
        lstRawData = [x for x in fileDataFile][1:]                             #create a list from CSV reader. Exclude 1st line.
        return(lstRawData)
       
    def fnWritefile(lstOutput):
        dir = os.path.dirname(__file__) 
        strWriteFile = os.path.join(dir, 'SydneyCleanData.csv')
        with open(strWriteFile, 'w') as fp:           
            fileHandle = csv.writer(fp, delimiter=',')
            fileHandle.writerows(lstOutput)
    
    lstRawData = fnReadFile()
    lstCleanData = [fnProcessLine(x) for x in lstRawData]
    lstBlanksFilled = fnFillinBlanks(lstCleanData)
    fnWritefile(lstBlanksFilled)
    
 
if __name__ == '__main__':
    main()  