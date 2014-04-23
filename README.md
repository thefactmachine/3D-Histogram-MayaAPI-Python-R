There are 3 main processing stages:

PREPROCESS
1)  Preprocess SydneyOriginalData.csv using SydneyCleanData.csv and
then save the results in SydneyCleanData.csv . The purpose of this 
step is to identify missing temperature observations and then interpolate
between these.

PROCESS WITH R
2) Use R to process the data and exlude partial years and leap days
This is done using ProcessPointCloud.R. The results are saved
as histogram.csv.  Also, during this step, a small amount of noise
is added to the data, the data is scaled to (0,1) [i.e. normalised]
and then the data is split up into 11 quantiles. 

USE MAYA TO VISUALISE
3)
The process in Maya is kicked off with histMain.py.  The 
following lists purpose of relevant modules:

stvReadDataFile.py	Reads histogram.csv creates list
stvMakeShaders.py	Creates 11 shaders of various colours using the colors.csv file
stvChunk.py		This splits the data into chunks and then polygons are created for
			each chunk.  And then a polymesh is created for each chunk.
			Maya is too slow if a polymesh is created for all data points at the same time.
stvCreateMesh.py	This creates the mesh and then assigns shaders for each component. 

4) MAYA FILES
These are various representations of the data.  The proceses described above
are stored in 3DHistogram.mb.
