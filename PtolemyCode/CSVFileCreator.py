# CSVFileCreator
# Creates a full CSV file of all the Ptolemy output states
# =============================================================================================== #
# First argument is the list of files with all the Ptolemy out-clean files
# in it.
# Second argument is the CSV file name
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
import sys

# Function to find the position of the dashes in a string
def FindDashes( string ):
	dash_index = []
	for i in range( 0, len(string) ):
		if string[i] == "-":
			dash_index.append(i)
	return dash_index

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ STORE ALL THE PTCLEANED FILES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Open the list of files
in_file_dir = sys.argv[1]
in_file = open(in_file_dir,"r")

# Declare a list to store them
clean_array = []

# Store the directories
for line in in_file:
	clean_array.append(line.rstrip("\n"))
	
# Close the file
in_file.close()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EXTRACT THE DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
###### Calculate the number of L-values
# Open the first file
first_file = open(clean_array[0])
first_data = []

# Store the contents
for i in first_file:
	first_data.append(i.rstrip("\n"))

# Close the file
first_file.close()

# Number of L-values = Number of "" in the data
numL = 0 	# There is a space after every block
block_size = 0
for i in range(0,len(first_data)):
	if first_data[i] == "":
		# If it's the end of the first block, store how many lines it took to get there
		if numL == 0:
			block_size = i
		numL += 1

###### Grab the angles
angle = []
for i in range(0,block_size):
	angle.append(float(first_data[i].split()[0]))

##### Grab the theoretical cross-sections
# Declare containers
energy = [ 0.0 for i in range( len(clean_array) ) ]
model_name = [ "" for i in range( len(clean_array) ) ]

# First index specifies L
# Second index specifies energy
# Third angle specifies angle
CS = [ [ [ 0.0 for i in range(len(angle)) ] for j in range(len(energy)) ] for k in range(numL) ]

# Loop over the number of clean files (effectively energy)
for i in range(0,len(clean_array)):
	# File name format: [DIR]/[REACTION]-[IN POTENTIAL]_[OUT POTENTIAL]-[ENERGY].out-clean
	# Grab the energy from the file name - first split at the rightmost "/"
	tempString = clean_array[i]
	tempString = tempString[tempString.rfind("/")+1:len(tempString)]
	
	# Now extract the model name and energies (between the first and second "-" characters)
	dash_index = FindDashes( tempString )
	model_name[i] = tempString[ dash_index[0] + 1:dash_index[1] ]
	
	# Now find the part between the leftmost "-" and rightmost "."
	energy[i] = float( tempString[ dash_index[1] + 1:tempString.rfind(".")] )
	
	# Open the file
	in_file = open(clean_array[i],"r")
	
	# Now define counters to reset etc.
	L_counter = 0
	angle_counter = 0

	# Loop over lines (angle and L)
	for line in in_file:
		# Check if it is a new L starting by empty line
		if line.split() == []:
			L_counter += 1
			angle_counter = 0
		else:
			#print(str(line.split()[0]) + "\t" + str(angle_counter) + "\t" + str(L_counter))
			CS[L_counter][i][angle_counter] = float(line.split()[1])
			angle_counter += 1
	
	# Close the file
	in_file.close()


# ~~~~~~~~~~~~~~~~~~~~~~~~ CREATE CSV FILE LINES ~~~~~~~~~~~~~~~~~~~~~~~ #
# Create the lines
# Need [number of angular momenta]*[number of angles + blank line underneath] + 2 header lines
CSVFileLines = ["" for i in range(numL*(len(angle)+1)+2)]

# Append the first two rows (model name and energies)
CSVFileLines[0] += ",,"
CSVFileLines[1] += ",,"
for i in range(0, len(model_name) ):
	if i == 0:
		CSVFileLines[0] += model_name[i] 
	
	elif model_name[i-1] != model_name[i]:
		CSVFileLines[0] += model_name[i] 
	
	CSVFileLines[1] += str(energy[i])
	CSVFileLines[0] += ","
	CSVFileLines[1] += ","


# Now insert the cross sections
# Loop over L [large row]
for i in range(0,numL):
	# Loop over angles + 1 (for blank line beneath) [one row]
	for j in range(0,len(angle)+1):
		# Loop over energy + 2 (for line of angles in second column and for L in first column) [one column]
		for k in range(len(energy)+2):
			# Append angles
			if k == 1 and j < len(angle):
				CSVFileLines[i*(len(angle) + 1) + j + 2] += str(angle[j]) + ","

			# Append angular momenta
			elif k == 0 and j == 0:
				CSVFileLines[i*(len(angle) + 1) + j + 2] += str(i) + ","

			# Append actual data
			elif j < len(angle) and k > 1:
				CSVFileLines[i*(len(angle) + 1) + j + 2] += str( CS[i][k-2][j] ) + ","

			# Fill the rest with blanks
			else:
				CSVFileLines[i*(len(angle) + 1) + j + 2] += ","



		
# ~~~~~~~~~~~~~~~~~~~~ STORE THE DATA IN A CSV FILE ~~~~~~~~~~~~~~~~~~~~ #
# Open the CSV File
outFileDir = sys.argv[2]
outFile = open(outFileDir,"w")

# Write lines to CSV file
for i in range(0,len(CSVFileLines)):
	outFile.write(CSVFileLines[i] + "\n")

# Close the file
outFile.close()















