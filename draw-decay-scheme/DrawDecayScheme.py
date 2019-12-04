# DrawDecayScheme.py
# Reads in NNDC decay scheme information and draws it in TiKZ for LaTeX
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
import sys

# TODO - Functions
	# Convert decay modes
	# Convert isotopes


# Get the input file
in_file_loc = sys.argv[1]
in_file = open(in_file_loc)

# Store levels and gamma properties in here with following format:
# [ 'G', Energy, Intensity ]
# [ 'L', Energy, Spin-parity ]
gamma_data = []

# Import the information
num_decays = -1
record_flag = 0
daughter_nucleus = []
parent_nucleus = []
decay_mode = []

for line in in_file:
	# Extract information from the first line
	if "START" in line:
		num_decays += 1
		gamma_data += [[]]
		daughter_nucleus += [ "" ]
		parent_nucleus += [ "" ]
		decay_mode += [ "" ]
		record_flag = 1
		continue
	if record_flag == 1:
		record_flag = 0
		# Extract the parent nucleus
		daughter_nucleus[num_decays] += str( line[0:5].lstrip(" ").rstrip(" ") )
	
		# Extract the parent nucleus
		parent_nucleus[num_decays] += line[9:14].lstrip(" ").rstrip(" ")
	
		# Extract the decay mode
		decay_mode[num_decays] += line[14:line.find(" DECAY")].lstrip(" ")
		
		print(daughter_nucleus)
	
	# Extract the gamma rays and levels
	gamma_signature = " "*(5 - len(daughter_nucleus[num_decays])) + daughter_nucleus[num_decays] + " "*2 + "G"
	level_signature = gamma_signature.rstrip("G") + "L"
	
	if line[0:8] == gamma_signature:
		g_energy = line[9:19].lstrip(" ").rstrip("\n").rstrip(" ")
		g_intensity = line[21:29].lstrip(" ").rstrip("\n").rstrip(" ")
		gamma_data[num_decays] += [['G', g_energy, g_intensity ]]
	
	if line[0:8] == level_signature:
		l_energy = line[9:19].lstrip(" ").rstrip("\n").rstrip(" ")
		l_spinparity = line[22:39].lstrip(" ").rstrip("\n").rstrip(" ")
		gamma_data[num_decays] += [['L', l_energy, l_spinparity ]]

for i in range(0,len(gamma_data)):
	for j in range(0,len(gamma_data[i])):
		if gamma_data[i][j][0] == 'G':
			print(gamma_data[i][j])




# Extract the mode of decay

# Extract the Q-value

# Extract all the gamma rays and their intensities

# Start drawing the stuff
	# Define coordinates

	# Draw levels

	# Draw arrows

	# Add labels to everything
