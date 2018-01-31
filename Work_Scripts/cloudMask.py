# WES PORTER
# 29-JAN-2018
# USDA PROJECT - cloudMask.py

# SCRIPT SUMMARY:
# Working with arcpy to mask clouds from SR_NDVI

import arcpy, arcinfo
import datetime
from arcpy.sa import *
from os import listdir


# System time
now = datetime.datetime.now()

# Disable: 'Add results of geoprocessing operations to the display'
arcpy.env.addOutputsToMap = 0

# Set output Coordianate System to NAD83 UTM Z16
arcpy.env.outputCoordinateSystem = "PROJCS['NAD_1983_UTM_Zone_16N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-87.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"

# # Set snapRaster
# arcpy.env.snapRaster = "Z:/Wes/USDA/Data/Mississippi/MS_NDVI/ESPA_NDVI/unzipped/SR_NDVI_mosaiced/LT05_L1TP_023036_19950615_20160927_01_T1_sr_ndvi_prj.tif"

# Cell Size
arcpy.env.cellSize = 30.0

# Setting our workspace/environment
ws = "E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/tmp"
arcpy.env.workspace = ws

#Location of sr_ndvi
ndvi_loc = "Z:/Wes/USDA/Data/Mississippi/MS_NDVI/ESPA_NDVI/unzipped/SR_NDVI_mosaiced/"

#Location of pixel_qa band
pixel_qa_loc = "Z:/Wes/USDA/Data/Mississippi/MS_NDVI/ESPA_NDVI/unzipped/PIXEL_QA_mosaiced/"

# Create list of file names
ndvi_list = []
items = listdir(ndvi_loc)
for i in items:
    if i.endswith(".tif"):
        ndvi_list.append(i)
ndvi_list.sort()

pixel_qa_list = []
items = listdir(pixel_qa_loc)
for i in items:
    if i.endswith(".tif"):
        pixel_qa_list.append(i)
pixel_qa_list.sort()

# Create a dictionary for ndvi, pixel_qa pairs
img_dictionary = dict(zip(ndvi_list,pixel_qa_list))

# Mask our sr_ndvi
out_loc = "Z:/Wes/USDA/Data/Mississippi/MS_NDVI/ESPA_NDVI/unzipped/SR_NDVI_msc_cloudFree/"

arcpy.CheckOutExtension("spatial")

for ndvi, pixel_qa in img_dictionary.items():
    # Define which pixel values in the pixel_qa band to mask output
    # Arcpy argument must be a string

    # Create temporary binary cloud raster
    reclass_pixel_qa = arcpy.sa.Reclassify(pixel_qa_loc + pixel_qa, "Value", "66 0;68 1;72 1;96 1;130 0;136 1;160 1;224 1", "DATA")

    output_raster = Con((reclass_pixel_qa == 1) | IsNull(reclass_pixel_qa) | (reclass_pixel_qa == -32768), -9999, ndvi_loc + ndvi)

    # Set snapRaster
    arcpy.env.snapRaster = reclass_pixel_qa

    arcpy.management.SetRasterProperties(output_raster, None, None, None, "1 -9999", None)

    output_raster.save(out_loc + "{}_masked.tif".format(ndvi[:-4]))

    # Can't have more than 6 conditional statements inside one Con function
    # output_raster = Con(((pixel_qa_loc + pixel_qa) == 224) | ((pixel_qa_loc + pixel_qa) == 176) | ((pixel_qa_loc + pixel_qa) == 160) | ((pixel_qa_loc + pixel_qa) == 144) | ((pixel_qa_loc + pixel_qa) == 136) | ((pixel_qa_loc + pixel_qa) == 132) | ((pixel_qa_loc + pixel_qa) == 112) | ((pixel_qa_loc + pixel_qa) == 96) | ((pixel_qa_loc + pixel_qa) == 80) | ((pixel_qa_loc + pixel_qa) == 72) | ((pixel_qa_loc + pixel_qa) == 68) | ((pixel_qa_loc + pixel_qa) == 1), -9999, (ndvi_loc + ndvi))

    # output_raster.save(out_loc + "{}_masked.tif".format(ndvi[:-4]))

print("\n TASK COMPLETED:" + now.strftime("%Y-%m-%d %H:%M") + "\n")


# pixel_qa_loc = pixel_qa_loc + "/" + "LT05_L1TP_023036_19950615_20160927_01_T1_pixel_qa_prj.tif"
# ndvi_loc = ndvi_loc + "/" + "LT05_L1TP_023036_19950615_20160927_01_T1_sr_ndvi_prj.tif"

# pixel_qa = "Z:/Wes/USDA/Data/Mississippi/MS_NDVI/ESPA_NDVI/unzipped/PIXEL_QA_mosaiced/LT05_L1TP_023_19850923_pixel_qa_msc.tif"
# ndvi = "Z:/Wes/USDA/Data/Mississippi/MS_NDVI/ESPA_NDVI/unzipped/SR_NDVI_mosaiced/LT05_L1TP_023_19850923_msc.tif"
#
# arcpy.CheckOutExtension("spatial")
#
# outRas = Con((pixel_qa_loc == 224) | (pixel_qa_loc == 176) , -9999, ndvi_loc)
#
# outRas.save(out_loc + "{}_masked.tif".format(ndvi))

# | (pixel_qa == 160) | (pixel_qa == 144) | (pixel_qa == 136) | (pixel_qa == 132) | (pixel_qa == 112) | (pixel_qa == 96) | (pixel_qa == 80) | (pixel_qa == 72) | (pixel_qa == 68) | (pixel_qa == 1)

# reclass_pixel_qa = arcpy.sa.Reclassify(pixel_qa, "Value", "66 0;68 1;72 1;96 1;130 0;136 1;160 1;224 1", "DATA")
#
# outRas = Con((reclass_pixel_qa == 1) | IsNull(reclass_pixel_qa) | (reclass_pixel_qa == -32768), -9999, ndvi)
#
# # Set snapRaster
# arcpy.env.snapRaster = reclass_pixel_qa
#
# arcpy.management.SetRasterProperties(outRas, None, None, None, "1 -9999", None)
#
# outRas.save(out_loc + "{}_maskedTEST.tif".format("LT05_L1TP_023_19850923_msc"))

arcpy.CheckInExtension("spatial")

arcpy.ResetEnvironments()
