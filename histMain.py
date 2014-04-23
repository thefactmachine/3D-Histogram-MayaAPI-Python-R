import maya.cmds as cmds
import sys
import os 
sys.path.append('/Users/zurich/Google Drive/SITES/FactMachine-Final/3D-Histogram')
import stvReadDataFile
reload(stvReadDataFile)
import stvMakeShaders
reload(stvMakeShaders)
import stvChunk
reload(stvChunk)
import stvCreateMesh
reload(stvCreateMesh)





def main():     
    lstDataMain = stvReadDataFile.fnReadMainData()
    
    # x,z,y : year, temp, day : left/right, up/down, top/bottom

    lstSelectedObjects = cmds.ls('STVPoly*')
    lstShadingGroup =  stvMakeShaders.fnCreateShaders() 
    
    if len(lstSelectedObjects) > 0:
        cmds.delete(lstSelectedObjects)
    fltTempScaler = float(2)
    fltHeight = float(20) / fltTempScaler
    fltSize = (float(40) / float(153)) * 1.03                                                                               #Define the size and add 1% for fun 
    
    fltXScaler = float(40) / float(152)
    fltXConstant = float(-20) - fltXScaler
    fltAspect = float(86) / float(153) * float(20)
    fltYScaler = fltAspect * float(2) / float(85)
    fltYConstant = (float(-1) * fltAspect) -  fltYScaler    

    def fnTempScalar(fltTemp):
        return((1.262 * fltTemp) -13.23)      

    def fnCreateCylinder(intX, intY, fltTemp, strFtr, strPlyName):                                                          #this generates a single cylinder
        strInstanceResult = cmds.instance(strPlyName, name = strPlyName + '_Factor' + strFtr + '_instance#')[0] 
        cmds.setAttr(strInstanceResult + '.scaleY', fltTemp)   
        fltTranslateHeight = fltSize * fltTemp / float(2) 
        fltXMovment = (float(intX) * fltXScaler) + fltXConstant 
        fltYMovement = (float(intY) * fltYScaler) + fltYConstant
        cmds.move(fltXMovment, fltTranslateHeight, fltYMovement, strInstanceResult, absolute=True)
        return(strInstanceResult)         
 
    def fnUniteMesh(lstChunk, intChunkNumber, strPName):        
        lstSelectedObjects = cmds.ls('STVPoly*')
        lstTranche = []
        for lstObj in lstChunk:
            fltAdjTemp = fnTempScalar(float(lstObj[2]))
            strInts = fnCreateCylinder(int(lstObj[1]), int(lstObj[0]), fltAdjTemp, str(lstObj[3]), strPName)         #NEED to add function here for temp
            lstTranche.append(strInts)        
        lstSelectedObjects = cmds.ls('STVPoly*')          
        if len(lstTranche) > 1:
            strPolyMeshName = 'STVPolyMesh_Factor' + str(lstObj[3]) + '_Tranche_' + str(intChunkNumber)
            cmds.polyUnite(lstTranche, n=strPolyMeshName)
            cmds.delete(strPolyMeshName, ch=True)
        cmds.delete(lstTranche)
        return(strPolyMeshName)                                         
    
    
    def fnCreateFactor(lstChunkedUp, intFactor):
        lstTranches = []
        for intChunkNum in range(0, len(lstChunkedUp)):
            strPolyName =  cmds.polyCube(sx=1, sy=1,sz=1, cuv=0, w=fltSize, h=fltSize, d=fltSize, name='STVPolyBase')[0]                #create the shape   
            strTrancheName = fnUniteMesh(lstChunkedUp[intChunkNum], intChunkNum, strPolyName)    
            lstTranches.append(strTrancheName)    
        strFactor = 'STVPoly_Factor_' + str(intFactor)
        cmds.polyUnite(lstTranches, n=strFactor)
        cmds.delete(strFactor, ch=True)
        return(strFactor)
    
    intFactorLimit = 11  + 1
    
    lstFactor = []
    for intFactNum in range(1,intFactorLimit):
        lstChunked = stvChunk.fnChunker(str(intFactNum), 50, lstDataMain)
        strFactor = fnCreateFactor(lstChunked, intFactNum)
        lstFactor.append(strFactor)
    
    def fnAssignMeshShader(lstShadingGroup, lstMesh):
        for intFactorNumber in range(1,intFactorLimit):                                                        #iterate through factors
            cmds.select(lstMesh[intFactorNumber-1], r=True)                                                    #select the mesh created    
            cmds.sets( e=True, forceElement = lstShadingGroup[intFactorNumber-1])                              #assign the mesh to a shader
    
    print(lstFactor)
    
    
    fnAssignMeshShader(lstShadingGroup, lstFactor)
 


    
    
if __name__ == '__main__':
    main()




    
    
    
    
    