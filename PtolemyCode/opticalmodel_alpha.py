# opticalmodel_alpha
# Functions for alpha optical models
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
from opticalmodel_globals import *
import numpy as np

alpha_dct = {
	"BP":    [0,1],
	"len":       1,
	"ALL_A": [0,1]
}


# Return the names of the helion potentials alphabetically
def AlphaModelNumber():
	return [ "BassaniPicard" ]

# bassaniPicard is the potential used for a
def BassaniPicard(A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H):
	# CHECK VALUE OF H
	CheckP(H)

	# CALCULATE TRIVIAL PARAMETERS
	[N, Q, E] = CalcTrivials(A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H)
	
	# Calculate final parameters
	v = 207.0
	vi = 28.0
	vsi = 0.0
	vso = 0.0
	vsoi = 0.0
	
	r0 = 1.30
	ri0 = 1.30
	rsi0 = 0.0
	rso0 = 0.0
	rsoi0 = 0.0
	
	a = 0.65
	ai = 0.52
	asi = 0.0
	aso = 0.0
	asoi = 0.0
	
	rc0 = 1.40
	
	# Format final paramaters into a list of strings
	v_list = [v, vi, vsi, vso, vsoi]
	r_list = [r0, ri0, rsi0, rso0, rsoi0]
	a_list = [a, ai, asi, aso, asoi]
	string_list = MakeStringList(v_list,r_list,a_list,rc0)
	
	if PRINT == 1:
		PrintOpticalModel(string_list, "Bassani and Picard alpha")
		PrintCalculatedQuantities(A,Z,E,Q)
	return string_list
