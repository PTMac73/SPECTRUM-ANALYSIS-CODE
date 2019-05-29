# Attempt to clean up the ptolemy output files. Adapted from someone else's code
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
import string
import sys

# Define a function to test if something is a float or not
# Return 1 if successful, and 0 if it fails
def isfloat(str):
	ret = 1
	try:
		this = float(str)
	except ValueError:
		ret = 0
	return ret

# MAIN FUNCTION
# Input file is the first argument - store it
infile = open(sys.argv[1])

# Open an output file for cleaning
outfile = open(sys.argv[1]+'-clean','w')

# Declare some flags 
asymptopia_flag = 0
warning_flag = 0
elastic_flag = 0

# Loop over the lines in the file
while True:
	# Store the line
	line=infile.readline()
	
	# If the line is empty - end of file, so break the while loop
	if (line==''):					
		break
	
	# Split the line at the spaces into different components
	words=string.split(line)
	
	# STORE THE DATA
	# Inelastic
	if ( len(words) > 1 and words[0] == "ANGLE" and elastic_flag == 0 ):	#look for lines starting with 'ANGLE'
		
		# Entered a region where there are useful numbers - deal with them in a new loop
		while True:
			# Get the next line and split it
			temp = string.split( infile.readline() )
			
			# Test if it is at the end of the file
			if ( len(temp) > 1 and temp[0] == "0TOTAL:" ):
				# If yes, write a new line and break the loop
				outfile.write('\n')
				break
			
			# Test if the line has length > 8 and the first two fields are numbers
			elif ( len(temp) > 8 and isfloat( temp[0] ) and isfloat( temp[1] ) ):
				outfile.write(temp[0] + ' ' + temp[1] + '\n')

	# Elastic
	elif ( len(words) > 1 and words[0] == "0" and words[1] == "ANGLE" and elastic_flag == 1 ):
		# Entered a region where there are useful numbers - deal with them in a new loop
		while True:
			# Get the next line and split it
			temp = string.split( infile.readline() )
			
			# Test if it is at the end of the file
			if ( len(temp) > 1 and temp[0] == "0TOTAL" ):
				# If yes, write a new line and break the loop
				outfile.write('\n')
				break
			
			# Test if the line has length > 7 and the first two fields are numbers
			elif ( len(temp) > 7 and isfloat( temp[0] ) and isfloat( temp[3] ) ):
				outfile.write(temp[0] + ' ' + temp[3] + '\n')

	# TEST FLAGS
	# Now look to see if there are any asymptopia issues
	if "INCREASE ASYMPTOPIA TO MORE THAN" in line and asymptopia_flag == 0:
		asymptopia_flag = 1

	# Now look to see if there are any warnings
	if "WARNING" in line and warning_flag == 0:
		warning_flag = 1

	# Check to see if it is an elastic scattering state
	if line == "0INPUT... ELASTIC SCATTERING\n":
		elastic_flag = 1

# Print a message once complete
# Get the filename
fileName = sys.argv[1].split("/")

# Print a blank line
print("")

# Print warnings if detected
if asymptopia_flag == 1:
	print("\033[1;36mAsymptopia probably incorrect in " + fileName[len(fileName)-1] + "\033[0m")

if warning_flag == 1:
	print("\033[1;33mWarning detected in " + fileName[len(fileName)-1] + "\033[0m")

# Close both of the files
infile.close()
outfile.close()
