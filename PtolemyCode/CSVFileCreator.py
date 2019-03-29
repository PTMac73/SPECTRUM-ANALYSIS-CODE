# CSVFileCreator
# Creates a full CSV file of all the Ptolemy output states
##########################################################################
# First argument is the list of files with all the Ptolemy out-clean files
# in it.
# Second argument is the CSV file name
##########################################################################
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# LAST EDITED: 09/02/18
# ########################################################################
import sys

# ~~~~~~~~~~~~~~~~~~~ STORE ALL THE PTCLEANED FILES ~~~~~~~~~~~~~~~~~~~~ #
# Open the list of files
inFileDir = sys.argv[1]
inFile = open(inFileDir,"r")

# Declare a list to store them
cleanArray = []

# Store the directories
for line in inFile:
	cleanArray.append(line.rstrip("\n"))
	
# Close the file
inFile.close()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ EXTRACT THE DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
###### Calculate the number of L-values
# Open the first file
firstFile = open(cleanArray[0])
firstData = []

# Store the contents
for i in firstFile:
	firstData.append(i.rstrip("\n"))

# Close the file
firstFile.close()

# Number of L-values = Number of "" in the data
numL = 0 	# There is a space after every block
blockSize = 0
for i in range(0,len(firstData)):
	if firstData[i] == "":
		# If it's the end of the first block, store how many lines it took to get there
		if numL == 0:
			blockSize = i
		numL += 1

###### Grab the angles
angle = []
for i in range(0,blockSize):
	angle.append(float(firstData[i].split()[0]))

##### Grab the theoretical cross-sections
# Declare containers
energy = [ 0.0 for i in range( len(cleanArray) ) ]

# First index specifies L
# Second index specifies energy
# Third angle specifies angle
CS = [ [ [ 0.0 for i in range(len(angle)) ] for j in range(len(energy)) ] for k in range(numL) ]

# Loop over the number of clean files (effectively energy)
for i in range(0,len(cleanArray)):
	# Grab the energy from the file name - first split at the rightmost "/"
	tempString = cleanArray[i]
	tempString = tempString[tempString.rfind("/")+1:len(tempString)]
	
	# Now find the part between the leftmost "-" and rightmost "."
	tempString = tempString[tempString.find("-")+1:tempString.rfind(".")]
	energy[i] = float(tempString)
	
	# Open the file
	inFile = open(cleanArray[i],"r")
	
	# Now define counters to reset etc.
	LCounter = 0
	angleCounter = 0
	# Loop over lines (angle and L)
	for line in inFile:
		# Check if it is a new L starting by empty line
		if line.split() == []:
			LCounter += 1
			angleCounter = 0
		else:
			#print(str(line.split()[0]) + "\t" + str(angleCounter) + "\t" + str(LCounter))
			CS[LCounter][i][angleCounter] = float(line.split()[1])
			angleCounter += 1
	
	# Close the file
	inFile.close()
	
# ~~~~~~~~~~~~~~~~~~~~~~~~ CREATE CSV FILE LINES ~~~~~~~~~~~~~~~~~~~~~~~ #
# Create the lines
CSVFileLines = ["" for i in range(numL*(len(angle)+1)+2)]
# Loop over L [large row]
for i in range(0,numL):
	# Loop over angles + 2 (for line of energies as the top row and for blank line beneath) [one row]
	for j in range(0,len(angle)+2):
		# Loop over energy + 2 (for line of angles in second column and for L in first column) [one column]
		for k in range(len(energy)+2):
			# Append energies
			if i == 0 and j == 0 and k > 1:
				CSVFileLines[i*(len(angle) + 1) + j + 1] = CSVFileLines[i*(len(angle) + 1) + j + 1] + str(energy[k-2]) + ","
				#pass
			# Append angles
			elif k == 1 and j > 0 and j < len(angle)+1:
				CSVFileLines[i*(len(angle) + 1) + j + 1] = CSVFileLines[i*(len(angle) + 1) + j + 1] + str(angle[j-1]) + ","
				#pass
			# Append angular momenta
			elif k == 0 and j == 1:
				CSVFileLines[i*(len(angle) + 1) + j + 1] = CSVFileLines[i*(len(angle) + 1) + j + 1] + str(i) + ","
				#pass
			# Append actual data
			elif j > 0 and j < len(angle)+1 and k > 1:
				CSVFileLines[i*(len(angle) + 1) + j + 1] = CSVFileLines[i*(len(angle) + 1) + j + 1] + str( CS[i][k-2][j-1] ) + ","
				#pass
			# Fill the rest with blanks
			else:
				CSVFileLines[i*(len(angle) + 1) + j + 1] = CSVFileLines[i*(len(angle) + 1) + j + 1] + ","
				#pass
				
# ~~~~~~~~~~~~~~~~~~~~ STORE THE DATA IN A CSV FILE ~~~~~~~~~~~~~~~~~~~~ #
# Open the CSV File
outFileDir = sys.argv[2]
outFile = open(outFileDir,"w")

# Write lines to CSV file
for i in range(0,len(CSVFileLines)):
	outFile.write(CSVFileLines[i] + "\n")

# Close the file
outFile.close()

















