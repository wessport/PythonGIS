# WES PORTER
# 6/8/2017
# USDA PROJECT - gdal_createBat.py

# SCRIPT SUMMARY:
# Working with python to generate a GDAL bat file to mosaic list of images.

# C:\Python27\ArcGISx6410.3\python.exe gdal_createBat.py

ws = "E:/Wes/Work/USDA/tmp/"

in_file = open(ws +"ndvi_test2.txt",'r')
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

sprySet = set(spry)
setList = list(sprySet)

spryList = []

# Create separate lits for each unique Landsat row in collection
for i in setList:
    fileList = []
    for name in files:
        if (i in name):
            fileList.append(name)
    spryList.append(fileList)

for i in spryList[0]:
    for j in spryList[1]:
        doyI = i[13:16]
        doyJ = j[13:16]
        if (doyI == doyJ):
            out_string = "gdalwarp -t_srs EPSG:26916 " + str(i) + " " + str(j) + " " + str(i[0:6]) + str(i[9:16])+ "mosaic.tif"
