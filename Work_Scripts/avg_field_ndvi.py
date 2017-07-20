# WES PORTER
# 7/20/2017
# USDA PROJECT - avg_field_ndvi.py

# SCRIPT SUMMARY:
# Working with arcpy to avg NDVI values for a test field

import arcpy
import glob

# Disable: 'Add results of geoprocessing operations to the display'
arcpy.env.addOutputsToMap = 0

# Setting our workspace/environment
ws = "E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/test_field"
arcpy.env.workspace = ws

ndvi_loc = "E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/MS_Cloudfree_Null"

years = ["1985","1990","1995"]
for year in years:
    image_list =  glob.glob(ndvi_loc+"/LT5023{}*_msc_null.tif".format(year))
    Id_list = []
    DOY_list = []
    Mean_list = []
    Max_list = []


    out_file = open((ws + "/Test_Field_{}.csv".format(year)),'w')

    Header = 'FIELD_ID,DOY,AVG_NDVI,MAX' +'\n'
    out_file.write(Header)

    for i in image_list:
        doy = i[-16:-13]
        arcpy.gp.ZonalStatisticsAsTable_sa("test_field", "Id", i, "E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/test_field/{}_{}.dbf".format(year,doy), "DATA", "ALL")

        # Create our search cursor
        table_loc = ws + "/{}_{}.dbf".format(year,doy)
        SC = arcpy.da.SearchCursor(table_loc,['Id','MEAN','MAX'])
        result = arcpy.GetCount_management(table_loc)
        count = int(result.getOutput(0))

        if (count == 1):
            row = next(SC)
            Id_list.append(row[0])
            DOY_list.append(doy)
            Mean_list.append(row[1])
            Max_list.append(row[2])
        else:
            Id_list.append("")
            DOY_list.append(doy)
            Mean_list.append("")
            Max_list.append("")

        del SC

    for i in range(0,len(Mean_list)):
        out_string = str(Id_list[i])+','+DOY_list[i]+','+str(Mean_list[i])+','+str(Max_list[i])+'\n'
        out_file.write(out_string)

    out_file.close()

print("\n ~~~FINI~~~ \n")
