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

a = "LC80230362015"
myList = []

for name in files:
    if (a in name):
        myList.append(name)

print(myList)
