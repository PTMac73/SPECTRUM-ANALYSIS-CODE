# Asks for a gf3 output (from a text file) and reads out a tab-delimited version (with errors done
# correctly) to copy and paste easily into a spreadsheet.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
from os import system
import sys

rev_array = [ "-r", "--reverse" ]
b_rev = 0
one_line_array = [ "-o" "--one-line" ]
b_one_line = 0
warn_array = ["-w", "--suppress-warnings"]
b_warn = 0


# Clear the terminal window
system('clear')

# Process arguments given
if len(sys.argv) > 1:
	for i in range( 1, len(sys.argv) ):
		# Reverse array
		if sys.argv[i] in rev_array:
			b_rev = 1

		# One line
		if sys.argv[i] in one_line_array:
			b_one_line = 1

		# Warnings
		if sys.argv[i] in warn_array:
			b_warn = 1

# Ask for file directory
in_file_dir = "data.txt"

# List for storing the data from the file
full_data = []	# Stores the total gf3 output
data = []		# For storing useful lines
fitted_flag = 0

# Open the file
in_file = open(in_file_dir,"r")

# Store the contents of the file line-by-line
for line in in_file:
	full_data.append(line)

# Close the file
in_file.close()

# Extract x^2, A, B, C, R, Beta, Step
bg_shape = ["-1" for x in range(0,7) ]

# Split the line
for i in range(0,len(full_data)):
	split_line = full_data[i].split()

	# Test the line
	try:
		if split_line[0] == "position" and data == []:
			data = full_data[i+1:len(full_data)]
			fitted_flag = 1
		elif split_line[0] == "Chs" and data == []:
			data = full_data
		else:
			pass
	except:
		pass

	for j in range(0,len(split_line)):
		if split_line[j] == "Chisq/d.o.f.=":
			bg_shape[0] = split_line[j+1].rstrip(",")

		if split_line[j] == "A":
			bg_shape[1] = split_line[j+2].rstrip(",")

		if split_line[j] == "B":
			bg_shape[2] = split_line[j+2].rstrip(",")

		if split_line[j] == "C":
			bg_shape[3] = split_line[j+2].rstrip(",")

		if split_line[j] == "R":
			bg_shape[4] = split_line[j+2].rstrip(",")

		if split_line[j] == "Beta":
			bg_shape[5] = split_line[j+2].rstrip(",")

		if split_line[j] == "Step":
			bg_shape[6] = split_line[j+2].rstrip(",")

# Check the fit parameters
if fitted_flag == 1 and float(bg_shape[6][0:len(bg_shape[6])-3]) != 0:
	print("-------------------------------------------------------------------------------\n  Warning! Step != 0  -------------------------------------------------------------------------------\n")

	for i in range(0,len(bg_shape)):
		if bg_shape[i] == "-1" and fitted_flag == 1:
			print("-------------------------------------------------------------------------------\n  Warning! Not detected some values in the background, shape, or chi^2\n-------------------------------------------------------------------------------")

# Define dictionary
if fitted_flag == 1:
	quantity_names = {
		0 : "position",
		2 : "width",
		4 : "height",
		6 : "area",
		8 : "centroid"
	}
else:
	quantity_names = {
		0 : "LB",
		1 : "UB",
		2 : "area",
		4 : "centroid"
	}


##### Start extracting spectrum results
# Loop over lines
for i in range(0,len(data)):
	split_data = data[i].split()

	if fitted_flag == 1:
		# Remove the first value (line number)
		split_data = split_data[1:len(split_data)]
	else:
		# Remove extraneous values
		temp_list = []
		for j in range(0,len(split_data)):
			if j == 1 or j == 3:
				temp_list.append(split_data[j].rstrip(","))
			elif ":" in split_data[j]:
				temp_list.append(split_data[j+1])

		split_data = temp_list

	# Declare useful array for storing all values (*2 for errors)
	if i == 0:
		useful_data = [[] for j in range(0,len(data)-1)]
		useful_data_string = [[] for j in range(0,len(data)-1)]

	# Loop over each value in list
	for j in range(0,len(split_data)):
		# Find relevant characters: "(", ")", "."
		if "(" in split_data[j]:
			for k in range(0,len(split_data[j])):
				if split_data[j][k] == "(":
					bracketL = k
		else:
			bracketL = -1

		if ")" in split_data[j]:
			for k in range(0,len(split_data[j])):
				if split_data[j][k] == ")":
					bracketR = k
		else:
			bracketR = -1

		if "." in split_data[j]:
			for k in range(0,len(split_data[j])):
				if split_data[j][k] == ".":
					decimal_point = k
		else:
			# Some quantities may not have a decimal point
			decimal_point = -1

		# Define quantities from these
		# Precision is the number of decimal places the number has
		if decimal_point > 0 and bracketL != -1:
			precision = bracketL - decimal_point - 1
		else:
			precision = 0

		# This distinguishes the numbers in and out of brackets
		if bracketL != -1 and bracketR != -1:
			num_in_brackets = split_data[j][bracketL+1:bracketR]
			num_outside_brackets = split_data[j][0:bracketL]

			# Start adding numbers into the lists - want outside number first, and then inside number
			useful_data[i].append(num_outside_brackets)

			# Define a factor to generate correct uncertainty on values
			factor = 0.1 ** precision

			# Now correctly calculate the uncertainty
			if precision == 0:
				# No decimal places => therefore just a number
				useful_data[i].append(int(float(num_in_brackets)*factor))
			else:
				# Some decimal places - round it so you don't get weird numbers like 0.01000000003
				useful_data[i].append(round(float(num_in_brackets)*factor,precision))

		else:
			# No number in brackets - just append the number
			if "." in split_data[j]:
				useful_data[i].append( float(split_data[j]) )
			else:
				useful_data[i].append( int(split_data[j]) )

# Sort the data in descending order based on position
ud_sort = sorted( useful_data, key = lambda x: float(x[0]), reverse=True )

# Convert data to strings so it can be output to console easily (except for the energy and error in energy, which is useless)
for i in range(0,len(ud_sort)):
	for j in range(0,len(ud_sort[i])-2):
		useful_data_string[i].append(str(ud_sort[i][j]))

# Swap order if in wrong order
loop_array = range(0,len(ud_sort))
if b_rev == 1:
	loop_array.reverse()

# Now print all this to the console (with error message if uncertainties are very large)
for i in loop_array:
	for j in range(0,len(ud_sort[i])-2):
		if j % 2 == 0 and ud_sort[i][j+1] > float(ud_sort[i][j]) and ( (fitted_flag == 0 and j > 1) or (fitted_flag == 1) ):
			if b_one_line == 0 and b_warn == 0:
				print("## Warning: " + quantity_names[j] + " has error larger than value --> " + str(ud_sort[i][j]) + " +/- " + str(ud_sort[i][j+1]) )

	# Print differently based on b_one_line
	if b_one_line == 0:
		print("\t".join(useful_data_string[i]))
	else:
		print("\t".join(useful_data_string[i])),
		print("\t"),

	# Print warning if there is a negative height that has slipped in
	if fitted_flag == 1 and "-" in ud_sort[i][4]:
		print("-------------------------------------------------------------------------------\n  Warning! Negative height detected \n-------------------------------------------------------------------------------")

# Now print the useful list
if fitted_flag == 1:
	print("[" + ",".join(bg_shape) + "]")

# Print blank line to make things easier to read
print("")
