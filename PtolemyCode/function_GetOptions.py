# getOptions [function]
# Gets the options from the desired options file and imports it into ptolemyMaster.py
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
import sys

def GetOptions(inFileDir):
	# Define dictionary
	# Necessary parameters -> string, -1, -1.0
	# Optional parameters -> -2, -2.0
	dct = {
		"reaction_name": "string",			# Short Reaction Name (for file name)		e.g. 28MgDP
		"reaction_full_name": "string",		# Full Reaction Name (for Ptolemy)			e.g. 28Mg(d,p)29Mg
		"ELAB": -1.0,						# Lab Energy in MeV
		"Z": -1,							# Proton number of the residual nucleus
		"A": -1,							# Mass number of the residual nucleus
		"reaction_type": "string",			# Specifies reaction for ptolemyMaster.py	e.g. dp
		"M_Target": -1.0,					# Mass of the target (a.m.u.)
		"M_Projectile": -1.0,				# Mass of the projectile (a.m.u.)
		"M_Ejectile": -1.0,					# Mass of the ejectile (a.m.u.)
		"M_Product": -1.0,					# Mass of the product (a.m.u.)
		"D": -1,							# Direction of states to occupy (1 for addition to residual nucleus, 0 for removal from residual nucleus)#
		"LMAX" : -1,						# Defines the maximum L
		
		# OPTIONAL PARAMETERS
		"Asymptopia": -2.0,					# Specifies asymptopia in Ptolemy
		"L": -2,							# Specifies a given L
		"ANGLEMIN": -2.0,					# Minimum angle for calculation
		"ANGLEMAX": -2.0,					# Maximum angle for calculation
		"LABANGLES": -2,					# Use lab angles
		"ANGLESTEP": -2.0,					# Step between angles
	}
	
	# Open the file
	inFile = open(inFileDir)

	# Store the lines in the file in the dictionary
	for line in inFile:
		try:
			if type(dct[line.split()[0]]) == int:
				dct[line.split()[0]] = int(line.split()[1])
			elif type(dct[line.split()[0]]) == float:
				dct[line.split()[0]] = float(line.split()[1])
			elif type(dct[line.split()[0]]) == str:
				dct[line.split()[0]] = str(line.split()[1])
		except:
			pass
	
	# Close the file
	inFile.close()
	
	# Check for not enough necessary options
	for key,val in dct.items():
		if dct[key] == "string" or dct[key] == -1.0 or dct[key] == -1:
			sys.exit("Options file does not contain enough options")

	# Return the dictionary
	return dct
