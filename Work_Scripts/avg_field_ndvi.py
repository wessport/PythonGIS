# WES PORTER
# 12-FEB-2018
# USDA PROJECT - avg_field_ndvi.py

# SCRIPT SUMMARY:
# Working with arcpy to avg NDVI values for a test field

import arcpy
import glob
import ntpath
import datetime
import dateutil.parser as dparser

# Disable: 'Add results of geoprocessing operations to the display'
arcpy.env.addOutputsToMap = 0

# Setting our workspace/environment
ws = "E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/tmp/test_field"
arcpy.env.workspace = ws

arcpy.env.overwriteOutput = True

ndvi_loc = "E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/SR_NDVI_msc_cloudFree"

arcpy.CheckOutExtension("spatial")

years = ["1985","1990","1995","2000"]
for year in years:
    image_list =  glob.glob(ndvi_loc+"/*_{}*_masked.tif".format(year))
    Id_list = []
    DOY_list = []
    Mean_list = []
    Max_list = []


    out_file = open((ws + "/Test_Field_{}.csv".format(year)),'w')

    Header = 'FIELD_ID,DOY,AVG_NDVI,MAX' +'\n'
    out_file.write(Header)

    test_field_loc = "E:/Wes/Work/USDA/raw/Mississippi/MS_Shapefiles/MS_Field_Boundaries/test_field.shp"

    for i in image_list:
        try:
            image_date = dparser.parse(ntpath.basename(i), fuzzy=True)
        except ValueError:
             sys.exit('ValueError encountered. Parse should only be called on a string containing one date')

        doy = image_date.timetuple().tm_yday
        arcpy.gp.ZonalStatisticsAsTable_sa(test_field_loc, "Id", i, "E:/Wes/Work/USDA/raw/Mississippi/MS_NDVI/tmp/test_field/{}_{}.dbf".format(year,doy), "DATA", "ALL")

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
        out_string = str(Id_list[i])+','+str(DOY_list[i])+','+str(Mean_list[i])+','+str(Max_list[i])+'\n'
        out_file.write(out_string)

    out_file.close()

arcpy.CheckInExtension("spatial")
arcpy.ResetEnvironments()

print("\n ~~~FINI~~~ \n")
