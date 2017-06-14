# WES PORTER
# 6/8/2017
# USDA PROJECT - gdal_createBat.py

# SCRIPT SUMMARY:
# Working with python to generate a GDAL bat file to mosaic list of images.

# C:\Python27\ArcGISx6410.3\python.exe gdal_createBat.py

ws = "E:/Wes/Work/USDA/tmp/"

in_file = open(ws +"ndvi.txt",'r')
files = []
for line in in_file:
    strFromFile = line.strip() # Remove line breaks
    files.append(strFromFile)

# Landsat rows that appear in file list
obs_sensors = []
obs_paths = []
obs_rows = []
obs_years = []
obs_doys = []
spry = []

for name in files:
    sensor = name[0:3]
    if (sensor not in obs_sensors):
        obs_sensors.append(sensor)
    path = name[3:6]
    if (path not in obs_paths):
        obs_paths.append(path)
    row = name[6:9]
    if (row not in obs_rows):
        obs_rows.append(row)
    year = name[9:13]
    if (year not in obs_years):
        obs_years.append(year)
        year = name[9:13]
    doy = name[13:16]
    if (doy not in obs_doys):
        obs_doys.append(doy)

    spry.append(name[0:13])

# Grab unique spry combinations
sprySet = set(spry)
sprySet = sorted(sprySet)
spryList = list(sprySet)

rowGroups = []
# Create separate lits for each unique Landsat row in collection
for i in spryList:
    fileList = []
    for name in files:
        if (i in name):
            fileList.append(name)
    rowGroups.append(fileList)

# Create text file to send formatted string to.
outFile = open(ws + "MS_gdal_mosaic.txt",'w')

# Write header info
l1 = ":: WES PORTER\n"
l2 = ":: 6/8/2017\n"
l3 = ":: USDA PROJECT\n"
l4 = ":: Summary: Working with GDAL to reproject and mosaic NDVI data.\n"
l5 = "echo off\n"
l6 = "title GDAL NDVI MOSAIC\n"
header = l1+l2+l3+l4+l5+l6
outFile.write(header)

for i in spryList:
    for j in spryList:
        spI = i[0:6]
        rowI = i[6:9]
        yI = i[9:13]
        spJ = j[0:6]
        rowJ = j[6:9]
        yJ = j[9:13]
        if (spI == spJ and yI == yJ and int(rowI) == (int(rowJ)-1)):
            # Format GDAL arguments for *possible mosaic combinations.
            for i in rowGroups[0]:
                for j in rowGroups[1]:
                    doyI = i[13:16]
                    doyJ = j[13:16]
                    if (doyI == doyJ):
                        out_string = "gdalwarp -t_srs EPSG:26916 " + str(i) + " " + str(j) + " " + str(i[0:6]) + str(i[9:16])+ "_msc.tif" + "\n"
                        outFile.write(out_string)

outFile.close()

print("\n ~~~FINI~~~ \n")
