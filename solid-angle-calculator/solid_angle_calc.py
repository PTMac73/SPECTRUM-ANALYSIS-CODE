# solid_angle_calc.py
# Extracts the positions from a sheet and calculates the angles for them using ROOT
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# Department of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# INPUT: DET#,EX,z,theta,z,theta,...,z,theta (no headings)
# OUTPUT: A set of files that contain columns of ex,z based on original column number
# USAGE: python solid_angle_calc.py YOUR_CSV_FILE.csv
# =============================================================================================== #
import sys
import os

# Read in the files
file_in_loc = sys.argv[1]
file_in = open(file_in_loc)

# Store the data
data = []
num_cols = 0
for line in file_in:
	# Remove unnecessary characters and split the data
	temp_list = line.rstrip("\n").split(",")

	# Get the number of columns on the first line
	if data == []:
		for i in range(0,len(temp_list)):
			if i > 1 and temp_list[i] != '':
				num_cols += 1

	# Store the data
	data.append(temp_list)

file_in.close()

# Define storage
Ex = []
z = [ [] for x in range(0,num_cols) ]

# Extract useful quantities
for i in range(0,len(data)):
	# Index for z
	index = 0
	if len(data[i]) > 1:
		# Grab excitation
		Ex.append( data[i][1] )

		# Grab the z for a given column
		for j in range(0,len(data[i])):
			if j > 1 and data[i][j] != '':
				z[index].append(data[i][j])
				index += 1


# Write the files
for i in range(0,num_cols):
	file_out_loc = os.path.dirname(file_in_loc) + "/col" + str(i) + ".dat"
	file_out = open(file_out_loc, "w+")
	
	# Write to the file
	for j in range(0,len(Ex)):
		file_out.write(str(Ex[j]) + "\t" + str(z[i][j]) + "\n")

	# Close the file
	file_out.close()
	

