# WES PORTER
# 5/17/2017
# USDA PROJECT - soilCheck

# SCRIPT SUMMARY:
# Take AnnAGNPS cells polygons with bad soil type e.g. 'W' and determine actual
# soil type ID using geospatial/python approach.

import arcpy

# Define arcpy workspace
ws = "C:/Users/wsp2sgis/Desktop/Soil_Check"
arcpy.env.workspace = ws

# Problem cells
cells = [51,82,83,91,92,93,101,102,103,1142,1152,1153,1301,1693,1791,1793,5942,10993,11003,11022,11873,11882,13253,13283,13301,13302,13303,13311,13312,13313,13381,13382,16023]

bad_soils = ['BP','LV','MR','W'] # Borrow pit, Levee, Marsh, Water

# Make a layer from the feature class
arcpy.MakeFeatureLayer_management("ms_agnps_Watercells_64.shp", "cells_lyr")

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

    arcpy.SelectLayerByAttribute_management(in_layer_or_view, selection_type, where_clause)

    # Perform intersect
    in_features="cells_lyr #;soil_merge.shp #"
    out_feature_class= ws + "/Intersect{}.shp".format(cell)
    join_attributes="ALL"
    cluster_tolerance="-1 Unknown"
    output_type="INPUT"

    arcpy.Intersect_analysis(in_features, out_feature_class, join_attributes, cluster_tolerance, output_type)

    # Clear selected layer
    arcpy.SelectLayerByAttribute_management("cells_lyr", "CLEAR_SELECTION")

    # Create search cursor
    SC = arcpy.da.SearchCursor(ws +'/Intersect{}.shp'.format(cell),['SHAPE@AREA','GRIDCODE','MUSYM'])

    a = -1
    for row in SC:
        if (row[0] > a) and (row[2] not in bad_soils):
            majSoil = row[2]
            a = row[0]
        gc = row[1]
    del SC

    cellSoil.append(str(gc) + ',' + majSoil + '\n')

    # Delete intermediate intersect files to save storage
    arcpy.Delete_management(ws + "/Intersect{}.shp".format(cell), data_type="")

# Delete any leftover temporary files
arcpy.Delete_management("cells_lyr", data_type="")

# Write results to a csv
out_file = open((ws + "/Cell_correctedSoilID.csv"),'w')

Header = 'Cell_ID,Soil_ID,' +'\n'
out_file.write(Header)

for i in cellSoil:
    out_file.write(i)

out_file.close()

# FINI
