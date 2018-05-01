# WES PORTER
# 29-JAN-2018
# USDA PROJECT - cloudMask.py

# SCRIPT SUMMARY:
# Working with arcpy to mask clouds from SR_NDVI

import sys, os
import arcpy, arcinfo
import datetime
from arcpy.sa import *
from os import listdir

def cloud_mask(state):
    """
    NOTE: In order for output to work NAS hould be mapped to Z:/ drive.
    Assuming no other drive is mapped in which case NAS may not map to Z:/.
    Masks clouds from NDVI by creating a binary masking raster.
    Uses ArcPy Reclassify and Con tools for the masking operations.
    SetProperties tool is used to strictly define nodata as -9999 instead of
    ESRI default nodata value.
    Outputs results to the NAS in respective state's NDVI directory.
    """

    # Disable: 'Add results of geoprocessing operations to the display'
    arcpy.env.addOutputsToMap = 0

    if state == 'MS':
        # Set output Coordianate System to NAD83 UTM Z16
        arcpy.env.outputCoordinateSystem = "PROJCS['NAD_1983_UTM_Zone_16N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-87.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"

        # Setting our workspace/environment
        ws = "E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/tmp"
        arcpy.env.workspace = ws

        # Location of sr_ndvi
        ndvi_loc = "Z:/Wes/USDA/Data/Mississippi/MS_NDVI/ESPA_NDVI/unzipped/sr_ndvi_mosaiced_2005/"

        # Check to make sure NAS is mapped to Z:/ drive
        if os.path.isdir(ndvi_loc) == False:
            print("NAS may not be currently mapped. Attempting to map drive...")
            os.system('pushd \\161.45.156.61\Public')
            if os.path.isdir(ndvi_loc) == True:
                print("NAS has been succesfully mapped.")

        # Location of pixel_qa band
        pixel_qa_loc = "Z:/Wes/USDA/Data/Mississippi/MS_NDVI/ESPA_NDVI/unzipped/PIXEL_QA_mosaiced_2005/"

        # Output file location
        out_loc = "Z:/Wes/USDA/Data/Mississippi/MS_NDVI/ESPA_NDVI/unzipped/sr_ndvi_mosaiced_2005/"

    elif state == 'ND':
        arcpy.env.outputCoordinateSystem = "PROJCS['NAD_1983_UTM_Zone_14N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-99.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"

        # Setting our workspace/environment
        ws = "E:/Wes/Work/USDA/raw/North_Dakota/ND_NDVI/tmp"
        arcpy.env.workspace = ws

        #Location of sr_ndvi
        #ndvi_loc = "Z:/Wes/USDA/Data/North_Dakota/ND_NDVI/ESPA_NDVI/unzipped/SR_NDVI_projected/"
        ndvi_loc = "E:/Wes/Work/USDA/raw/North_Dakota/ND_NDVI/tmp/nd_ndvi_2005/"

        #Location of pixel_qa band
        #pixel_qa_loc = "Z:/Wes/USDA/Data/North_Dakota/ND_NDVI/ESPA_NDVI/unzipped/PIXEL_QA_projected/"
        pixel_qa_loc = "E:/Wes/Work/USDA/raw/North_Dakota/ND_NDVI/tmp/nd_pixel_qa_2005/"

        # Output file location
        out_loc = "Z:/Wes/USDA/Data/North_Dakota/ND_NDVI/ESPA_NDVI/unzipped/SR_NDVI_masked/"

    # Cell Size
    arcpy.env.cellSize = 30.0

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

    if len(ndvi_list) == len(pixel_qa_list):
        # Create a dictionary for ndvi, pixel_qa pairs
        img_dictionary = dict(zip(ndvi_list,pixel_qa_list))

    else:
        return('NDVI list and pixel_qa list are different lengths!')

    # Mask our sr_ndvi
    start_time = datetime.datetime.now()

    arcpy.CheckOutExtension("spatial")

    for ndvi, pixel_qa in img_dictionary.items():

        # !! Arcpy argument must be a string !!

        # Define which pixel values in the pixel_qa band to mask output
        # Create temporary binary cloud raster in memory
        reclass_pixel_qa = arcpy.sa.Reclassify(pixel_qa_loc + pixel_qa, "Value", "66 0;68 1;72 1;96 1;130 0;136 1;160 1;224 1", "DATA")

        # Set snapRaster
        arcpy.env.snapRaster = reclass_pixel_qa

        output_raster = Con((reclass_pixel_qa == 1) | IsNull(reclass_pixel_qa) | (reclass_pixel_qa == -32768), -9999, ndvi_loc + ndvi)

        # Define nodata value as -9999
        arcpy.management.SetRasterProperties(output_raster, None, None, None, "1 -9999", None)

        output_raster.save(out_loc + "{}_masked.tif".format(ndvi[:-4]))

    # Current system time
    now = datetime.datetime.now()

    elapsed_time = (float(start_time.strftime("%S")) - float(now.strftime("%S"))) / 60

    print("\n TASK COMPLETED:" + now.strftime("%Y-%m-%d %H:%M") + "\n" + "ELAPSED TIME: " + str(elapsed_time) + "\n")

    arcpy.CheckInExtension("spatial")

    arcpy.ResetEnvironments()

if __name__ == '__main__':
    cloud_mask(sys.argv[1])
