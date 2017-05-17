# WES PORTER
# 5/17/2017
# USDA PROJECT - soilCheck

# SCRIPT SUMMARY:
# Take AnnAGNPS cells polygons with bad soil type e.g. 'W' and determine actual
# soil type ID using geospatial/python approach.

import arcpy

# Define arcpy workspace
ws = "D:/Wes/Work/USDA/raw/Scripts/soil_check"

# Cell shapefile path
c = "D:/Wes/Work/USDA/raw/Scripts/soil_check/ms_annagnps_cells_64_may17.shp"

arcpy.env.workspace = ws

# Disable: 'Add results of geoprocessing operations to the display'
# Annoying otherwise
arcpy.env.addOutputsToMap = 0

# Problem cells
in_file = open(ws + '/problemCells.csv','r')

cells = []
for i in in_file:
    strFromFile = i.strip() # Remove line breaks
    parsedList = strFromFile.split(',') # Returns a list of strings
    cells.append(int(parsedList[0]))
in_file.close()

bad_soils = ['BP','LV','MR','W'] # Borrow pit, Levee, Marsh, Water

# Make a layer from the feature class
arcpy.MakeFeatureLayer_management(c, "cells_lyr")

# List of cells and majority soil ID
cellSoil = []

################################################################################

# INTERSECT ANALYSIS

for i in cells:

    # Select individual cells
    cell = i

    in_layer_or_view = "cells_lyr"
    selection_type="NEW_SELECTION"
    where_clause=""""GRIDCODE" = {}""".format(cell)

    arcpy.SelectLayerByAttribute_management(in_layer_or_view, selection_type,
                                            where_clause)

    # Perform intersect
    in_features="cells_lyr #;soil_merge.shp #"
    out_feature_class= ws + "/Intersect{}.shp".format(cell)
    join_attributes="ALL"
    cluster_tolerance="-1 Unknown"
    output_type="INPUT"

    arcpy.Intersect_analysis(in_features, out_feature_class, join_attributes,
                             cluster_tolerance, output_type)

    # Calculate add area for each soil type
    arcpy.AddField_management(out_feature_class,'AREA','DOUBLE','10','5')

    # Create our Update cursor to fill area data into attribute table
    UC = arcpy.da.UpdateCursor(out_feature_class,['SHAPE@AREA','AREA'])

    for row in UC:
        row[1] = row[0]
        UC.updateRow(row)
    del UC

    # Clear selected layer
    arcpy.SelectLayerByAttribute_management("cells_lyr", "CLEAR_SELECTION")

    # Calculate sum of area for each soil type in selected cell
    in_table= ws +"/Intersect{}.shp".format(cell)
    out_table= ws + "/intersect{}_stats".format(cell)
    statistics_fields="AREA SUM"
    case_field="MUSYM"
    arcpy.Statistics_analysis(in_table, out_table, statistics_fields,
                              case_field)

    # Create search cursor
    table_loc = ws + "/intersect{}_stats".format(cell)
    SC = arcpy.da.SearchCursor(table_loc,['MUSYM','SUM_AREA'])

    a = -1
    for row in SC:
        if (row[1] > a) and (row[0] not in bad_soils):
            majSoil = row[0]
            a = row[1]
    del SC

    cellSoil.append(str(cell) + ',' + majSoil + '\n')

    # Delete intermediate intersect files to save storage
    arcpy.Delete_management(ws + "/Intersect{}.shp".format(cell), data_type="")
    arcpy.Delete_management(ws + "/intersect{}_stats".format(cell),
                            data_type="")

# Delete any leftover temporary files
arcpy.Delete_management("cells_lyr", data_type="")

################################################################################

#  WRITE RESULTS  TO CSV

# Write results to a csv
out_file = open((ws + "/Cell_correctedSoilID.csv"),'w')

Header = 'Cell_ID,Soil_ID,' +'\n'
out_file.write(Header)

for i in cellSoil:
    out_file.write(i)

out_file.close()

# FINI
