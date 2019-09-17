# XMGFileCreator.py
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# LAST EDITED: 22/11/18
# =============================================================================================== #
# Run the script as
#	python XMGFileCreator.py "FILE_DIR"
# where FILE_DIR is the directory containing the .dat file (and that is the only one of its kind)
#
# The CSV file name should have the format [ISOTOPE]-[REACTION]-[MODEL]-[PERIPHERAL STUFF].csv
#
# =============================================================================================== #
import numpy as np
import sys
import glob

def GetColumn( array, num ):
	return [ array[x][num] for x in range(0, len(array)) ]

# Create L string from L array
def CreateLString(L):
	L_string = "["

	# Test type
	if type(L) == list:
		# Loop over list elements
		for i in range(0,len(L)):
			if L[i] >= 0:
				L_string += str(L[i])
			
			if i != len(L) - 1 and L[i+1] >= 0:
				L_string += "_"
		L_string += "]"

	else:
		# L is an int
		L_string += str(L) + "]"
	return L_string

# CSV FILE HAS FORMAT e.g. 28Mg-(d,p)-MOREINFORMATION.csv
def GetDetailsFromCSV( CSV_file_name ):
	detail_list = CSV_file_name.split("-")
	isotope = detail_list[0]
	reaction = detail_list[1]
	return isotope, reaction

def CreateDATFileName( model, energy, L, L_column, ExorPT, CSV_file_name ):
	# Get details from CSV file name
	if model == "":
		model = "NA"
	isotope, reaction = GetDetailsFromCSV( CSV_file_name )
	file_name = isotope + "-" + reaction + "-" + ExorPT + "-["  + model + "]-" + str(energy) + "-" + CreateLString( GetColumn(L, L_column ) ) + ".dat"
	return file_name


##### GRAB THE FILE
baseDir = sys.argv[1]
fullDir = glob.glob(baseDir + "*.csv")[0]
fileName = fullDir.split("/")[-1]

##### EXPERIMENTAL DATA
inFile = open(fullDir)
data = []

# Store the data
for line in inFile:
	data.append( line.split(",") )

# Close the file
inFile.close()

ExCounter = 0	# Counts the number of experimental data points = numAngles * 3 (Angle, CS, E(CS))
PTCounter = -1	# Counts the number of ptolemy data points (minus one for the blank line above it)
dash_line_counter = 0 # Counts the number of dashed lines to calculate the number of L's
dash_line_location = []	# Stores the row of the dashed lines
ExFlag = 0		# Flag to determine end of experimental states
PTFlag = 0		# Flag to determine when the first (and possibly only) Ptolemy block ends

# Deduce things about the data
for i in range(0, len(data)):
	# Get rid of the "\n" characters from the final entry
	data[i][-1] = data[i][-1].rstrip("\n")
	
	# Get number of states (2 initial columns)
	if i == 0:
		numStates = len(data[i]) - 2
	
	# Get number of experimental angles - 3 lines for model, L and E, and then a blank line. Then Ex stuff starts
	spaceCounter = 0
	if i > 3 and ExFlag == 0:
		ExCounter += 1
		
		for j in range(0, len(data[i])):
			if data[i][j] == "":
				spaceCounter += 1
		if spaceCounter == numStates + 2:
			ExFlag = 1
			ExCounter -= 1
			spaceCounter = 0
	
	# Get number of Ptolemy angles after blank line in between Ex and PT stuff
	if ExFlag == 1 and spaceCounter == 0 and PTFlag == 0:
		if data[i][0] != "---":
			PTCounter += 1
		else:
			PTFlag = 1

	# Count the number of lines with three dashes in each cell
	if i > 3 and data[i][0] == "---":
		dash_line_counter += 1
		dash_line_location.append(i)

# Define calculated quantities
numExAngles = int(ExCounter/3.0)
numPTAngles = PTCounter
numL = dash_line_counter + 1

# Now define arrays
model = [ "" for i in range(0, numStates) ]
exAngle = np.ones([numExAngles, numStates])*-1
exCS = np.ones([numExAngles, numStates])*-1
exECS = np.ones([numExAngles, numStates])*-1
ptCS = np.ones([numL, numPTAngles, numStates])*-1
ptAngle = np.ones(numPTAngles)*-1
energy = np.ones(numStates)*-1
L = [ [-1 for x in range(0,numStates) ] for y in range(0, dash_line_counter + 1 ) ]
num_dashed_lines = 0	# Counter for how many dashed lines reached

# Store the data
for i in range(0, len(data)):
	for j in range(0, len(data[i])):
		# Calculate if a dashed line has been reached
		if data[i][0] == "---" and j == 0:
			num_dashed_lines += 1

		# Store model (row 0)
		if i == 0 and j > 1:
			if data[i][j] != "NA" and data[i][j] != "":
				model[j-2] = data[i][j]

		# Store L's in row 1
		if i == 1 and j > 1:
			if data[i][j] != "" and data[i][j] != "U":
				if "%" in data[i][j]:
					L[0][j-2] = data[i][j]
				else:
					L[0][j-2] = int(data[i][j])
			else:
				L[0][j-2] = -1

		# Store remaining L's
		if i - 1 in dash_line_location and j > 1:
			if data[i][j] != "":
				L[ dash_line_location.index(i-1) + 1 ][j-2] = int(data[i][j])

		# Store energy (row 2)
		if i == 2 and j > 1 and data[i][j] != "":
			energy[j-2] = float(data[i][j])

		# Store exAngle (row 4 -> 3+numExAngles)
		if i > 3 and i < 3 + numExAngles + 1 and j > 1:
			if data[i][j] != "":
				exAngle[i-4][j-2] = float(data[i][j])

		# Store CS (row 3+numExAngles+1 -> 3+2*numExAngles)
		if i > 3 + numExAngles and i < 3 + 2*numExAngles + 1  and j > 1:
			if data[i][j] != "":
				exCS[i-3-numExAngles-1][j-2] = float(data[i][j])

		# Store ECS (row 3+2*numExAngles+1 -> 3+3*numExAngles)
		if i > 3 + 2*numExAngles and i < 3 + 3*numExAngles + 1 and j > 1:
			if data[i][j] != "":
				exECS[i-3-2*numExAngles-1][j-2] = float(data[i][j])

		# Store PTCS (row 3+3*numExAngles+2 -> end)
		if i > 3 + 3*numExAngles + 1 and j > 1:
			if data[i][j] == "U":
				ptCS[num_dashed_lines][i-3-3*numExAngles-2-num_dashed_lines][j-2] = -100
			elif data[i][j] != "" and data[i][j] != "---" and data[i][0] != "L":
				ptCS[num_dashed_lines][i-3-3*numExAngles-2-(numPTAngles+2)*num_dashed_lines][j-2] = float(data[i][j])

		# Store PT Angles
		if i > 3 + 3*numExAngles + 1 and j == 1 and num_dashed_lines == 0:
			if data[i][j] != "":
				ptAngle[i-3-3*numExAngles-2] = float(data[i][j])

# Write the data to file
for i in range(0, numStates):
	if energy[i] != -1:
		outFileEx = open(baseDir + CreateDATFileName( model[i], energy[i], L, i, "Ex", fileName ), "w")
		for j in range(0, numExAngles):
			if (exCS[j][i] != -1 and exAngle[j][i] != -1):
				outFileEx.write(str(exAngle[j][i]) + "\t" + str(exCS[j][i]) + "\t" + str(exECS[j][i]) + "\n")
		outFileEx.close()

		
		outFilePT = open(baseDir + CreateDATFileName( model[i], energy[i], L, i, "PT", fileName ), "w")
		for k in range(0, numL):	
			for j in range(0, numPTAngles):
				if (ptCS[k][j][i] != -1 and ptAngle[j] != -1):
					outFilePT.write(str(ptAngle[j]) + "\t" + str(ptCS[k][j][i]) + "\n")
			outFilePT.write("\n")
		outFilePT.close()






































