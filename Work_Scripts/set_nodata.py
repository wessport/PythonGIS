# WES PORTER
# 05-FEB-2018
# USDA PROJECT - set_nodata.py

# SCRIPT SUMMARY:
# Working with numpy and GDAL to remove ESRI nodata garbage
# Followed guide @ https://geohackweek.github.io/raster/04-workingwithrasters/

# E:\GitHub\PythonGIS\Work_Scripts\set_nodata.py

import sys, os
import datetime
import numpy as np

from os import listdir
from osgeo import gdal


# Reclassify ESRI NoData values
def ndvi_nodata(image):
    '''Replace ESRI NoData values with appropriate NoData value '''
    image[image == -32768] = -9999
    return image

def nd_ndvi_nodata(file_name):
    image_loc = file_name

    # Read in raster using gdal

    ds = gdal.Open(image_loc)
    ndvi_band = ds.GetRasterBand(1)
    ndvi = ndvi_band.ReadAsArray()

    # Reclassify ESRI NoData values using function above
    ndvi_fixed = ndvi_nodata(ndvi)

    # Save the NDVI Raster to Disk
    out_loc = "E:/Wes/Work/USDA/raw/North_Dakota/ND_NDVI/SR_NDVI_masked_fixed/"
    driver = gdal.GetDriverByName('GTiff')
    new_dataset = driver.Create(out_loc + image_loc,
                                ds.RasterXSize,    # number of columns
                                ds.RasterYSize,    # number of rows
                                1,                 # number of bands
                                gdal.GDT_Int16 )  # datatype of the raster - http://www.gdal.org/gdal_8h.html#a22e22ce0a55036a96f652765793fb7a4af5cbd2f96abffd9ac061fc0dced5cbba
    new_dataset.SetProjection(ds.GetProjection())
    new_dataset.SetGeoTransform(ds.GetGeoTransform())

    # Now we need to set the band's nodata value to -9999
    new_band = new_dataset.GetRasterBand(1)
    new_band.SetNoDataValue(-9999)

    # And finally, let's write our NDVI array
    new_band.WriteArray(ndvi_fixed)
    new_band.FlushCache()

    del new_dataset
    del ds

# Create list of file names to correct
start_time = datetime.datetime.now()

ndvi_loc = "E:/Wes/Work/USDA/raw/North_Dakota/ND_NDVI/SR_NDVI_masked"
ndvi_list = []

items = listdir(ndvi_loc)
for i in items:
    if i.endswith(".tif"):
        ndvi_list.append(i)
ndvi_list.sort()

for i in ndvi_list:
    nd_ndvi_nodata(i)

# Current system time
now = datetime.datetime.now()

elapsed_time = (float(start_time.strftime("%S")) - float(now.strftime("%S"))) / 60

if elapsed_time < 0:
    elapsed_time = 0

print("\n TASK COMPLETED:" + now.strftime("%Y-%m-%d %H:%M") + "\n" + "ELAPSED TIME: " + str(elapsed_time) + "\n")
