# WES PORTER
# 14-FEB-2018
# USDA PROJECT - field_stats.py

# SCRIPT SUMMARY:
# Working with numpy arrays to calculate NDVI statistics for
# each agricultural field in study area

import sys, os
import datetime
import time
import numpy as np
import gdal
#import matplotlib.pyplot as plt

start_time = time.time()

# RASTERIZE FIELD POLYGONS
# http://www.gdal.org/gdal_rasterize.html

# Georeferenced extents of masked ndvi
# Obtained from gdalinfo LT05_L1GS_023_19850110_msc_masked.tif

# GDAL command ran from OSGEO shell
# gdal_rasterize -a Id -l MS_Agg_Fields_NLCD2001_final MS_Agg_Fields_NLCD2001_final.shp -a_nodata -9999 -te 133088.835 3716769.915 182948.835 3814599.915 -tr 30.0 30.0 -ot int16 MS_Agg_Fields_gdal.tif

################################################################################
# READ IN RASTER DATA AS ARRAYS

# Read in test ndvi
dataset = r"E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\SR_NDVI_msc_cloudFree\LT05_L1GS_023_19850110_msc_masked.tif"
ndvi = gdal.Open(dataset)

# Create numpy array
ndvi_array = np.array(ndvi.GetRasterBand(1).ReadAsArray())

# ndvi_array.shape
#
# ndvi_array

# TESTING GDAL RASTER

fr_gdal = r"E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\Field_raster\MS_Agg_Fields_gdal.tif"

f_gdal = gdal.Open(fr_gdal)

field_array = np.array(f_gdal.GetRasterBand(1).ReadAsArray())

field_array.shape
#
# field_array

#plt.imshow(field_array)

# Export array to textfile
#np.savetxt('E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/Field_raster/field.csv', field_array, fmt='%i', delimiter=',')

################################################################################

# Get unique list of field ids

unique_field = np.unique(field_array)
# len(unique_field)
# Get rid of no data
unique_field = unique_field[unique_field != -9999]
# len(unique_field)
np.savetxt('E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/Field_raster/unique_field.csv', unique_field, fmt='%s', delimiter=',')
# Consider optimizing this for performance later
# https://wiki.python.org/moin/PythonSpeed/PerformanceTips

# Threshold of minimum clean pixels neccessary to calculate stats
min_clean_ratio = 0.10

stats = np.zeros((5253,8))

# Calculate stats
count = 0
for field_id in unique_field:
    # Number of pixels in a given field
    total_pixels = len(ndvi_array[field_array == field_id])

    # Specify a condition - exclude no data values
    f_ndvi_values = ndvi_array[np.logical_and(field_array == field_id, ndvi_array != -9999)]

    # Calculate number of clean pixels
    clean_pixels = len(f_ndvi_values)
    clean_ratio = (float(clean_pixels)/total_pixels)

    if clean_ratio < min_clean_ratio:
        f_mean = -9999
        f_max = -9999
        f_min = -9999
        f_range = -9999
        f_std = -9999
        f_count = len(f_ndvi_values)
        f_area = -9999

    else:

        f_mean = np.mean(f_ndvi_values)
        f_max = np.max(f_ndvi_values)
        f_min = np.min(f_ndvi_values)
        f_range = f_max - f_min
        f_std = np.std(f_ndvi_values)
        f_count = len(f_ndvi_values)
        f_area = (30**2) * f_count

        count = count + 1
    stats[(count)] = field_id, f_mean, f_max, f_min, f_range, f_std, f_count, f_area

# Write stats to file

np.savetxt('E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/Field_raster/stats.csv', stats, fmt='%s', delimiter=',')

print("--- {} seconds ---".format(round(time.time() - start_time),2))
