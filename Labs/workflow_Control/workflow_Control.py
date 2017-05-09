# PGEO6050 [SPRING2017]
# Python Programming - Lab3
# 2/3/2017
# Wes Porter

 # WORKFLOW CONTROL STATEMENTS

# Python path: C:\Python27\ArcGIS10.3\python.exe Wes_Lab3.py

import math
import numpy as np
import random as rd

print ("\n~ WORKING WITH PYTHON FOR STATEMENT ~ \n")

# Defining our column names
header = ['integer', 'square', 'square root', 'exponential']

# Creating a list of numbers from which to generate our table
numbers = [2,4,6,8,10]

# Specifying our table spacing.
tab = "    "

# Initializing the offset
offset = ' '

# Printing the table header
print(header[0] + tab + header[1] + tab + header[2] + tab + header[3] + tab +"\n")

# For loop used to generate the table
for i in numbers:
    colm1 = str(i)
    colm1 = colm1 + offset*(len(header[0]) - len(str(colm1)))

    colm2 = str(i**2)
    colm2 = colm2 + offset*(len(header[1]) - len(str(colm2)))

    colm3 = str(math.ceil(math.sqrt(i)*100)/100)
    colm3 = colm3 + offset*(len(header[2]) - len(str(colm3)))

    colm4 = str(math.ceil(math.exp(i)*100)/100)
    colm4 = colm4 + offset*(len(header[3]) - len(str(colm4)))

    print (colm1 + tab + colm2 + tab + colm3 + tab + colm4 +"\n")




print ("\n~ WORKING WITH WORKFLOW CONTROL STATEMENT ~ \n")


# Create random 3 dimensional point cloud

pts_x = []
pts_y = []
pts_z = []
pts_n = 1000
delta = 200
for i in range (pts_n):
    x = 1000.00 * rd.random()
    y = 1000.00 * rd.random()
    z = 1000.00 * rd.random()
    pts_x.append (float(x))
    pts_y.append (float(y))
    pts_z.append (float(z))

# Create nested list to iterate over with for loop
v = [pts_x,pts_y,pts_z]

#Initialize lists to hold calculation results
n = 3
averages = [0] * n
maximums = [0] * n
minimums = [0] * n
lastSubs = [0] * n

#Calculate standard deviation of points
sd = np.std(v)

# Initializing Avg for use in subsequent function
Avg = 0

# Create a function to evaluate which points should be subset
def subsetFunc(element):
    return element >= (Avg-sd) and element <= (Avg+sd)

# for loop to perform calculations for each point set
count = 0
for i in v:
    # Calc mean for each set of pts
    Avg = np.mean(i)
    averages[count] = Avg

    # Calc max for each set of pts
    Max = np.max(i)
    maximums[count] = Max

    # Calc min for each set of pts
    Min = np.min(i)
    minimums[count] = Min

    # Determine subset for each set of pts
    subset = filter(subsetFunc,i)
    lastSub = subset[-1]

    # Determine the last value in each subset
    lastSubs[count] = lastSub
    lenSub = [len(subset)]

    count = count+1

# Output string
os = ["mean X", "mean Y", "mean Z", "maximum X", "maximum Y", "maximum Z",
             "minimum X", "minimum Y", "minimum Z", "pts in subset",
             "last sub pts X", "last sub pts Y","last sub pts Z"]

# Output list of values
ol = averages + maximums + minimums + lenSub + lastSubs

# Initialize offset
offset = ' '

# for loop to print results
for i in range(0,13,1):
    print(os[i] + offset*(16 - len(os[i])) + ":  " + str(ol[i]))
