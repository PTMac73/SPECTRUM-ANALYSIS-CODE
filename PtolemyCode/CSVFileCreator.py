# CSVFileCreator
# Creates a full CSV file of all the Ptolemy output states
# =============================================================================================== #
# First argument is the list of files with all the Ptolemy out-clean files
# in it.
# Second argument is the CSV file name
# File name is of the form [reaction]-[model]-[energy]-[jnumber]-[jpi].out-clean
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
import numpy as np
import sys

# Function to find the position of the dashes in a string
def FindDashes( string ):
	dash_index = []
	for i in range( 0, len(string) ):
		if string[i] == "-":
			dash_index.append(i)
	return dash_index
	
# Convert jpi string to something better
# Of the form [x]2[pn], where x is an odd number
def JPiString( string ):
	a = string.replace("2","/2")
	b = a.replace("p","+")
	c = b.replace("n","-")
	return c

# Of the form [x]2[pn], where x is an odd number
def JPi2L( jpi ):
	# split the string
	j,pi = jpi.split("2")
	
	# get the parity and calculate whether even or odd
	if pi == "p":
		mod = 0
	elif pi == "n":
		mod = 1
	else:
		print("ERROR. ASSUMING EVEN.")
		mod = 0
		
	# calculate the L value
	if int( 0.5*( int(j) + 1 ) ) % 2 == mod:
		return int( 0.5*( int(j) + 1 ) )
	elif int( 0.5*( int(j) - 1 ) ) % 2 == mod:
		return int( 0.5*( int(j) - 1 ) )
	else:
		print("ERROR. j = " + j + " not working")
		return -1

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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EXTRACT THE DATA FROM FILE NAMES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Extract numL
Jnumbers = []
jpi = []
numL = 0

for i in range(0, len(clean_array) ):
	temp_str = clean_array[i].split("/")[-1]
	split_file_name = temp_str.split("-")
	if ( Jnumbers == [] or int(Jnumbers[-1]) < int(split_file_name[3]) ):
		Jnumbers.append( split_file_name[3] )
		jpi.append( split_file_name[4].split(".")[0] )

numL = len(Jnumbers)

# Extract energies, models, and jpi's too
energy = []
model_name = []

temp_index = 0

for i in range(0, len(clean_array) ):
	temp_str = clean_array[i].split("/")[-1]
	split_file_name = temp_str.split("-")
	
	# Store things that change per state
	if ( split_file_name[3] == Jnumbers[0] ):
		model_name.append( split_file_name[1] )
		energy.append( float( split_file_name[2] ) )
		temp_index += 1


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EXTRACT THE DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Open the first file
first_file = open(clean_array[0])
first_data = []

# Store the contents
for i in first_file:
	first_data.append(i.rstrip("\n"))

# Close the file
first_file.close()

###### Grab the angles
angle = []
for i in range(0, len(first_data) ):
	try:
		angle.append( float( first_data[i].split()[0] ) )
	except:
		pass

##### Grab the theoretical cross-sections
# First index specifies jpi
# Second index specifies energy
# Third angle specifies angle
CS = [ [ [ 0.0 for i in range(len(angle)) ] for j in range(len(energy)) ] for k in range(numL) ]


# Loop over the number of clean files (effectively energy)
L_index = 0
energy_index = 0
for i in range(0,len(clean_array)):
	# File name format: [DIR]/[reaction]-[model]-[energy]-[jnumber]-[jpi].out-clean
	# Open the file
	in_file = open(clean_array[i],"r")
	energy_index = int(np.floor(i/len(Jnumbers)))
	L_index = i % len(Jnumbers)
	

	# Loop over lines (angle and L)
	angle_counter = 0
	for line in in_file:
		if len( line.split() ) > 1:
			CS[L_index][energy_index][angle_counter] = float(line.split()[1])
			angle_counter += 1
	
	# Close the file
	in_file.close()

#"""
# ~~~~~~~~~~~~~~~~~~~~~~~~ CREATE CSV FILE LINES ~~~~~~~~~~~~~~~~~~~~~~~ #
# Create the lines
# Need [number of angular momenta]*[number of angles + blank line underneath] + 2 header lines
CSVFileLines = ["" for i in range(numL*(len(angle)+1)+2)]

# Append the first two rows (model name and energies)
# Append corner item
CSVFileLines[0] += "Jpi,,,"
CSVFileLines[1] += ",,,"
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
		# Loop over energy + 3 (for line of angles in third column and for L in second column and for jpi in first column) [one column]
		for k in range(len(energy)+3):
			# Append angles
			if k == 2 and j < len(angle):
				CSVFileLines[i*(len(angle) + 1) + j + 2] += str(angle[j]) + ","

			# Append JPI
			elif k == 0 and j == 0:
				CSVFileLines[i*(len(angle) + 1) + j + 2] += JPiString( jpi[i] ) + ","
				
			# Append L
			elif k == 1 and j == 0:
				CSVFileLines[i*(len(angle) + 1) + j + 2] += str( JPi2L( jpi[i] ) ) + ","

			# Append actual data
			elif j < len(angle) and k > 2:
				CSVFileLines[i*(len(angle) + 1) + j + 2] += str( CS[i][k-3][j] ) + ","

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

#"""













