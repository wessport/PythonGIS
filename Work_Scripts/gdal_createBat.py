# WES PORTER
# 6/8/2017
# USDA PROJECT - gdal_createBat.py

# SCRIPT SUMMARY:
# Working with python to generate a GDAL bat file to mosaic list of images.

# C:\Python27\ArcGISx6410.3\python.exe gdal_createBat.py

ws = "E:/Wes/Work/USDA/tmp/"

in_file = open(ws + "ndvi_combined.txt", 'r')
files = []
for line in in_file:
    strFromFile = line.strip()  # Remove line breaks
    files.append(strFromFile)

# Create text file to send formatted string to
outFile = open(ws + "MS_gdal_mosaic.txt", 'w')

# Write header info
l1 = ":: WES PORTER\n"
l2 = ":: 6/8/2017\n"
l3 = ":: USDA PROJECT\n"
l4 = ":: Summary: Working with GDAL to reproject and mosaic NDVI data.\n"
l5 = "echo off\n"
l6 = "title GDAL NDVI MOSAIC\n"
header = l1 + l2 + l3 + l4 + l5 + l6
outFile.write(header)

gdal = "C:/OSGeo4W64/bin/gdalwarp.exe"  # GDAL location
proj = '"+proj=utm +zone=16 +datum=NAD83"'  # Projection

for i in files:
    for j in files:
        spI = i[0:6]
        rowI = i[6:9]
        yI = i[9:13]
        doyI = i[13:16]
        spJ = j[0:6]
        rowJ = j[6:9]
        yJ = j[9:13]
        doyJ = j[13:16]
        if (spI == spJ and yI == yJ and int(rowI) == (int(rowJ) - 1) and doyI == doyJ):
            out_string = gdal + " -t_srs " + proj + " " + \
                str(i) + " " + str(j) + " " + \
                str(i[0:6]) + str(i[9:16]) + "_msc.tif" + "\n"
            outFile.write(out_string)

footer = "echo Execution complete.\nPause"
outFile.write(footer)
outFile.close()

print("\n ~~~FINI~~~ \n")
