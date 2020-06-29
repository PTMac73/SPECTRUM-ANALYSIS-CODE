# importEnergies [FUNCTION]
# Imports the list of excitation energies from a list
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
def ImportEnergy(inFileDir):
	inFile = open(inFileDir)
	energy = []
	for line in inFile:
		a = line.rstrip("\n")
		if a != "":
			energy.append(float(a))
	inFile.close()
	return(energy)
