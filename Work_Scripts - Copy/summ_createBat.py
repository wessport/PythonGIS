# WES PORTER
# 6/21/2017
# USDA PROJECT - summ_createBat.py

# SCRIPT SUMMARY:
# Working with python to generate a summary bat file to use with Dr. Momm's script.

# C:\Python27\ArcGISx6410.3\python.exe summ_createBat.py

ws = "E:/Wes/Work/Rusle2/AnnAGNPS-RUSLE2_Runs/erosionSummary/"

in_file = open(ws + "files.txt", 'r')
files = []
for line in in_file:
    strFromFile = line.strip()  # Remove line breaks
    files.append(strFromFile)

# Create text file to send formatted string to
outFile = open(ws + "summ2.txt", 'w')

# Write header info
l1 = ":: WES PORTER\n"
l2 = ":: 6/21/2017\n"
l3 = ":: USDA PROJECT\n"
l4 = ":: Summary: Using timeSeries.py to summarize Rusle2 data.\n"
l5 = "echo off\n"
l6 = "title timeSeries\n"
header = l1 + l2 + l3 + l4 + l5 + l6
outFile.write(header)

for i in files:
    out_string = "python " + "timeSeries.py " +"2 " + i + " 1982 1994 " + i[:-4] + "_cont.csv" + "\n"
    outFile.write(out_string)

footer = "echo Execution complete.\nPause"
outFile.write(footer)
outFile.close()

in_file = open(ws + "files.txt", 'r')
files = []
for line in in_file:
    strFromFile = line.strip()  # Remove line breaks
    files.append(strFromFile)


# Create text file to send formatted string to
outFile = open(ws + "summ1.txt", 'w')

# Write header info
l1 = ":: WES PORTER\n"
l2 = ":: 6/21/2017\n"
l3 = ":: USDA PROJECT\n"
l4 = ":: Summary: Using timeSeries.py to summarize Rusle2 data.\n"
l5 = "echo off\n"
l6 = "title timeSeries\n"
header = l1 + l2 + l3 + l4 + l5 + l6
outFile.write(header)

for i in files:
    out_string = "python " + "timeSeries.py " +"1 " + i[:-4] + "_cont.csv " + i[:-4] + "\n"
    outFile.write(out_string)

footer = "echo Execution complete.\nPause"
outFile.write(footer)
outFile.close()

print("\n ~~~FINI~~~ \n")
