# writeInputFile [FUNCTION]
# Writes a block of Ptolemy code for an input file
# =============================================================================================== #
# OTHER FUNCTIONS
# FileNameCSV - Generates the file name used by the CSV files
# FileNameIN - Generates the file name used by the Ptolemy input files
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# inFile -> The open file to which the output is written
# reaction_full_name -> Full name of the nuclear reaction e.g. 122Sn(d,p)123Sn
# jp ->	The spin parity of the state e.g. 11/2-
# energy ->	The energy level of the state
# ELAB -> The lab beam energy in MeV
# node -> nJpi is the state, where n is the node number
# IN ->	The input parameters
# OUT -> The output parameters
# last -> Flag that says whether it's the last file
# =============================================================================================== #

# Define a function to write a block of Ptolemy code
def WritePtolemyBlock( inFile, jp, L, node, energy, s, opt_dct, Q, last ):
	# Choose Ptolemy block to write based on whether it is elastic scattering or not
	if opt_dct["reaction_type"] == "dd":
		WritePtolemyBlockElastic( inFile, jp, L, node, energy, s, opt_dct, last )
	else:
		WritePtolemyBlockTransfer( inFile, jp, L, node, energy, s, opt_dct, Q, last )

	return


def WritePtolemyBlockTransfer( inFile, jp, L, node, energy, s, opt_dct, Q, last ):
	# Write all the necessary lines to the file
	inFile.write('''reset
r0target
print 0
''')
	inFile.write("REACTION: " + opt_dct["reaction_full_name"] + "(" + jp + " " + str(energy) + ") ELAB=" + str(opt_dct["ELAB"]) + " Q=" + str( round( Q, 3 ) ) )
	inFile.write('''
PARAMETERSET dpsb labangles r0target lstep=1 maxlextrap=0
PROJECTILE
NODES = 0
R = 1   A = 0.5   WAVEFUNCTION = av18   L = 0
''')
	if opt_dct["Asymptopia"] > 0:
		inFile.write("ASYMPTOPIA=" + str(opt_dct["Asymptopia"]) + "\n")
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
	
	# Lab Angles?
	inFile.write(";\n")
	if opt_dct["LABANGLES"] == 1:
		inFile.write("LABANGLES\n")
	
	# Minimum angle
	if opt_dct["ANGLEMIN"] != -2.0:
		inFile.write("ANGLEMIN=" + str(opt_dct["ANGLEMIN"]) + " " )
	else:
		inFile.write("ANGLEMIN=0 ")

	# Maximum angle
	if opt_dct["ANGLEMAX"] != -2.0:
		inFile.write("ANGLEMAX=" + str(opt_dct["ANGLEMAX"]) + " " )
	else:
		inFile.write("ANGLEMAX=60 " )

	# Angle step
	if opt_dct["ANGLESTEP"] != -2.0:
		inFile.write("ANGLESTEP=" + str(opt_dct["ANGLESTEP"]) + "\n" )
	else:
		inFile.write("ANGLESTEP=1\n")

	# Finish the block
	inFile.write(";\n")
	inFile.write("writens crosssec\n")

	# Write end?
	if last == 1:
		inFile.write("end")
	else:
		inFile.write("")
	return



def WritePtolemyBlockElastic( inFile, jp, L, node, energy, s, opt_dct, last ):
	# Write all the necessary lines to the file
	inFile.write("reset\n")

	# Convert the full reaction name into something easier
	inFile.write("CHANNEL " + ReactionToChannel( opt_dct["reaction_full_name"] )+ "\n" )

	# Write the lab energy
	inFile.write("ELAB=" + str(opt_dct["ELAB"]) + "\n" )

	# Write incoming and outgoing things
	for i in range(0,5):
		inFile.write(s[i] + "\n")
	
	inFile.write(";\nELASTIC SCATTERING\n")
	# Minimum angle
	if opt_dct["ANGLEMIN"] != -2.0:
		inFile.write("ANGLEMIN=" + str(opt_dct["ANGLEMIN"]) + " " )
	else:
		inFile.write("ANGLEMIN=0 ")

	# Maximum angle
	if opt_dct["ANGLEMAX"] != -2.0:
		inFile.write("ANGLEMAX=" + str(opt_dct["ANGLEMAX"]) + " " )
	else:
		inFile.write("ANGLEMAX=60 " )

	# Angle step
	if opt_dct["ANGLESTEP"] != -2.0:
		inFile.write("ANGLESTEP=" + str(opt_dct["ANGLESTEP"]) + "\n" )
	else:
		inFile.write("ANGLESTEP=1\n")

	# Finish the block
	inFile.write(";\n")
	inFile.write("writens crosssec\n")

	# Write end?
	if last == 1:
		inFile.write("end")
	else:
		inFile.write("")
	return
	



# Function to generate filenames based on the type and the input quantities
def FileNameCSV(reaction_name,ELAB):
	# CSV
	# This contains the Ptolemy incoming and outgoing text data.
	# It depends on the reaction and the energy of the beam only
	CSV = reaction_name + "-" + str( ELAB ) + "MeV.csv"
	return CSV
	
def DecimalPointPos(numString):
	# Find decimal point position
	point_pos = -1
	for i in range(0,len(numString)):
		if numString[i] == ".":
			point_pos = i
			break
	
	return point_pos
	
def FileNameIN( reaction_name, energy, name_of_model ):
	# Ptolemy input file
	# This contains the code for the Ptolemy input file
	# It depends on the reaction, and the energy of the state
	
	# Ensure that the energy contains 3 decimal places
	energyString = str(round(energy,3))
	while DecimalPointPos(energyString) != len(energyString) - 4:
		if DecimalPointPos(energyString) == -1:
			energyString = energyString + ".000"
		else:
			energyString = energyString + "0"
	inFileName = reaction_name + "-" + name_of_model + "-" + energyString + ".in"
	return inFileName


def ReactionToChannel( reaction_full_name ):
	# Reaction should be of form A(b,b)A
	heavy = reaction_full_name[0:reaction_full_name.find("(")]
	light = reaction_full_name[reaction_full_name.find("(")+1:reaction_full_name.find(",")]
	channel = light + " + " + heavy
	return channel










