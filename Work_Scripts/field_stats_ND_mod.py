# WES PORTER
# 14-FEB-2018
# USDA PROJECT - field_stats.py

# SCRIPT SUMMARY:
# Working with numpy arrays to calculate NDVI statistics for
# each agricultural field in study area
from datetime import datetime
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
# Obtained from gdalinfo LT05_L1TP_030028_19950531_20160926_01_T1_sr_ndvi_proj_masked.tif

# GDAL command ran from OSGEO shell
# gdal_rasterize -a Id -l ND_Agg_Fields_gdal ND_Agg_Fields_gdal.shp -a_nodata -9999 -te 544824.177 5117058.451 582054.177 5177988.451 -tr 30.0 30.0 -ot int16 ND_Agg_Fields_gdal.tif

# HEY DUMMY! YOU MUST INSURE THAT THE FID AND ID MATCH OTHERWISE YOU'LL RUN INTO
# INDEXING ERRORS

################################################################################
# CALCULATE FIELD STATISTICS

ndvi_loc = r"E:\Wes\Work\USDA\raw\North_Dakota\ND_NDVI\SR_NDVI_masked"

#years = ["1985","1990","1995","2000"]
years = ["2005"]
for year in years:
    image_list =  glob.glob(ndvi_loc+"/*_{}*_masked.tif".format(year))

    for i in image_list:
        d = ntpath.basename(i)
        d = d[17:25]
        datetime_object = datetime.strptime(d, '%Y%m%d')

        # Calculate day of year
        doy = datetime_object.timetuple().tm_yday

        # Read in raster data as np arrays
        ndvi = gdal.Open(i)
        ndvi_array = np.array(ndvi.GetRasterBand(1).ReadAsArray())

        # Field raster
        fr_gdal =  r"E:\Wes\Work\USDA\raw\North_Dakota\ND_NDVI\Field_raster\ND_Agg_Fields_gdal.tif"
        f_gdal = gdal.Open(fr_gdal)
        field_array = np.array(f_gdal.GetRasterBand(1).ReadAsArray())

        # Mask NoData
        mask = (ndvi_array != -9999) & (field_array != -9999)
        nd = ndvi_array[mask]
        fi = field_array[mask]

        # Calculate stats
        # num_fields = np.unique(field_array).size - 1 # ignore -9999
        # print(num_fields)
        num_fields = 1754 + 1
        stats = np.array(range(0,num_fields))
        doys = np.full(stats.shape,doy)

        counts = np.bincount(fi, minlength=num_fields)
        sums = np.bincount(fi, nd, minlength=num_fields)

        avgs = sums / counts # will return nan if 0/0 i.e. field covered by clouds
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
        palette = range(0,1755)
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

        try:
            stats_out = np.append(stats_out,stats, axis = 0)
        except NameError:
            stats_out = stats

    np.savetxt(r"E:\Wes\Work\USDA\raw\North_Dakota\ND_NDVI\Field_raster\stats_out_{}.csv".format(year), stats_out, fmt='%s', delimiter=',')
    del stats_out

print("--- {} seconds ---".format(time.time() - start_time))

# Will need to replace 'nan' with 0
