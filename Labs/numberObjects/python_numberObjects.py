# GEOG-650 [SPRING2017]
# Python Programming - Lab2
# 2/2/2017
# Wes Porter

# WORKING WITH PYTHON NUMBER OBJECTS

# Python path: C:\Python27\ArcGISx6410.3\python.exe Wes_Lab2.py


print "\n~ WORKING WITH PYTHON NUMBER OBJECTS ~ \n"

# Define Variables
v0 = 5.0
v1 = 10.0
g = 9.81
t1 = 0.6
t2 = 0.55

# Computation 1
Yt1 = (v0*t1) - ((1.0/2.0)*g*(t1)**2.0)

# Computation 2
Yt2 = (v0*t2) - ((1.0/2.0)*g*(t2)**2.0)

# Input / Output String

v0s = "v0 = " + str(v0) + "m/s \n"
v1s = "v1 = " + str(v1) + "m/s \n"
gs = "g = " + str(g) + "m/s^2 \n"
t1s = "t1 = " + str(t1) + "s \n"
t2s = "t2 = " + str(t2) + "s \n"

myVariables = "My Variables: \n" + v0s + v1s + gs + t1s + t2s
print myVariables

# Free fall formula
ffFormula = "Free fall formula: \n Yt = v0t - 1/2gt^2 \n"
print ffFormula

text1 = "The vertical position Yt at time t = 0.6s and v0 = 5 meters is : "
text2 = "The vertical position Yt at time t = 0.55s and v0 = 10 meters is : "


Yt = str(Yt1)
print(text1 + Yt + "\n")
Yt = str(Yt2)
print(text2 + Yt + "\n")



print "\n~ WORKING WITH PYTHON STRING OBJECTS ~ \n"

print "Question 1 \n"

UN = 'Middle Tennessee State University'
PT = 'C:\temp\new'
PT2 = r'C:\temp\new'

q1a = "The length of UN is : "
q1b = "The length of PT, considering escape characters is : "
q1c = "The length of PT, not considering escape characters is : "

L = len(UN)
L = str(L)
print(q1a + L +"\n")

L = len(PT)
L = str(L)
print(q1b + L +"\n")

L = len(PT2)
L = str(L)
print(q1c + L +"\n")


print "Question 2 \n"

p1 = UN[5]

p2 = UN[15]

p3 = UN[0]

p = p1 + " " + p2 + " " + p3

q2 = "The character values of UN[5], UN[15], UN[0] are : "

print  q2 + p + "\n"


print "Question 3 \n"

q3a = "The range is 7:16"
q3b = "Which returns: " + UN[7:16]

print q3a + "\n" + q3b + "\n"


print "Question 4 \n"

q4a = "UN[-1] returns the last character of UN which is: " + UN[-1]

print q4a + "\n"


print "Question 5 \n"

q5a = "You would change the characters in UN to upper by calling 'UN.upper()' : "

UNU = UN.upper()

print q5a + UNU + "\n"


print "Question 6 \n"

q6a = "The result when you type 'print PT' is: "

print q6a + PT + "\n"

q6b = "This occurs do to the escape characters present in the string.\n"

q6c = r"To prevent escape characters from interfering you would type: r'C:\temp\new'"

q6d = "\nOr you could replace the backslash with forward slashes: 'C:/temp/new' \n"

q6 = q6b + q6c + q6d

print q6



print "\n~ WORKING WITH PYTHON LIST OBJECTS ~ \n"

print "Question 1 \n"

myList = ['blue', 'yellow', 'green', 'white', 'black', 'magenta']

L = len(myList)

q1a = "The length of the list is: " + str(L) +"\n"

q1b = "You could code this as: L = len(myList) \n print(L) \n"

print(q1a + q1b)


print "Question 2 \n"

A = myList[0]
B = myList[3]

q2 = "The items in positions 0 and 3 are: " + A + " and " + B +"\n"

print q2


print "Question 3 \n"

q3a = "You would print the last item in the list by calling: myList[-1] \n"

q3b = "Which returns: " + myList[-1] + "\n"

print q3a + q3b


print "Question 4 \n"

myList.append('UT-orange')

q4a = "You would add a new color by calling: myList.append('UT-orange') \n"

q4b = "Which returns:" + str(myList) + "\n"

print q4a +q4b


print "Question 5 \n"

#Got fancy because I capitalized 'UT-orange' which throws off .sort()
myList = sorted(myList, key=str.lower)

q5a = "You could sort your list alphabetically by calling: myList = sorted(myList, key=str.lower) \n"

q5b = "Which returns:" + str(myList) + "\n"

print q5a +q5b



print "\n~ WORKING WITH PYTHON DICTIONARY OBJECTS ~ \n"

print "Question 1 \n"

dictionary1 = {'AL':'Alabama', 'TN': 'Tennessee','KY':'Kentucky','FL':'Florida', 'MS':'Mississippi'}

AL_cities = ['Birmingham', 'Tuscaloosa', 'Mobile']
TN_cities = ['Knoxville', 'Nashville', 'Memphis']
KY_cities = ['Lexignton', 'Louisville', 'Bowling Green']
FL_cities = ['Tampa', 'Miami', 'Gainsville']
MS_cities = ['Oxford', 'Natchez', 'Tupelo']

dictionary2 = {'AL':AL_cities, 'TN':TN_cities, 'KY':KY_cities, 'FL':FL_cities, 'MS':MS_cities}

p = dictionary1['AL']

q1a = "You could fetch a state value from the first dictionary by using its key: dictionary1['AL'] \n"

q1b = "Which if printed, the return would be: " + p + "\n"

print q1a + q1b


print "Question 2 \n"

p = dictionary2['TN']

q2a = "You could fetch a list of cities from the second dictionary by using its key as well, \n"

q2b = "assuming the corresponding value was a list object of those cities. \n"

q2c = "\nThat would look like this: dictionary2['TN'] \n"

q2d = "\nWhich if printed, the return would be: " + str(p) + "\n"

print q2a + q2b + q2c + q2d
