# WES PORTER
# 11-JUNE-2018
# LUCA PROJECT - luca_insert.py

# "C:\Python27\ArcGIS10.4\python.exe"

# SCRIPT SUMMARY:
# Working with Arcpy to insert E911 address locations into Census address bank

import arcpy

# Define workspace
ws = "C:/Users/wPorter/Data/LUCA2020"

# E911 addresses
in_file = ws + "/LUCA2020.gdb/Trousdale_E911_additions"

# Census addresses
census_file = ws + "/LUCA2020.gdb/Trousdale_census_address_list_test"

# Create a search cursor to collect E911 addresses
SC = arcpy.da.SearchCursor(in_file, ['SHAPE@','Trousdale_E911_address_list_STNUM','Trousdale_E911_address_list_NAME','Trousdale_E911_address_list_TYPE','Trousdale_E911_address_list_ZIP'])

# Create insert cursor
IC = arcpy.da.InsertCursor(census_file,['SHAPE@','ENTITY','ACTION_','STATEFP','COUNTYFP','HOUSENUMBER','STREETNAME','ZIP','USE','ADDRESS'])

for row in SC:

    # Handle missing zip codes
    try:
        zip = int(row[4])
    except ValueError:
        zip = None

    # Clean duplicate road types
    stnum = row[1]
    n = row[2].rsplit(None, 1)[-1] # e.g. MELROSE RD RD
    b = row[2].rsplit(None, -1)[0]
    t = row[3]

    if(n==t):
        street_name = row[2]
    else:
        street_name = row[2] + ' ' + row[3]

    if(stnum==b):
        address = street_name
    else:
        address = row[1] + ' ' + street_name

    # Format row for insert
    insert_row_value = [row[0],'ST47','A','47','169',row[1],street_name,zip,'L',address]

    # Insert row
    IC.insertRow(insert_row_value)

del SC
del IC
