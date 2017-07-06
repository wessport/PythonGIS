# WES PORTER
# 5/31/2017
# USDA PROJECT - irrigation_Analysis

# SCRIPT SUMMARY:

import arcpy

# Define arcpy workspace
ws = "D:/Wes/Work/USDA/raw/Scripts/irrigation"
arcpy.env.workspace = ws

# Disable: 'Add results of geoprocessing operations to the display'
# Annoying otherwise
arcpy.env.addOutputsToMap = 0

for i in range(2002,2016):
    # Irrigation year
    y = i

    # Resample raster cells so that feature zone is larger than cell size
    in_raster= "/YMD_Irrigation{}_proj.tif".format(y)
    out_raster= ws + "/YMD_Irrigation{}_proj_rs.tif".format(y)
    arcpy.Resample_management(in_raster, out_raster, cell_size="10 10", resampling_type="NEAREST")

    # RASTER CALC
    # Assign value of '1' to cells that are irrigated
    outFile = ws + "/Irr_{}.tif".format(y)
    arcpy.gp.RasterCalculator_sa("""OutRas = Con(InList("YMD_Irrigation{}_proj_rs.tif",[1,2,3,5]), 1, -9999)""".format(y), outFile)

    # Assign NoData to '0'
    outFile = ws + "/Irr_{}_fix.tif".format(y)
    arcpy.gp.RasterCalculator_sa("""Con(IsNull("Irr_{}.tif"),0,"Irr_{}.tif")""".format(y,y), outFile)

    # ZONAL STATS
    featureZone = ws + "/ms_annagnps_cells_64_may17.shp"
    outTable = ws + "/ZonalST_{}".format(y)
    arcpy.gp.ZonalStatisticsAsTable_sa(featureZone, "GRIDCODE", outFile, outTable, "DATA", "ALL")

    # Delete intermediate intersect files to save storage
    arcpy.Delete_management(ws + "/Irr_{}.tif".format(y), data_type="")

    # Create search cursor
    SC = arcpy.da.SearchCursor(outTable,['GRIDCODE','COUNT','SUM'])

    # Write results to a csv
    out_file = open((ws + "/Irrigation{}.csv".format(y)),'w')

    Header = 'GRIDCODE,PERCENT_IRR_{},'.format(y) +'\n'
    out_file.write(Header)

    for row in SC:
        countTotal = row[1]
        countIrr = row[2]
        percent = (countIrr/countTotal)*100
        textOut = str(row[0]) + ',' + str(percent) + '\n'
        out_file.write(textOut)
    out_file.close()
    del SC

    # FINI
