# XMGFullPage
# Plots the experimental data and theoretical fit for a given peak, in a
# m x n grid to fit on A4 paper (max 15 per sheet)
# Input files contain information for each state - PT file contains PT
# states in order, and the same for EX files
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
import sys
import numpy as np
# ~~~~~~~~~~~~~~~~~~~~~~~~~~ # XMGrace NOTES # ~~~~~~~~~~~~~~~~~~~~~~~~~ #
#### COLOURS
#	00	White		04	Blue		08	Violet		12	Indigo
# 	01	Black		05	Yellow		09	Cyan		13	Maroon
#	02	Red			06	Brown		10	Magenta		14	Turquoise
#	03	Green		07	Grey		11	Orange		15	Green4
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# MATCHES TO DIFFERENT L's UP TO 6, 7 is 2-3, 8 is 2-5, and 9 is unassigned
#                 [ 0,  1, 2, 3,  4, 5, 6,2-3,2-5, U ]
allowed_colours = [ 1, 11, 2, 6, 15, 4, 8, 13, 10, 0 ]
printNumOnGraph = 1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Define a function that makes lists of a given length
def makeList(n):
	list = []
	for i in range(0,n):
		list.append([])
	return list

# Find the position of dashes in a string WITH BRACKETS
def FindDashPositions( string ):
	positions = []
	for i in range( 0, len(string) ):
		if string[i] == "-" and ( string[i-1] == "]" or string[i+1] == "[" ):
			positions.append(i)

	return positions

def FindBracketPositions( string ):
	positions = []
	for i in range( 0, len(string) ):
		if string[i] == "[" or string[i] == "]":
			positions.append(i)

	return positions

def ConvertL( string ):
	# String of form [A_B_C_D_E] -> put elements into list
	temp_string = string.lstrip("[").rstrip("]")
	temp_list = temp_string.split("_")
	for i in range( 0, len(temp_list) ):
		if "%" in temp_list[i]:
			if temp_list[i] == "2%3":
				temp_list[i] = 7
			elif temp_list[i] == "2%5":
				temp_list[i] = 8
			else:
				temp_list[i] = 0
		if temp_list[i] == "":
				temp_list[i] = 9
		temp_list[i] = int(temp_list[i])
	return temp_list

def ReturnMaxIndex( MAX, i ):
	if MAX == "ex":
		return 2*i
	elif MAX == "pt":
		return 2*i + 1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Define the input files
inFileDir = sys.argv[1]
outFileDir = sys.argv[2]
baseFileDir = sys.argv[3]
energy = inFileDir[len(inFileDir)-10:len(inFileDir)-4]
w = int(sys.argv[4])
v = int(sys.argv[5])
MAX = sys.argv[6]
logy = int(sys.argv[7])

# Isolate which number it is
tempString = outFileDir.split("/")[-1]
fileNum = ""
for i in range(0,len(tempString)):
	if tempString[i].isdigit():
		fileNum += tempString[i]
numFile = int(fileNum)

# Open the list of fileNames
inFile = open(inFileDir,"r")

# Count the number of lines
count = 0
fileDirs = []
for line in inFile:
	count += 0.5
	fileDirs.append(line.rstrip("\n"))
inFile.close()

# Ensure count is integer
count = int(count)

# Extract energies and L
energy, model_name, L = [],[], []

for i in range(0,count):
	twoStateFlag = 0
	
	# Define a temporary string that is just the experimental file
	tempString = fileDirs[2*i]
	
	# Find the dashes and brackets
	bracket_positions = FindBracketPositions( tempString )
	dash_positions = FindDashPositions( tempString )

	# Find the model name
	model_name.append( tempString[bracket_positions[0]+1:bracket_positions[1]] )

	# Find the energy
	energy.append( float(tempString[dash_positions[1]+1:dash_positions[2]]))
	
	# Find the angular momenta
	L_string = tempString[bracket_positions[2]+1:bracket_positions[3]]
	L.append( ConvertL( L_string ) )


# Count now gives the number of blocks of data for Ptolemy, the same as the experimental file.
# Define graph-filling order
if type(w) != int:
	w = 4 										# Number of graphs across page horizontally
if type(v) != int or v == -1:
	v = int(np.ceil(float(count)/float(w)))		# Number of graphs across page vertically

# Find the maximum value for every file
max_value = []
min_value = []
angle_min = 5
angle_max = 10

# Find the maximum and minimum value from experimental file
for i in range(0,int(len(fileDirs)/2)):
	# Open the correct file
	find_ex_max_file = open(fileDirs[ReturnMaxIndex( "ex", i ) ])

	# Define the current maximum
	current_max = 0
	current_min = 10

	# Find a bigger maximum
	for line in find_ex_max_file:
		temp_list = line.rstrip("\n").split("\t")

		if len( temp_list ) > 1:
			temp_num = float(temp_list[1])
			if len( temp_list ) > 2:
				temp_num_max = temp_num + float(temp_list[2])
				temp_num_min = temp_num - float(temp_list[2])
			
			try:
				if temp_num_max > current_max:
					current_max = temp_num_max
			except:
				pass

			try:
				if temp_num_min < current_min:
					current_min = temp_num_min
			except:
				pass

	find_ex_max_file.close()

	
	# Open the Ptolemy file
	find_pt_max_file = open(fileDirs[ReturnMaxIndex( "pt", i ) ])

	# Find the minimum and maximum angle
	for line in find_pt_max_file:
		temp_list = line.rstrip("\n").split("\t")
		
		try:
			if float(temp_list[0]) < angle_min:
				angle_min = float(temp_list[0])
			if float(temp_list[0]) > angle_max:
				angle_max = float(temp_list[0])
		except:
			pass
		
		if MAX == "pt":
			# Find a bigger maximum if in options
			if len( temp_list ) > 1:
				temp_num = float(temp_list[1])
				if len( temp_list ) > 2:
					temp_num += float(temp_list[2])
				
				try:
					if temp_num > current_max:
						current_max = temp_num
				except:
					pass

				try:
					if temp_num < current_min:
						current_min = temp_num
				except:
					pass

	# Close the Ptolemy file
	find_pt_max_file.close()

	# Now append the maximum value
	max_value.append(current_max)
	min_value.append(current_min)

# FORCE SETTINGS
angle_max =  50

##### MAKE THE BATCH FILE
# First prepare parameters to go into file
# Page size
R = 1					# Desired ratio of height/width
W = 200*w				# Fix the width of the page
H = round(R*W*(float(v)/float(w)))	# Calculate the height of the page

# Offset (effective margin if width is 1) -> margin for the whole page
offset = 0.1

# SIZES OF STUFF
fontArray = [3,1.5,0.8,0.62,0.6,0.4,0.35,0.3]
try:
	fontSize = str(fontArray[max(v,w)-1-abs(v-w)])
except:
	fontSize = str(0.1)
symbolSize = str(0.25)
lineWidth = str(2.0)

# Now write the batch file
# Open the file
outFile = open(outFileDir,"w")

# GLOBAL PARAMETERS
# Page size
outFile.write("PAGE SIZE " + str(W) + ", " + str(H) + "\n")
# Arrange the boxes
#outFile.write("ARRANGE(" + str(v) + "," + str(w) + "," + str(offset) + ",0.4,0.4,OFF,OFF,OFF"  + ")\n")
outFile.write("ARRANGE(" + str(v) + "," + str(w) + "," + str(offset) + ",0.35,0.35,OFF,OFF,OFF"  + ")\n")

# Now loop over graphs and write output
for i in range(0,count):
	# Focus on graph
	outFile.write("FOCUS G" + str(i) + "\n")
	if logy == 1:
		outFile.write("G" + str(i) + " TYPE LOGY\n")
	
	# Find out number of LStates
	try:
		len(L[i])
		numLStates = 2
	except:
		numLStates = 1
	
	# EXPERIMENTAL
	outFile.write("READ XYDY \"" + fileDirs[2*i] + "\"\n")
	outFile.write('''S0 LINESTYLE 0
S0 ERRORBAR LINEWIDTH 1.0
S0 ERRORBAR LENGTH 0.25
S0 SYMBOL 1
S0 SYMBOL FILL 1
''')
	outFile.write("S0 SYMBOL SIZE " + symbolSize + "\n")
	
	# PTOLEMY - will differ depending if there are two L states
	outFile.write("READ XY \"" + fileDirs[2*i+1] + "\"\n")
	for j in range(0, len(L[i])):
		outFile.write("S" + str(j+1) + " LINE COLOR " + str( allowed_colours[ L[i][j] ] ) + "\n")
		outFile.write("S" + str(j+1) + " LINEWIDTH " + lineWidth + "\n")

	# GLOBAL
	# Calculate the world coordinates
	height_of_box = 1.3*float( max_value[i] )

	# x-axis ticks
	outFile.write('''XAXIS TICK MAJOR 10
XAXIS TICK MAJOR SIZE 0.4
XAXIS TICK MINOR 5
XAXIS TICK MINOR SIZE 0.2
XAXIS TICKLABEL FONT 4
''')
	outFile.write("XAXIS TICKLABEL CHAR SIZE " + fontSize + "\n")

	# y-axis ticks
	outFile.write("YAXIS TICKLABEL FONT 4\n")
	outFile.write("YAXIS TICKLABEL CHAR SIZE " + fontSize + "\n")

	# Calcuate where y-axis ticks should go based on the maximum value
	outFile.write("YAXIS TICK MAJOR SIZE 0.4\n")
	outFile.write("YAXIS TICK MINOR SIZE 0.2\n")

	# CALCULATE TICK SPACING FOR LIN/LOG SCALE ON Y AXIS AND MAXIMUM Y
	if logy == 1:
		outFile.write("YAXIS TICK MAJOR 10\n")
		outFile.write("YAXIS TICK MINOR TICKS 9\n")
		
		# Calculate the maximum and minimum y's based on max and min values
		y_max = 1.3*float( max_value[i] )
		y_min = float( min_value[i] )/1.3
		
		y_max_log = ( np.ceil( y_max/( 10**np.floor( np.log10(y_max) ) ) ) + 0.5 )*10**np.floor( np.log10(y_max) )
		
		if ( 10**( np.mod( np.log10( y_min ), 1 ) ) ) <= 5.0:
			y_min_log = 10**( np.floor( np.log10( y_min ) ) )
		else:
			y_min_log = 10**( np.floor( np.log10( y_min ) ) + np.log10(5) )

	else:
		# Calculate order of magnitude
		exponent = np.floor( np.log10( height_of_box ) )

		# Calculate the normalised size between zero and 1
		rem_1 = np.round( height_of_box/( 10**exponent ) )

		y_major_tick = 10
		if rem_1 == 1:
			y_major_tick = 0.2
		elif rem_1 == 2:
			y_major_tick = 0.4
		elif rem_1 == 3:
			y_major_tick = 0.5
		elif rem_1 == 4:
			y_major_tick = 0.5
		elif rem_1 == 5:
			y_major_tick = 1
		elif rem_1 == 6:
			y_major_tick = 1
		elif rem_1 == 7:
			y_major_tick = 1
		elif rem_1 == 8:
			y_major_tick = 2
		elif rem_1 == 9:
			y_major_tick = 2

		
		outFile.write("# y_major_tick = " + str(y_major_tick) + ", exponent = " + str(exponent) + "\n" )
		outFile.write("YAXIS TICK MAJOR " + str(y_major_tick*(10**exponent)) + "\n")
		outFile.write("YAXIS TICK MINOR " + str(y_major_tick*(10**exponent)/2) + "\n#")

	# BASE FOR ENERGY STRING
	outFile.write("READ XY \"" + baseFileDir + "\"\n")
	outFile.write("S" + str(len(L[i]) + 1) + " LINESTYLE 0\n")
	outFile.write('''WITH STRING
STRING ON
STRING LOCTYPE WORLD
STRING COLOR 1
STRING ROT 0
STRING FONT 4
STRING JUST 9
''')
	outFile.write("STRING CHAR SIZE " + fontSize + "\n")
	outFile.write("STRING G" + str(i) + "\n")
	if logy == 1:
		outFile.write("STRING " + str(angle_max - 5) + ", " + str(10**( 0.923*np.log10( y_max_log ) ) ) + "\n")
	else:
		outFile.write("STRING " + str(angle_max - 5) + ", " + str( 0.923*height_of_box ) + "\n")
		
		
	if printNumOnGraph == 1:
		outFile.write("STRING DEF \"" + "(" + str(w*v*(numFile-1) + i + 1) + ") " + str(energy[i]) + "\"\n")
	else:
		outFile.write("STRING DEF \"" + str(energy[i]) + "\"\n")

	# MODEL NAME STRING
	if model_name[i] != "NA":
		outFile.write('''WITH STRING
		STRING ON
		STRING LOCTYPE WORLD
		STRING COLOR 1
		STRING ROT 0
		STRING FONT 4
		STRING JUST 6
		''')
		outFile.write("STRING CHAR SIZE 0.450\n")
		outFile.write("STRING G" + str(i) + "\n")
		if logy == 1:
			outFile.write("STRING " + str( 0.5*( angle_min + angle_max ) ) + ", " + str(10**( 1.05*np.log10( y_max_log ) ) ) + "\n")
		else:
			outFile.write("STRING " + str( 0.5*( angle_min + angle_max ) ) + ", " + str(1.05*height_of_box) + "\n")
		outFile.write("STRING DEF \"" + model_name[i] + "\"\n" )

	

	# DEFINE WORLD COORDINATES
	if logy == 1:
		# LOGY SCALE
		outFile.write("WORLD " + str(angle_min) + ", " + str(y_min_log) + ", " + str(angle_max) + ", " + str(y_max_log) + "\n")

	else:
		# LINEAR SCALE
		outFile.write("WORLD " + str(angle_min) + ", 0, " + str(angle_max) + ", " + str(height_of_box) + "\n")

	# Calculate if there are any states to kill
	if (w*v) - count > 0:
		num2Kill = (w*v) - count
		for i in range(0,num2Kill):
			outFile.write("KILL G" + str(count+i) + "\n")
	
# Add axis labels along side and bottom
largeFontSize = str(1.5*float(fontSize))
outFile.write("STRING CHAR SIZE " + largeFontSize + "\n")
outFile.write('''WITH STRING
STRING ON
STRING LOCTYPE VIEW
STRING COLOR 1
STRING ROT 0
STRING FONT 4
STRING JUST 6
STRING DEF "Angle (degrees)"
	''')
if w > v:
	outFile.write("STRING " + str(max(float(v)/float(w),float(w)/float(v))/2.0) + ", 0.025\n")
else:
	outFile.write("STRING 0.5, 0.025\n")

outFile.write('''WITH STRING
STRING ON
STRING LOCTYPE VIEW
STRING COLOR 1
STRING ROT 90
STRING FONT 4
STRING JUST 12
STRING DEF "d\\xs\\f{}/d\\xW\\f{} (mb/sr)"
	''')
outFile.write("STRING CHAR SIZE " + largeFontSize + "\n")
if v > w:
	outFile.write("STRING 0.01, " + str(max(float(v)/float(w),float(w)/float(v))/2.0) + "\n")
else:
	outFile.write("STRING 0.01, 0.5\n")
# Printer settings
# Change the ending to a .ps rather than a .txt
printDir = inFileDir.split("/")
printDir = "/".join(printDir[0:len(printDir)-1]) + "/full_page" + fileNum

outFile.write("PRINT TO \"" + printDir + ".ps\"\n")
outFile.write("PRINT \n")
outFile.write("SAVEALL \"" + printDir + ".agr\"\n")

outFile.close()

