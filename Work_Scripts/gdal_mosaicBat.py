# WES PORTER
# 24-JAN-2018
# USDA PROJECT - gdal_mosaicBat.py

# SCRIPT SUMMARY:
# Working with python to generate a GDAL bat file to mosaic list of ESPA images.

# C:\Python27\ArcGISx6410.3\python.exe gdal_createBat.py
import datetime
now = datetime.datetime.now()

ws = "E:/Wes/Work/USDA/tmp/"

in_file = open(ws + "MS_2005_request.txt", 'r')
files = []
for line in in_file:
    strFromFile = line.strip() +"_pixel_qa_prj.tif"  # Remove line breaks
    files.append(strFromFile)

# Create text file to send formatted string to
outFile = open(ws + "MS_gdal_mosaic.txt", 'w')

# Write header info
l1 = ":: WES PORTER\n"
l2 = ":: " + now.strftime("%Y-%m-%d ") + "\n"
l3 = ":: USDA PROJECT\n"
l4 = ":: Summary: Working with GDAL to reproject and mosaic NDVI data.\n"
l5 = "echo off\n"
l6 = "title GDAL NDVI MOSAIC\n"
header = l1 + l2 + l3 + l4 + l5 + l6
outFile.write(header)

gdal = "C:/OSGeo4W64/bin/gdalwarp.exe"  # GDAL location
proj = '"+proj=utm +zone=16 +datum=NAD83"'  # Projection

# Grab matching landsat rows, write GDAL arguments
for i in files:
    for j in files:
        sI = i[0:4]
        pI = i[10:13]
        rowI = i[13:16]
        dateI = i[17:25]
        sJ = j[0:4]
        pJ = j[10:13]
        rowJ = j[13:16]
        dateJ = j[17:25]

        if (sI == sJ and pI == pJ and dateI == dateJ and int(rowI) == (int(rowJ) - 1)):
            out_string = gdal + " -t_srs " + proj + " " + \
                str(i) + " " + str(j) + " " + \
                str(i[0:13]) + str(i[16:25]) + "_pixel_qa_msc.tif" + "\n" #_pixel_qa_msc
            outFile.write(out_string)

footer = "echo Execution complete.\nPause"
outFile.write(footer)
outFile.close()

print("\n ~~~FINI~~~ \n")
