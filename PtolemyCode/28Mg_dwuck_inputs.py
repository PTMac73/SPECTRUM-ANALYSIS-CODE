# Writes DWUCK input files for the 28Mg(d,p) reaction
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
import function_WriteDWUCKBlock as dwuck
from dwuck_options import *

# CREATE LOOP ARRAY VARIABLES
Ex = [ 
	0.0,
	0.0546,
	1.092,
	1.432,
	2.270,
	2.501,
	2.900,
	3.220,
	3.906,
	3.980,
	4.045,
	4.360,
	5.623,
	5.811,
	6.043
	]
	
n = [ 1, 1, 1, 0, 0, 0, 0 ]
l = [ 0, 1, 1, 2, 2, 3, 3 ]
J = [ 1, 0, 1, 0, 1, 0, 1 ]

theta_start = [0, 20, 40, 60, 80 ]

input_file_dir = "/home/ptmac/Documents/07-CERN-ISS-Mg/Mg-Analysis/DWUCK-IN"


# Loop over Ex
for i in range(0,len(Ex)):
	# Loop over jpi
	for j in range(0, len(n)):
		# Generate file name
		file_name = input_file_dir + "/DW_28MgDP_" + format(int(1000*Ex[i]), "04d") + "_" + str(l[j]) + "_" +  str(n[j]) + spdf[l[j]] + str(2*( l[j] + J[j] ) - 1) + "_2.in"
	
		# Open the file for writing
		out_file = open(file_name,"w")
	
		# Loop over angles
		for k in range(0,len(theta_start)):
			SetDWOptions(Ex[i], n[j], l[j], J[j], theta_start[k], out_file )
		
			# Write DWUCK Block to file
			if k < len(theta_start) - 1:
				dwuck.WriteDWUCKOutput(0)
			else:
				dwuck.WriteDWUCKOutput(1)
		
		
		# Close the file
		out_file.close()
















