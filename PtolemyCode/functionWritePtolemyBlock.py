# writeInputFile [FUNCTION]
# Writes a block of Ptolemy code for an input file
# =============================================================================================== #
# OTHER FUNCTIONS
# fileNameCSV - Generates the file name used by the CSV files
# fileNameIN - Generates the file name used by the Ptolemy input files
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# inFile -> The open file to which the output is written
# ReactionFullName -> Full name of the nuclear reaction e.g. 122Sn(d,p)123Sn
# jp ->	The spin parity of the state e.g. 11/2-
# energy ->	The energy level of the state
# ELAB -> The lab beam energy in MeV
# node -> nJpi is the state, where n is the node number
# IN ->	The input parameters
# OUT -> The output parameters
# last -> Flag that says whether it's the last file
# =============================================================================================== #

# Define a function to write a block of Ptolemy code
def WritePtolemyBlock(inFile, ReactionFullName,jp,L,energy,ELAB,node,s,Asymptopia,last):
	# Write all the necessary lines to the file
	inFile.write('''reset
r0target
print 0
''')
	inFile.write("REACTION: " + ReactionFullName + "(" + jp + " " + str(energy) + ") ELAB=" + str(ELAB))
	inFile.write('''
PARAMETERSET dpsb labangles r0target lstep=1 lmin=0 lmax=30 maxlextrap=0
PROJECTILE
NODES = 0
R = 1   A = 0.5   WAVEFUNCTION = av18   L = 0
''')
	if Asymptopia > 0:
		inFile.write("ASYMPTOPIA=" + str(Asymptopia) + "\n")
	inFile.write(''';
TARGET
''')
	# Remove parity from jp (if it exists)
	parityFlag = 0
	if ("+" or "-") in jp:
		parityFlag = 1
	
	# Continue writing
	if parityFlag == 0:
		inFile.write("nodes=" + str(node) + " l=" + str(L) + " jp=" + jp + " r0=1.28 a=0.65 vso=6 rso0=1.10 aso=0.65 rc0=1.3\n")
	else:
		inFile.write("nodes=" + str(node) + " l=" + str(L) + " jp=" + jp[0:len(jp)-1] + " r0=1.28 a=0.65 vso=6 rso0=1.10 aso=0.65 rc0=1.3\n")

	# Write incoming and outgoing things
	inFile.write(";\nINCOMING\n")
	for i in range(0,5):
		inFile.write(s[i] + "\n")
	inFile.write(";\nOUTGOING")
	for i in range(5,10):
		inFile.write("\n" + s[i])
	
	# Finish the file
	inFile.write('''
;
LABANGLES
ANGLEMIN=0 ANGLEMAX=60 ANGLESTEP=1
;
writens crosssec
''')
	if last == 1:
		inFile.write("end")
	else:
		inFile.write("")
	return
	
# Function to generate filenames based on the type and the input quantities
def fileNameCSV(reactionName,ELAB):
	# CSV
	# This contains the Ptolemy incoming and outgoing text data.
	# It depends on the reaction and the energy of the beam only
	CSV = reactionName + "-" + str(ELAB) + "MeV.csv"
	return CSV
	
def decimalPointPos(numString):
	# Find decimal point position
	pointPos = -1
	for i in range(0,len(numString)):
		if numString[i] == ".":
			pointPos = i
			break
	
	return pointPos
	
def fileNameIN(reactionName,energy):
	# Ptolemy input file
	# This contains the code for the Ptolemy input file
	# It depends on the reaction, and the energy of the state
	
	# Ensure that the energy contains 3 decimal places
	energyString = str(round(energy,3))
	while decimalPointPos(energyString) != len(energyString) - 4:
		if decimalPointPos(energyString) == -1:
			energyString = energyString + ".000"
		else:
			energyString = energyString + "0"
	inFileName = reactionName + "-" + energyString + ".in"
	return inFileName
