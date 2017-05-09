# PGEO6050 [SPRING2017]
# Python Programming - Lab8
# 3/30/2017
# Wes Porter

# C:\Python27\ArcGISx6410.3\python.exe rastersLab.py

import arcpy
from arcpy import env

env.workspace = r"C:\Users\wsp2s\Desktop\Class9"

# CREATE A RASTER FROM ESRI GRID: ELEVATION

dem = arcpy.Raster(r"C:\Users\wsp2s\Desktop\Class9\elevation")

# Create slope of DEM
dem_slope = arcpy.sa.Slope(dem,"PERCENT_RISE")

# If you want to save the slope
dem_slope.save(r"C:\Users\wsp2s\Desktop\Class9\slope.tif")

# Create aspect of DEM
dem_aspect = arcpy.sa.Aspect(dem)

# Saving the aspect
dem_aspect.save(r"C:\Users\wsp2s\Desktop\Class9\aspect.tif")

# Finding the perfect location for our winter cabin
winterCabin = (dem_aspect > 157.5) & (dem_aspect < 202.5) & (dem_slope < 20)
