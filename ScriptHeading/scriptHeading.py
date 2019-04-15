# scriptHeading.py
# Makes a heading for a script in a nice format
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
import sys
import numpy as np

# FORMATTING VARIABLES
heading_length = 99
comment_char = "#"
line_char = "~"

# CONSTRUCT THE STRING
# Grab the input string
title = sys.argv[1]

# Calculate the line length (6 characters needed for spaces and initial and final characters)
line_length = 0.5*( heading_length - 6 - len(title) )

# Check that there are enough characters
if line_length < 0:	
	print("String too long!")
	exit(1)

# Check if the string is odd
if np.mod(line_length, 1.0) == 0.0:
	# Even number so can do same number
	output = "# " + int(line_length)*line_char + " " + title.upper() + " " + int(line_length)*line_char + " #"
else:
	# Odd number, so add a character on the end
	output = "# " + int(line_length - 0.5)*line_char + " " + title.upper() + " " + int(line_length + 0.5)*line_char + " #"

print(output)

