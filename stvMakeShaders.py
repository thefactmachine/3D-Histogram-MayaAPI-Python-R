import maya.cmds as cmds
import csv

def fnGetColorFile():    
    #read in file of 11 color values, assign the colors to lstColor
    fileColorFile = csv.reader(open("/Users/zurich/Google Drive/SITES/FactMachine-Final/3D-Histogram/colors.csv","rU"))
    dictColorVector = {}
    i = 1
    for lstLine in fileColorFile:
        lstInteger = [int(element) for element in  lstLine]
        dictColorVector[i] = lstInteger
        i = i + 1
    return(dictColorVector)    

def fnDeleteShaders():
    lstObjectList =  cmds.ls('STVShader*')    
    if len(lstObjectList) > 0:
        cmds.delete(lstObjectList)
    

def fnCreateShaders():
    dictColor = fnGetColorFile()
    fnDeleteShaders()
    lstShadingGroup = []
    for intCounter in range(1,12):                                                                  #iterates from 1 to 11
        strShaderName = 'STVShader' + str(intCounter)
        strShader = cmds.shadingNode('lambert', asShader=True, name=strShaderName)            
            
        #create shading group
        strSGName = strShaderName + 'SG' + str(intCounter)
        strResult = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name = strSGName)
        #print(strResult)
        red = float(dictColor[intCounter][0]) / 255
        green = float(dictColor[intCounter][1]) / 255
        blue =  float(dictColor[intCounter][2]) / 255
        strValues = str(intCounter) + ":" + str(red) + " " + str(green) + "   " + str(blue)
        #print(strValues)

        cmds.setAttr(strShader + ".color", red , green, blue, type="double3")           
            
        #connect shader to shading group
        cmds.connectAttr(strShaderName + '.outColor', strSGName + '.surfaceShader')
        lstShadingGroup.append(strSGName)
    return(lstShadingGroup)
 