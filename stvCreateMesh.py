import maya.cmds as cmds
def fnCreatePolyMesh(lstTranche, strMeshNumber, strFactor):
    #strPolyName =  cmds.polySphere(sx=10, sy=10, r=0.1,  name='STVPoly')[0]
    fltSize = 0.13
    strPolyName =  cmds.polyCube(sx=1, sy=1,sz=1, cuv=0, w=fltSize, h=fltSize, d=fltSize, name='STVPoly')[0]
    
    for i in range(0, len(lstTranche)):                                                                                 #one iteration is one tranche
        lstCurrentList = lstTranche[i]
        fltCurrentTemp = float(lstCurrentList[0]) * 1.7
        fltCurrentYear = float(lstCurrentList[1]) * 13
        fltCurrentDay =  float(lstCurrentList[2]) * 8
        strFactor =  str(lstCurrentList[3])                  
        instanceResult = cmds.instance(strPolyName, name = strPolyName + '_' + strFactor + '_instance#')           
        cmds.move(fltCurrentDay, fltCurrentTemp, fltCurrentYear, instanceResult)       
    strSelection = strPolyName + '_' + strFactor + '*'
    lstSelectedObjects = cmds.ls(strSelection)
    #print(lstSelectedObjects)
    #print('Created mesh ' + strMeshNumber)
    if len(lstSelectedObjects) > 1:
        strPolyName = 'STVPolyMesh_' + strFactor +  '_Tranche_' +  strMeshNumber
        cmds.polyUnite(lstSelectedObjects, n=strPolyName)
        cmds.delete(strPolyName, ch=True)                                                                                   #delete construction history
    cmds.delete(lstSelectedObjects) 
    return(strPolyName)
    
    
def fnCreateFactor(lstChunked, intFactorNumber):
    lstMeshCollection = []
    for intChunkCounter in range(0, len(lstChunked)):                                                                   #iterate through chunks and create meshes  
        strMesh = fnCreatePolyMesh(lstChunked[intChunkCounter], str(intChunkCounter), str(intFactorNumber))
        lstMeshCollection.append(strMesh)
    strFactorMesh = "STV_Factor_" + str(intFactorNumber)
    cmds.polyUnite(lstMeshCollection, n= strFactorMesh)
    cmds.delete(strFactorMesh, ch=True)
    return(strFactorMesh)
