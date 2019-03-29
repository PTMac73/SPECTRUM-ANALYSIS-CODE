# getOptions [function]
# Gets the options from the desired options file and imports it into ptolemyMaster.py
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# LAST EDITED: 08/10/18
# =============================================================================================== #
def getOptions(inFileDir):
	# Define dictionary
	dct = {
		"reactionName": "string",
		"reactionFullName": "string",
		"ELAB": -1.0,
		"Z": -1,
		"A": -1,
		"reactionType": "string",
		"M_Target": -1.0,
		"M_Projectile": -1.0,
		"M_Ejectile": -1.0,
		"M_Product": -1.0,
		"D": -1,
		"Asymptopia": -2.0,
		"L": -2
	}
	
	# Open the file
	inFile = open(inFileDir)
	# Get the list of values
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
	
	# Check for not enough options
	for key,val in dct.items():
		if dct[key] == "string" or dct[key] == -1.0 or dct[key] == -1:
			sys.exit("Options file does not contain enough options")
	
	# Assign values
	reactionName = dct["reactionName"]
	reactionFullName = dct["reactionFullName"]
	ELAB = dct["ELAB"]
	Z = dct["Z"]
	A = dct["A"]
	reactionType = dct["reactionType"]
	M_Target = dct["M_Target"]
	M_Projectile = dct["M_Projectile"]
	M_Ejectile = dct["M_Ejectile"]
	M_Product = dct["M_Product"]
	D = dct["D"]
	Asymptopia = dct["Asymptopia"]
	L = dct["L"]
	return [reactionName, reactionFullName, ELAB, Z, A, reactionType, M_Target, M_Projectile, M_Ejectile, M_Product, D, Asymptopia, L]

