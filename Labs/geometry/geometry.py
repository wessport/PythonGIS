# C:\Python27\ArcGISx6410.3\python.exe Scratch.py

#Working with polygons

# cHm = arcpy.da.InsertCursor('test.shp',['SHAPE@'])
# vectorPts = arcpy.Array()
# pts = arcpy.Point()
# pts.ID = 1
# pts.X = 0
# pts.Y = 0
# vectorPts.add(pts)
# pts.ID = 2
# pts.X = 10
# pts.Y = 0
# vectorPts.add(pts)
# pts.ID = 3
# pts.X = 15
# pts.Y = 5
# vectorPts.add(pts)
# pts.ID = 4
# pts.X = 0
# pts.Y = 5
# vectorPts.add(pts)
# poly = arcpy.Polygon(vectorPts)
# cHM.insertRow([poly])

import arcpy
import random as rd
import numpy as np

# Setting our workspace/environment
arcpy.env.workspace = "C:/Users/wsp2s/Desktop/Class8"

# Must create the empty feature class first
arcpy.CreateFeatureclass_management("C:/Users/wsp2s/Desktop/Class8","test.shp", "POINT")

# Add a field for our zone check
arcpy.AddField_management('test.shp','Zone','SHORT')

pts_x = []
pts_y = []
pts_zone = []
for i in range (1000):
    x = 1000.00 * rd.random()
    y = 1000.00 * rd.random()
    pts_x.append (float(x))
    pts_y.append (float(y))
    pts_zone.append(int(0))

meanX = np.mean(pts_x)
meanY = np.mean(pts_y)

# Define the distance from the mean for our zone
delta = 257

# Iterate through random points to check if they're inside
for i in range(1000):
    if (((pts_x[i]<meanX+delta)and(pts_x[i]>meanX-delta)) and ((pts_y[i]<meanY+delta) and(pts_y[i]>meanY-delta))):
            pts_zone[i] = 1

# Create our cursor to populate our random point data
IC = arcpy.da.InsertCursor('test.shp',['SHAPE@','Zone'])


for i in range(1000):
    IC.insertRow([arcpy.Point(pts_x[i],pts_y[i]),pts_zone[i]])

del i
del IC

# Create our polygon shapefile
arcpy.CreateFeatureclass_management("C:/Users/wsp2s/Desktop/Class8","poly.shp", "POLY")

IC = arcpy.da.InsertCursor('poly.shp',['SHAPE@'])
vectorPts = arcpy.Array()
pts = arcpy.Point()
pts.ID = 1
pts.X = meanX+delta
pts.Y = meanY+delta
vectorPts.add(pts)
pts.ID = 2
pts.X = meanX+delta
pts.Y = meanY-delta
vectorPts.add(pts)
pts.ID = 3
pts.X = meanX-delta
pts.Y = meanY-delta
vectorPts.add(pts)
pts.ID = 4
pts.X = meanX-delta
pts.Y = meanY+delta
vectorPts.add(pts)
poly = arcpy.Polygon(vectorPts)
cHM.insertRow([poly])

del IC
