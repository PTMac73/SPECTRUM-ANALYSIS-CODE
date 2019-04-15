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
from functionWritePtolemyBlock import *
from functionGenerateLValues import *
from functionPtolemyParameters import *
from functionImportEnergies import *
from functionGetOptions import *

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
[reactionName, reactionFullName, ELAB, Z, A, reactionType, M_Target, M_Projectile, M_Ejectile, M_Product, D, Asymptopia, L] = getOptions(optionFileDir)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CALCULATE RELEVANT QUANTITIES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Import Energies
energy = importEnergy(PARAMETERFileDir + "energyList.txt")

# Generate L Values
if L == -2:
	L, J, JP, node = getSpecificStates(A-Z,D)
else:
	L, J, JP, node = getNodes(A-Z,D,L)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAKE THE PTOLEMY FILE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Need to do the same inputs for a given energy
for i in range(0,len(energy)):
	# Open the file	
	inFile = open(INPUTFileDir + fileNameIN(reactionName,energy[i]),"w")
	
	# Generate the correct Ptolemy input parameter string
	s = obtainPTList(reactionType, A, Z, ELAB, energy[i], M_Target, M_Projectile, M_Ejectile, M_Product, potential_in, potential_out)
	
	# Now need to loop over possible states
	for a in range(0, len(s) ):
		for j in range(0,len(J)):
			if j != len(J) - 1:
				# Write a normal block if not the last block
				WritePtolemyBlock(inFile,reactionFullName,JP[j],L[j],energy[i],ELAB,node[j],s[a],Asymptopia,0)

			else:
				# Last block, so need to write end of the file as well
				WritePtolemyBlock(inFile,reactionFullName,JP[j],L[j],energy[i],ELAB,node[j],s[a],Asymptopia,1)

	# Close the file
	inFile.close()

























