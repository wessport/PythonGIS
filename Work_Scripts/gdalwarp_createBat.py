# WES PORTER
# 7/20/2017
# USDA PROJECT -

# SCRIPT SUMMARY:
# Working with python to generate a GDAL bat file to warp list of images.

import datetime

ws = "E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/MS_Cloudfree_Null"

in_file = open(ws + "/files.txt",'r')

null_files = []
for i in in_file:
    strFromFile = i.strip()
    parsedList = strFromFile.split(' ')
    null_files.append(parsedList[0])

in_file.close()

out_file = open(ws + "/MS_gdalwarp.txt", 'w')

# Write header info
l1 = ":: WES PORTER\n"
l2 = ":: " + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + "\n"
l3 = ":: USDA PROJECT\n"
l4 = ":: Summary: Working with GDAL to warp mosaic_null NDVI data.\n"
l5 = "echo off\n"
l6 = "title GDALWARP NDVI_NULL \n"
header = l1 + l2 + l3 + l4 + l5 + l6
out_file.write(header)

for i in null_files:
    out_string = "gdalwarp -dstnodata -9999 " + i + " " + i[:-4] + "_warp.tif" +"\n"
    out_file.write(out_string)

footer = "echo Execution complete.\nPause"
out_file.write(footer)
out_file.close()

print("\n ~~~FINI~~~ \n")
