# WES PORTER
# 6/8/2017
# USDA PROJECT - cloudfree_SetNull.py

# SCRIPT SUMMARY: Set No Data values 0 & -9999 to NULL

import arcpy

# Disable: 'Add results of geoprocessing operations to the display'
# Annoying otherwise
arcpy.env.addOutputsToMap = 0

# Define arcpy workspace
arcpy.env.workspace = "E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/MS_Cloudfree_Mosaic"

out_loc = "E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/MS_Cloudfree_Null"

in_file = open("E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/MS_Cloudfree_Mosaic/files.txt",'r')

mosaic_files = []
for i in in_file:
    strFromFile = i.strip()
    parsedList = strFromFile.split(' ')
    mosaic_files.append(parsedList[0])

in_file.close()

for i in mosaic_files:
    arcpy.gp.SetNull_sa(i, i, out_loc+"/"+i[:-4]+"_null.tif", "VALUE = 0 OR VALUE < -1 OR VALUE > 1")
    arcpy.gp.Float_sa(out_loc+"/"+i[:-4]+"_null.tif", out_loc+"/"+i[:-4]+"_null_flt.tif")
    

# MAKE SURE TO RUN gdalwarp_createBat.py TO SET NODATA VALUE AS -9999
