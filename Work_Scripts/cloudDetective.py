# WES PORTER
# 6/8/2017
# USDA PROJECT - cloudDetective

# SCRIPT SUMMARY:
# Working with python to identify cloudy NDVI pixels.

# C:\Python27\ArcGISx6410.3\python.exe cloudDetective.py
import arcpy
from arcpy.sa import *
# Define arcpy workspace
ws = r"E:\Wes\Work\USDA\raw\Scripts\cloud_detect"

# Specify the input & output raster
inRaster = ws + "/LT50300282000357.B3.tif"
outRaster = ws + "/LT50300282000_357_05.tif"

# Assign cloud pixel threshold
cloudThresh = -0.05

# Check out the Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")

arcpy.gp.RasterCalculator_sa("""Con("{}">{},"{}",-1)""".format(inRaster,cloudThresh,inRaster), "{}".format(outRaster))


# Check in the Spatial Analyst extension now that you're done
arcpy.CheckInExtension("Spatial")

print("\n ***FINI*** \n")
