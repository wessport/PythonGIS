# WES PORTER
# 14-FEB-2018
# USDA PROJECT - field_stats.py

# SCRIPT SUMMARY:
# Working with numpy arrays to calculate NDVI statistics for
# each agricultural field in study area

import sys, os
import datetime
import numpy as np
import gdal

test = 2 +2

print(test)

ndvi = r"E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\SR_NDVI_msc_cloudFree\LT05_L1GS_023_19850110_msc_masked.tif"
ds = gdal.Open(ndvi)

myarray = np.array(ds.GetRasterBand(1).ReadAsArray())

myarray.shape

myarray
