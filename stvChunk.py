'''
Splits a list of data into a number of chunks determined by intChunkAmount
The list is initially filtered to contain only the relevant factor
The first 0..n-1 lists will be of length intChunkAmount
The last list will contain the remaining observations.
The number of lists returned will be (NumberObservations Div intChunkAmount) + 1
'''
def fnChunker(strFactor, intChunkAmount, lstData):
    lstSource = [i for i in lstData if i[3] == strFactor]                      #lstSource contains the relevant factor (i.e. strFactor)
    lstChunkPoints = range(0,len(lstSource), intChunkAmount)                   #a list of cutoff points for the chunks 
    lstChunked = []
    for i in lstChunkPoints:
        if((i + intChunkAmount) < len(lstSource)):            
            lstTmp = lstSource[i:i+intChunkAmount]
            lstChunked.append(lstTmp)
        else:
            lstTmp = lstSource[i:len(lstSource)]
            lstChunked.append(lstTmp)
    return(lstChunked)            
