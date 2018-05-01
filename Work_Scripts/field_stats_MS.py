# WES PORTER
# 14-FEB-2018
# USDA PROJECT - field_stats.py

# SCRIPT SUMMARY:
# Working with numpy arrays to calculate NDVI statistics for
# each agricultural field in study area

import time
import numpy as np
import gdal
import glob
import ntpath
import dateutil.parser as dparser

start_time = time.time()

# RASTERIZE FIELD POLYGONS
# http://www.gdal.org/gdal_rasterize.html

# Georeferenced extents of masked ndvi
# Obtained from gdalinfo LT05_L1GS_023_19850110_msc_masked.tif

# GDAL command ran from OSGEO shell
# gdal_rasterize -a Id -l MS_Agg_Fields_NLCD2001_final_fixed MS_Agg_Fields_NLCD2001_final_fixed.shp -a_nodata -9999 -te 133088.835 3716769.915 182948.835 3814599.915 -tr 30 30 -ot int16 MS_Agg_Fields_gdal.tif

################################################################################
# CALCULATE FIELD STATISTICS

# Read in test ndvi
# dataset = r"E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\SR_NDVI_msc_cloudFree\LT05_L1GS_023_19850110_msc_masked.tif"
# ndvi = gdal.Open(dataset)
# ndvi_array = np.array(ndvi.GetRasterBand(1).ReadAsArray())
#
# fr_gdal =  r"E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\Field_raster\MS_Agg_Fields_gdal.tif"
# f_gdal = gdal.Open(fr_gdal)
# field_array = np.array(f_gdal.GetRasterBand(1).ReadAsArray())
#
# np.savetxt(r'E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\Field_raster\unique.csv', np.unique(field_array), fmt='%s', delimiter=',')
#plt.imshow(field_array)

# Export array to textfile
#np.savetxt('E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/Field_raster/field.csv', field_array, fmt='%i', delimiter=',')

################################################################################

ndvi_loc = "E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/SR_NDVI_msc_cloudFree"

#years = ["1985","1990","1995","2000"]
years = ["2005"]
for year in years:
    image_list =  glob.glob(ndvi_loc+"/*_{}*_masked.tif".format(year))

    for i in image_list:
        image_date = dparser.parse(ntpath.basename(i), fuzzy=True)

        # Calculate day of year
        doy = image_date.timetuple().tm_yday

        # Read in raster data as np arrays
        ndvi = gdal.Open(i)
        ndvi_array = np.array(ndvi.GetRasterBand(1).ReadAsArray())

        # Field raster
        fr_gdal =  r"E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\Field_raster\MS_Agg_Fields_gdal.tif"
        f_gdal = gdal.Open(fr_gdal)
        field_array = np.array(f_gdal.GetRasterBand(1).ReadAsArray())

        # Mask NoData
        mask = (ndvi_array != -9999) & (field_array != -9999)
        nd = ndvi_array[mask]
        fi = field_array[mask]

        # Calculate stats
        num_fields = np.unique(field_array).size
        stats = np.array(range(0,num_fields))
        doys = np.full(stats.shape,doy)

        counts = np.bincount(fi, minlength=num_fields)
        sums = np.bincount(fi, nd, minlength=num_fields)

        avgs = sums / counts
        areas = np.multiply(counts, (30**2))
        stats = np.column_stack((stats,doys,avgs))

        # Max Min
        maxs = np.zeros(num_fields)
        np.maximum.at(maxs, fi, nd)
        mins = np.zeros(num_fields)
        np.minimum.at(mins, fi, nd)

        ranges = np.subtract(maxs,mins)

        # palette must be given in sorted order
        n = [-9999]
        palette = range(0,num_fields)
        palette = n + palette

        # key gives the new values you wish palette to be mapped to.
        avgs = np.nan_to_num(avgs)
        avgs = np.insert(avgs, 0, -9999)
        key = avgs
        index = np.digitize(field_array.ravel(), palette, right=True)
        f_avgs = key[index].reshape(field_array.shape)

        mask = (ndvi_array != -9999) & (f_avgs != -9999)
        f_a = f_avgs[mask]
        nd = ndvi_array[mask]
        nd_less_a = np.subtract(nd, f_a)
        nd_less_a_sq = np.square(nd_less_a)
        sums = np.bincount(fi, nd_less_a_sq, minlength=num_fields)
        avgs = sums / counts
        stds = np.sqrt(avgs)

        stats = np.column_stack((stats,maxs,mins,ranges,stds,counts,areas))
        stats = stats[:-1,] #Remove last row -- artifact of using bincount - not a real field

        try:
            stats_out = np.append(stats_out,stats, axis = 0)
        except NameError:
            stats_out = stats

    np.savetxt(r'E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\Field_raster\stats_out_{}.csv'.format(year), stats_out, fmt='%s', delimiter=',')
    del stats_out

#np.savetxt(r'E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\Field_raster\stats.csv', stats, fmt='%s', delimiter=',')

# print(len(range(0,5319)))
# print(len(avgs))
#np.place(fileds,np.unique(field_array),avgs)
#np.subtract(nd_out, fi, avgs)


#np.savetxt(r'E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\Field_raster\nd_out.csv', nd_out, fmt='%s', delimiter=',')

#np.savetxt(r'E:\Wes\Work\USDA\raw\Mississippi\MS_NDVI\Field_raster\maxs.csv', out, fmt='%s', delimiter=',')

# # Get unique list of field ids
# unique_field = np.unique(field_array)
#
# # Get rid of no data
# unique_field = unique_field[unique_field != -9999]

# Consider optimizing this for performance later
# https://wiki.python.org/moin/PythonSpeed/PerformanceTips

# # Threshold of minimum clean pixels neccessary to calculate stats
# min_clean_ratio = 0.10
#
# stats = np.zeros((5253,8))
# # stats[2]
# #np.savetxt('E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/Field_raster/stats.csv', stats, fmt='%s', delimiter=',')
#
# # f_ndvi_values = ndvi_array[np.logical_and(field_array == 20, ndvi_array != -9999)]
# f_ndvi_values = ndvi_array[field_array == 20]
# print(type(f_ndvi_values))
#
# np.savetxt(r'Z:\Scripts\scratch_virtualenv\cython_test\data\f_ndvi_values.csv', f_ndvi_values, fmt='%s', delimiter=',')
# # Calculate stats
# count = 0
# for field_id in unique_field:
#     # Number of pixels in a given field
#     # total_pixels = len(ndvi_array[field_array == field_id])
#
#     # Specify a condition - exclude no data values
#     f_ndvi_values = ndvi_array[np.logical_and(field_array == field_id, ndvi_array != -9999)]

    # # Calculate number of clean pixels
    # clean_pixels = len(f_ndvi_values)
    # clean_ratio = (float(clean_pixels)/total_pixels)
    #
    # if clean_ratio < min_clean_ratio:
    #     f_mean = -9999.0
    #     f_max = -9999.0
    #     f_min = -9999.0
    #     f_range = -9999.0
    #     f_std = -9999.0
    #     f_count = len(f_ndvi_values)
    #     f_area = -9999.0
    #
    # else:
    #
    #     f_mean = np.mean(f_ndvi_values)
    #     f_max = np.max(f_ndvi_values)
    #     f_min = np.min(f_ndvi_values)
    #     f_range = f_max - f_min
    #     f_std = np.std(f_ndvi_values)
    #     f_count = len(f_ndvi_values)
    #     f_area = (30**2) * f_count
    #
    #     count = count + 1
    #     stats[(count)] = field_id, f_mean, f_max, f_min, f_range, f_std, f_count, f_area

# Write stats to file
# with open('E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/Field_raster/file.txt', 'w') as file:
#     file.write('F_ID,F_AVG,F_MAX,F_MIN,F_RANGE,F_STD,F_COUNT,F_AREA' + '\n')
#     for key, value in stats.iteritems():
#         out_string = str(key) + ',' + str(value).strip('()').replace(" ", "") + '\n'
#         file.write(out_string)

print("--- {} seconds ---".format(time.time() - start_time))
