# ScriptHeading.py
# Makes a heading for a script in a nice format
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
import sys
import numpy as np


def HelpMessage():
	print('''Usage:
  python ScriptHeading.py  -h | --help
  python ScriptHeading.py  ( --len=NUM ) ( --align=X ) [ string ]
	
  -h | --help displays this help message and exits the script.
  NUM is a number that defines the length of the title
  X can take the value c, l or r for centre, left, and right alignment
    respectively.
  string is the mandatory argument that will be capitalised and placed
    in the title.
''')


# MAIN SCRIPT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Allowed options
allowed_aligns = ["c","C","l","L","r","R"]

# Grab the input string and options
arguments = sys.argv
strings = []
for i in range(1, len(arguments) ):

	# Help option
	if arguments[i] == "-h" or arguments[i] == "--help":
		HelpMessage()
		exit(0)
	
	# Align option
	if arguments[i][0:8] == "--align=":
		align = arguments[i][8:len(arguments[i])]
		if align not in allowed_aligns:
			print( str(align) + " is not an allowed align parameter [c/l/r]. Using centre-alignment..." )
			align = "c"
	
	# Length option
	elif arguments[i][0:6] == "--len=":
		try:
			heading_length = int(arguments[i][6:len(arguments[i])])
		except:
			print( str( arguments[i][6:len(arguments[i])] ) + " is not an allowed length. Using 99 characters...")
			heading_length = 99

	else:
		strings.append(arguments[i])


# Set defaults
try:
	len(align)
except:
	align = "c"
	
try:
	2*heading_length
except:
	heading_length = 99

# FORMATTING VARIABLES
comment_char = "#"
line_char = "~"

# CONSTRUCT THE STRING
# Calculate the line length (6 characters needed for spaces and initial and final characters)
for j in range(0, len(strings) ):
	# Do alignment checks
	# Centre-alignment
	if align == "c" or align == "C":
		# Calculate length of characters
		line_length = 0.5*( heading_length - 6 - len(strings[j]) )
		
		# Check that there are enough characters
		if line_length < 0:	
			print("String " + strings[j] + " too long!")
			continue
	
		# Check if odd or even
		if np.mod(line_length, 1.0) == 0.0:
			# Even number so can do same number
			output = "# " + int(line_length)*line_char + " " + strings[j].upper() + " " + int(line_length)*line_char + " #"
		else:
			# Odd number, so add a character on the end
			output = "# " + int(line_length - 0.5)*line_char + " " + strings[j].upper() + " " + int(line_length + 0.5)*line_char + " #"
			
	else:
		# Left or right aligned, so can change the line length
		# Calculate length of characters
		line_length = heading_length - 5 - len(strings[j])
		
		# Check that there are enough characters
		if line_length < 0:	
			print("String " + strings[j] + " too long!")
			continue
		
		if align == "r" or align == "R":
			output = "# " + int(line_length)*line_char + " " + strings[j].upper() + " #"
			
		else:
			output = "# " + strings[j].upper() + " " + int(line_length)*line_char + " #"
	
	print("\n" + output + "\n")


































