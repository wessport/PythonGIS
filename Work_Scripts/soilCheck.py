# WES PORTER
# 5/17/2017
# USDA PROJECT - soilCheck

# SCRIPT SUMMARY:
# Take AnnAGNPS cells polygons with soil type 'W' and determine actual soil
# type ID using geospatial/python approach.

import arcpy

# Define arcpy workspace
ws = "C:/Users/wsp2sgis/Desktop/Soil_Check"
arcpy.env.workspace = ws

################################################################################

# INTERSECT ANALYSIS

# Problem cells
cells = [51,82,83,91,92,93,101,102,103,1142,1152,1153,1301,1693,1791,1793,5942,10993,11003,11022,11873,11882,13253,13283,13301,13302,13303,13311,13312,13313,13381,13382,16023]

# Make a layer from the feature class
arcpy.MakeFeatureLayer_management("ms_agnps_Watercells_64.shp", "cells_lyr")

# Select individual cells
cell = 51

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


# arcpy.Delete_management("cells_lyr", data_type="")
