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
# import matplotlib.pyplot as plt

# RASTERIZE FIELD POLYGONS
# http://www.gdal.org/gdal_rasterize.html

# Georeferenced extents of masked ndvi
# Obtained from gdalinfo LT05_L1GS_023_19850110_msc_masked.tif

# GDAL command ran from OSGEO shell
# gdal_rasterize -a Id -l MS_Agg_Fields_NLCD2001 MS_Agg_Fields_NLCD2001.shp -a_nodata -9999 -te 133088.835 3716769.915 182948.835 3814599.915 -tr 30.0 30.0 -ot int16 MS_Agg_Fields_gdal.tif

################################################################################
# READ IN RASTER DATA AS ARRAYS

# Read in test ndvi
dataset = r"E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\SR_NDVI_msc_cloudFree\LT05_L1GS_023_19850110_msc_masked.tif"
ndvi = gdal.Open(dataset)

# Create numpy array
ndvi_array = np.array(ndvi.GetRasterBand(1).ReadAsArray())

ndvi_array.shape

ndvi_array

# TESTING GDAL RASTER

fr_gdal = r"E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\Field_raster\MS_Agg_Fields_gdal.tif"

f_gdal = gdal.Open(fr_gdal)

field_array = np.array(f_gdal.GetRasterBand(1).ReadAsArray())

field_array.shape

field_array

# plt.imshow(field_array)

# Export array to textfile
#np.savetxt('E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/Field_raster/field.csv', field_array, fmt='%i', delimiter=',')

################################################################################

# Get unique list of field ids

unique_field = np.unique(field_array)
len(unique_field)
# Get rid of no data
unique_field = unique_field[unique_field != -9999]
len(unique_field)

# Consider optimizing this for performance later
# https://wiki.python.org/moin/PythonSpeed/PerformanceTips

# Threshold of minimum clean pixels neccessary to calculate stats
min_clean_ratio = 0.10

stats = {}
# Calculate stats
for field_id in unique_field:

        # Number of pixels in a given field
        total_pixels = len(ndvi_array[field_array == field_id])

        # Specify a condition - exclude no data values
        f_ndvi_values = ndvi_array[np.logical_and(field_array == field_id, ndvi_array != -9999)]

        # Calculate number of clean pixels
        clean_pixels = len(f_ndvi_values)
        clean_ratio = (float(clean_pixels)/total_pixels)

        if clean_ratio < min_clean_ratio:
            f_mean = ''
            f_max = ''
            f_min = ''
            f_range = ''
            f_std = ''
            f_count = len(f_ndvi_values)
            f_area = ''

        else:

            f_mean = np.mean(f_ndvi_values)
            f_max = np.max(f_ndvi_values)
            f_min = np.min(f_ndvi_values)
            f_range = f_max - f_min
            f_std = np.std(f_ndvi_values)
            f_count = len(f_ndvi_values)
            f_area = (30^2) * f_count

        stats[field_id] = f_mean, f_max, f_min, f_range, f_std, f_count, f_area

total_pixels = len(ndvi_array[field_array == 1])
total_pixels
test = ndvi_array[np.logical_and(field_array == 1, ndvi_array != -9999)]
np.mean(test)
clean_pixels = len(test)
clean_pixels
clean_ratio = (float(clean_pixels) / total_pixels)
clean_ratio

# stats[1] = 40, 10, 20

# Write stats to file
with open('E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/Field_raster/file.txt', 'w') as file:
    file.write('F_ID,F_AVG,F_MAX,F_MIN,F_RANGE,F_STD,F_COUNT,F_AREA' + '\n')
    for key, value in stats.iteritems():
        out_string = str(key) + ',' + str(value).strip('()').replace(" ", "") + '\n'
    file.write(out_string)
