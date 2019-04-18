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
		"reaction_name": "string",
		"reaction_full_name": "string",
		"ELAB": -1.0,
		"Z": -1,
		"A": -1,
		"reaction_type": "string",
		"M_Target": -1.0,
		"M_Projectile": -1.0,
		"M_Ejectile": -1.0,
		"M_Product": -1.0,
		"D": -1,
		"Asymptopia": -2.0,
		"L": -2,
		"ANGLEMIN": -2.0,
		"ANGLEMAX": -2.0,
		"LABANGLES": -2,
		"ANGLESTEP": -2.0
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
