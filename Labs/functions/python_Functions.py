# PGEO6050 [SPRING2017]
# Python Programming - Lab3
# 2/3/2017
# Wes Porter

# COVERTING CODE INTO A FUNCTION

# C:\Python27\ArcGISx6410.3\python.exe scratch.py

def myFunction(eFile,nFile,offset):
    inFile = open(eFile, 'r')

    x_list=[]
    y_list=[]
    z_list=[]
    for line in inFile:
        strFromFile = line.strip() # Remove line breaks
        parsedList = strFromFile.split(' ') # Returns a list of strings
        x_list.append(float(parsedList[0]))
        y_list.append(float(parsedList[1]))
        z_list.append(float(parsedList[2]))

    inFile.close()

    z_new = []

    for i in z_list:
        z_new.append(i + offset)

    #Writing the new file
    outFile = open(nFile,'w')


    for i in range(1000):
        line =(str(x_list[i]) + ',' + str(y_list[i]) + ',' + str(z_new[i]) +'\n') # Don't need comma on the end. Line break works as a delimeter
        outFile.write(line)

    outFile.close()

eFile = 'raw_pts.xyz'
nFile = 'mod_pts.xyz'
offset = 2.00
