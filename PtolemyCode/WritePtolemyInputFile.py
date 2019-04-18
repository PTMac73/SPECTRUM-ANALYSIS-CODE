# WritePtolemyInputFile
# Generates the input files for Ptolemy using a range of custom functions
# to generate various things.
# N.B. First argument passed to this script is the options
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# Import functions and headers
import numpy as np

# Import arguments
import sys
import os
import importlib

#from functionImportINOUTdata import *
from function_WritePtolemyBlock import *
from function_GenerateLValues import *
from function_PtolemyParameters import *
from function_ImportEnergies import *
from function_GetOptions import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GET THE FILE DIRECTORIES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Get the file directories
INPUTFileDir = os.environ["INPUT_FILE_DIR"]
OUTPUTFileDir = os.environ["OUTPUT_FILE_DIR"]
PARAMETERFileDir = os.environ["PARAMETER_DIR"]

# Get the deuteron potential information
potential_in = os.environ["POTENTIAL_IN"]
potential_out = os.environ["POTENTIAL_OUT"]

# Load the option
optionFileDir = sys.argv[1]

# Get the values
opt_dct = GetOptions(optionFileDir)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CALCULATE RELEVANT QUANTITIES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Import Energies
energy = importEnergy(PARAMETERFileDir + "energyList.txt")

# Generate L Values
if opt_dct["L"] == -2:
	L, J, JP, node = GenerateSpinParity( opt_dct["A"] - opt_dct["Z"], opt_dct["Z"], opt_dct["D"] )
else:
	L, J, JP, node = GetNodes( opt_dct["Z"], opt_dct["A"] - opt_dct["Z"], opt_dct["D"], opt_dct["L"] )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAKE THE PTOLEMY FILE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Need to do the same inputs for a given excitation energy
for i in range(0,len(energy)):
	
	# Generate the correct Ptolemy input parameter string
	s, name_list = ObtainPTList(energy[i], potential_in, potential_out, opt_dct)	
	
	# Now need to loop over possible states
	for a in range(0, len(s) ):
		# Open the file	
		inFile = open(INPUTFileDir + FileNameIN( opt_dct["reaction_name"], energy[i], name_list[a] ), "w" )

		# Loop over all states if J
		for j in range(0,len(J)):
			if j == len(J) - 1:
				# Last block, so need to write end of the file as well
				WritePtolemyBlock( inFile, JP[j], L[j], node[j], energy[i], s[a], opt_dct, 1 )
			else:
				# Write a normal block if not the last block
				WritePtolemyBlock( inFile, JP[j], L[j], node[j], energy[i], s[a], opt_dct, 0 )

		# Close the file
		inFile.close()






