# Attempt to clean up the ptolemy output files. Adapted from someone else's code
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
import string
import sys
from datetime import *

# Define a function to test if something is a float or not
# Return 1 if successful, and 0 if it fails
def isfloat(str):
	ret = 1
	try:
		this = float(str)
	except ValueError:
		ret = 0
	return ret
	
def JPiNumber(jpi):
	# jpi of form "x/2+" or "x/2-" where x is an integer
	if  jpi[-1] == "+":
		pi = 1
	elif jpi[-1] == "-":
		pi = -1
	else:
		print( jpi + " is not a valid JPI string" )
		exit(1)
	
	j = int( jpi.split("/")[0] ) # This gives 1 for 1/2+
	
	# Carry out complicated operation to assign ordering
	fac = int( -0.5*( ( ( j % 4 ) + pi ) % 4 ) )
	ret = "%02d" % ( j + fac )
	#print( "\t".join([ jpi, str(j%4 + pi), str(pi), str(fac),ret] ) )
	return ret
	
	
def GetSpinParity(s):
	# String resembles something like "028Mg(d,p)29Mg(3/2+ 0.0) "
	# Split at bracket
	t = s.split("(")
	
	for i in range( 0, len(t) ):
		if "/2+" in t[i]:
			return str( JPiNumber(t[i]) ) + "-" + t[i].replace("+","p").replace("/","")
		if "/2-" in t[i]:
			return str( JPiNumber(t[i]) ) + "-" + t[i].replace("-","n").replace("/","")
	print("Could not find spin parity in " + s + ".")
	exit(1)
	
	
def CleanFileName(s, sp):
	# Split at .
	t = s.split(".")
	
	# Should be [ PRE + Estart, Eend, suffix ] 
	u = ""
	
	for i in range(0,len(t)):
		u += t[i]
		
		if i == len(t) - 2:
			u += "-" + sp + "."
		elif i < len(t) - 2:
			u += "."
			
	u += "-clean"
	return str(u)
	
	

# MAIN FUNCTION
# Input file is the first argument - store it
infile = open(sys.argv[1])

# Open a logfile for storing issues with asymptopia
logfile = open("logfile.log", 'a')

# Declare some flags 
asymptopia_flag = 0
warning_flag = 0
elastic_flag = 0

# Loop over the lines in the file
while True:
	# Store the line
	line = infile.readline()
	
	# If the line is empty - end of file, so break the while loop
	if (line==''):					
		break
	
	# Split the line at the spaces into different components
	words = string.split(line)
	
	# Get the spin-parity
	if ( len(words) > 1 and words[0] == "0INPUT..." and words[1] == "REACTION:" ):
		sp = GetSpinParity( words[2] )
			
		# Open an output file for cleaning
		filename = CleanFileName( sys.argv[1], sp )
		outfile = open( filename,'w+')
	
	# STORE THE DATA
	# Inelastic
	if ( len(words) > 1 and words[0] == "ANGLE" and elastic_flag == 0 ):	#look for lines starting with 'ANGLE'
	
		# Check the file is open for writing
		if outfile.closed:
			print("ERROR. FILE NOT OPEN!")
			exit(1)
		
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
	
	# Record in log file
	logfile.write( datetime.now().strftime("%F %X") + ".....Asymptopia.............." + fileName[len(fileName)-1] + "\n" )

if warning_flag == 1:
	print("\033[1;33mWarning detected in " + fileName[len(fileName)-1] + "\033[0m")

# Close all of the files
infile.close()
outfile.close()
logfile.close()
