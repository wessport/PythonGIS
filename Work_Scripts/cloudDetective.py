# WES PORTER
# 6/8/2017
# USDA PROJECT - cloudDetective

# SCRIPT SUMMARY:
# Working with python to identify cloudy NDVI pixels.

# C:\Python27\ArcGISx6410.3\python.exe cloudDetective.py
import arcpy
from os import listdir
from os.path import isfile, join

# Check out the Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")

# Define arcpy workspace
ws = "E:/Wes/Work/USDA/raw/North_Dakota/ND_Cloud_Detect/NDVI_LT5_2000/proj"
outLoc = "E:/Wes/Work/USDA/raw/North_Dakota/ND_Cloud_Detect/NDVI_LT5_2000/filtered/"

# Create a list of raster file names
files = [f for f in listdir(ws) if isfile(join(ws, f))]

# Assign cloud pixel threshold
cloudThresh = -0.05

# Raster calc to filter clouds from NDVI
for i in files:
    # Specify the input & output raster
    inRaster = ws + "/{}.tif".format(i)
    outRaster = outLoc + i[:-12] +"_con.tif"

    # Raster Calculator
    arcpy.gp.RasterCalculator_sa("""Con("{}">{},"{}",-1)""".format(inRaster,cloudThresh,inRaster), "{}".format(outRaster))
    print("\n Raster Calculation for: " + i + " - Complete. \n")

# Check in the Spatial Analyst extension now that you're done
arcpy.CheckInExtension("Spatial")

print("\n ***FINI*** \n")
