# PYTHON PROGRAMMING MINI PROJECT

import arcpy

# Define arcpy workspace - dependent on where project files are stored
ws = "C:/Users/wsp2sgis/Desktop/miniProj"

# Setting our workspace/environment
arcpy.env.workspace = ws

# Disable: 'Add results of geoprocessing operations to the display'
# Annoying otherwise
arcpy.env.addOutputsToMap = 0

################################################################################

# GENERATE CROSS SECTION POLYLINES

# Must create the empty feature class first
arcpy.CreateFeatureclass_management(ws,"crossSection.shp", "POLYLINE")

# Add a field for distance to outlet
arcpy.AddField_management('crossSection.shp','DIST','DOUBLE')

# Create our insert cursor
IC = arcpy.da.InsertCursor('crossSection.shp',['SHAPE@','DIST'])

# Create our coordinate data pairs in (mm) using T10geo.tif as reference

# Left and right side boundary points
pts_x = [100.11,100.716]

array = arcpy.Array()

# Generate list of cross section lines and coordinate pairs
for i in range(100324, 101812, 30): # 30mm or 3 cm - last name: Porter
    array = arcpy.Array([
        arcpy.Point(pts_x[0],(i/1000.00)),
        arcpy.Point(pts_x[1],(i/1000.00))
        ])
    polyline = arcpy.Polyline(array)
    dist = (i - 100324.00)/1000.00
    row_value = [polyline, dist]
    IC.insertRow(row_value)
    array.removeAll()

del IC

################################################################################

# INTERSECT ANALYSIS

for i in range(0,2110,10):
    if i == 0:
        # Define arguments
        time = 1
        time_formatted = '''"TIME"={}'''.format(time)
        in_features= ws +"/P2016-07-19.shp"
        out_feature_class= ws + "/P20160719_Select{}.shp".format(time)
        where_clause= time_formatted

        #Select individual time periods
        arcpy.Select_analysis(in_features, out_feature_class, where_clause)

        # Define arguments
        in_feature_1 = ws + "/crossSection.shp #;"
        in_feature_2 = ws + "/P20160719_Select{}.shp #".format(time)
        in_features = in_feature_1 + in_feature_2
        out_feature_class= ws + "/Intersect_Merge{}.shp".format(i)
        join_attributes="ALL"
        cluster_tolerance="-1 Unknown"
        output_type="INPUT"


        # Perform intersect analysis
        arcpy.Intersect_analysis(in_features,out_feature_class,join_attributes,
                                 cluster_tolerance,output_type)
        #Delete temp files
        in_data= ws + "/P20160719_Select{}.shp".format(time)
        arcpy.Delete_management(in_data, data_type="")

    else:

        # Define arguments
        time = i
        time_formatted = '''"TIME"={}'''.format(time)
        in_features= ws + "/P2016-07-19.shp"
        out_feature_class= ws + "/P20160719_Select{}.shp".format(time)
        where_clause= time_formatted

        #Select individual time periods
        arcpy.Select_analysis(in_features, out_feature_class, where_clause)

        # Define arguments
        in_feature_1 = ws + "/crossSection.shp #;"
        in_feature_2 = ws + "/P20160719_Select{}.shp #".format(time)
        in_features = in_feature_1 + in_feature_2
        out_feature_class= ws + "/Intersect_{}.shp".format(time)
        join_attributes="ALL"
        cluster_tolerance="-1 Unknown"
        output_type="INPUT"

        # Perform intersect analysis
        arcpy.Intersect_analysis(in_features,out_feature_class,join_attributes,
                                 cluster_tolerance,output_type)

        # Merge intersect results together
        input_1 = ws + "/Intersect_Merge{}.shp;".format(i-10)
        input_2 = " " + ws + "/Intersect_{}.shp".format(i)
        inputs = input_1 + input_2
        output= ws + "/Intersect_Merge{}.shp".format(i)
        arcpy.Merge_management(inputs, output)

        #Delete temp files
        in_data= ws + "/P20160719_Select{}.shp".format(time)
        arcpy.Delete_management(in_data, data_type="")

        in_data= ws + "/Intersect_{}.shp".format(time)
        arcpy.Delete_management(in_data, data_type="")

        in_data= ws + "/Intersect_Merge{}.shp".format(i-10)
        arcpy.Delete_management(in_data, data_type="")

# THIS IS BUGGED. DOESN'T REFRESH FOLDER LOCATION IN CATALOG WINDOW :/
# Refresh manually to see merge result
arcpy.RefreshCatalog(ws)

################################################################################

#  WRITE CHANNEL DATA TO CSV

# Create a search cursor to find each intersect line's length
in_file = ws + "/Intersect_Merge2100.shp"
SC = arcpy.da.SearchCursor(in_file, ['SHAPE@LENGTH'])

ch_length = []

for row in SC:
    ch_length.append(row[0])

del SC


# Add a field for channel width
arcpy.AddField_management(in_file,'WIDTH','DOUBLE','10','5')


# Create our Update cursor
UC = arcpy.da.UpdateCursor(in_file,['WIDTH'])

index = 0
for row in UC:
    row[0] = ch_length[index]
    index = index + 1
    UC.updateRow(row)

del UC

# Write primary results to csv

SC = arcpy.da.SearchCursor(in_file, ['TIME','FID_crossS','WIDTH','DIST'])

out_file = open((ws + "/Ch_Data_Output.csv"),'w')

Header = 'TIME,CROSS_SECTION_ID,AVERAGE_WIDTH,DISTANCE_TO_OUTLET' +'\n'
out_file.write(Header)

for row in SC:
    row_string = str(row[0]) + ',' + str(row[1]) + ','
    row_string = row_string + str(row[2]) + ',' + str(row[3]) + '\n'
    out_file.write(row_string)

out_file.close()

del SC

################################################################################

# GENERATE SUMMARY STATISTICS

# Define arguments

out_table= ws + "/Ch_Summary_Stats"
statistics_fields="WIDTH MEAN"
case_field="TIME"

# Calculate Summary Statistics
arcpy.Statistics_analysis(in_file, out_table, statistics_fields, case_field)


# Write Summary Statistics to csv
table_loc = ws + "/Ch_Summary_Stats"
SC = arcpy.da.SearchCursor(table_loc,['Rowid','TIME','FREQUENCY','MEAN_WIDTH'])

out_file = open((ws + "/Ch_Summary_Stats.csv"),'w')

Header = 'Rowid,TIME,FREQUENCY,AVERAGE_WIDTH' +'\n'
out_file.write(Header)

for row in SC:
    row_string = str(row[0]) + ',' + str(row[1]) + ','
    row_string = row_string + str(row[2]) + ',' + str(row[3]) + '\n'
    out_file.write(row_string)

out_file.close()

del SC

# FINI
