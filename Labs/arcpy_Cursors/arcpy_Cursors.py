# GEOG-650 [SPRING2017]
# Python Programming - Lab3
# 3/23/2017
# Wes Porter

# LEARNING ARCPY: CURSORS

import arcpy

# 1.) RETRIEVING INFORMATION FROM FC/FL TABLE

# Define workspace *TEMPORARY*
ws = "C:/Users/wsp2sgis/Desktop/Class7/dataCursor"
arcpy.env.workspace = ws

SC = arcpy.da.SearchCursor('airports.shp', ['NAME'])

# Create an empty list for the airport names to go into
names = []

#Iterate cursor to append airport names to empty list
for i in SC:
    names.append(i[0])

# Remove cursor
del i
del SC

# Write the list to a csv
fl = 'C:/Users/wsp2sgis/Desktop/Class7/dataCursor/airports.csv'
outFile = open(fl,'w')

for i in names:
    line = (i + ',' + '\n')
    outFile.write(line)

outFile.close()

# 2.) UPDATING INFORMATION WITHIN FC/FL TABLE

UC = arcpy.da.UpdateCursor('airports.shp',['STATE'])

# Iterate through table to update state name to AK

for i in UC:
    i[0] = 'AK'
    UC.updateRow(i)

# Remove cursor
del i
del UC
