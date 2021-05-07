# Cleans DWUCK output files
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
import sys

# Import file
in_file_path = sys.argv[1]
in_file = open(in_file_path, "r")

# Create array to store the data
angle = []
dwcs = []
flag_record = 0
flag_fail = 0

# Scrape the data out
for line in in_file:
	if flag_fail == 0:
		# Check to see whether I need to turn off the recording flag
		if "0Tot-sig" in line and flag_record == 1:
			flag_record = 0

		# Record the data 
		if flag_record == 1:
			# Only want the first two values from the line
			temp_line = line.split()
			angle.append( float(temp_line[0]) )
			dwcs.append( float(temp_line[1]) )

		# Check to see whether to record the following line or not
		if "Inelsig" in line and flag_record == 0:
			flag_record = 1
		
		# Check to see if there are any fails
		if "FAILS" in line:
			flag_fail = 1
	
in_file.close()


# Write to an output clean file
if flag_fail == 0:
	out_file = open(in_file_path + "-clean", "w")
	for i in range(0,len(angle)):
		out_file.write(str(angle[i]) + "\t" + str(dwcs[i]) + "\n")
	out_file.close()
else:
	print(in_file_path + " -> FAIL!")
