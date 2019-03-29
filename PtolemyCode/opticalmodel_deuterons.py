# opticalmodel_deuterons
# Functions for deuteron optical models
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
from opticalmodel_globals import *

# An and Cai
def AnCai(A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H):
	# CHECK VALUE OF H2 - Energy changes if ejectile is deuteron
	CheckP(H)

	# CALCULATE TRIVIAL PARAMETERS
	[N, Q, E] = CalcTrivials(A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H)
		
	# CALCULATE FINAL PARAMETERS
	v = 91.85 - 0.249*E + (1.16e-4)*(E**2) + 0.642*Z*(A**(-1.0/3.0))
	vi = 1.104 + 0.0622*E
	vsi = 10.83 - 0.0306*E
	vso = 3.557
	vsoi = 0
	
	r0 = 1.152 - 0.00776*(A**(-1.0/3.0))
	ri0 = 1.305 + 0.0997*(A**(-1.0/3.0))
	rsi0 = 1.334 + 0.152*(A**(-1.0/3.0))
	rso0 = 0.972
	rsoi0 = 0
	
	a = 0.719 + 0.0126*(A**(1.0/3.0))
	ai = 0.855 - 0.1*(A**(1.0/3.0))
	asi = 0.531 + 0.062*(A**(1.0/3.0))
	aso = 1.011
	asoi = 0
	
	rc0 = 1.303

	# Format final paramaters into a list of strings
	v_list = [v, vi, vsi, vso, vsoi]
	r_list = [r0, ri0, rsi0, rso0, rsoi0]
	a_list = [a, ai, asi, aso, asoi]
	string_list = MakeStringList(v_list,r_list,a_list,rc0)
	
	if PRINT == 1:
		PrintOpticalModel(string_list, "An and Cai deuteron")
		PrintCalculatedQuantities(A,Z,E,Q)
	return string_list

# =============================================================================================== #
# PereyPerey is another potential used for deuterons
def PereyPerey(A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H):
	# CHECK VALUE OF H2 - Energy changes if ejectile is deuteron
	CheckP(H)

	# CALCULATE TRIVIAL PARAMETERS
	[N, Q, E] = CalcTrivials(A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H)
	
	# CALCULATE FINAL PARAMETERS
	v = 81 - 0.22*E + 2*Z*(A**(-1.0/3.0))
	vi = 0.0
	vsi = 14.4 + 0.24*E
	vso = 0.0
	vsoi = 0.0
	
	r0 = 1.15
	ri0 = 0.0
	rsi0 = 1.34
	rso0 = 0.0
	rsoi0 = 0.0
	
	a = 0.81
	ai = 0.0
	asi = 0.68
	aso = 0.0
	asoi = 0.0
	
	rc0 = 1.15

	# Format final paramaters into a list of strings
	# Format final paramaters into a list of strings
	v_list = [v, vi, vsi, vso, vsoi]
	r_list = [r0, ri0, rsi0, rso0, rsoi0]
	a_list = [a, ai, asi, aso, asoi]
	string_list = MakeStringList(v_list,r_list,a_list,rc0)
	
	if PRINT == 1:
		PrintOpticalModel(string_list, "Perey and Perey deuteron")
		PrintCalculatedQuantities(A,Z,E,Q)
	return string_list

# =============================================================================================== #
# LohrHaeberli is another potential used for deuterons
def LohrHaeberli(A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H):
	# CHECK VALUE OF H2 - Energy changes if ejectile is deuteron
	CheckP(H)

	# CALCULATE TRIVIAL PARAMETERS
	[N, Q, E] = CalcTrivials(A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H)
		
	# CALCULATE FINAL PARAMETERS
	v = 91.13 + 2.2*Z*(A**(-1.0/3.0))
	vi = 0.0
	vsi = 218*(A**(-2.0/3.0))
	vso = 7.0
	vsoi = 0.0
	
	r0 = 1.05
	ri0 = 0.0
	rsi0 = 1.43
	rso0 = 0.75
	rsoi0 = 0.0
	
	a = 0.86
	ai = 0.0
	asi = 0.5 + 0.013*(A**(2.0/3.0))
	aso = 0.5
	asoi = 0.0
	
	rc0 = 1.30

	# Format final paramaters into a list of strings
	v_list = [v, vi, vsi, vso, vsoi]
	r_list = [r0, ri0, rsi0, rso0, rsoi0]
	a_list = [a, ai, asi, aso, asoi]
	string_list = MakeStringList(v_list,r_list,a_list,rc0)
	
	if PRINT == 1:
		PrintOpticalModel(string_list, "Lohr and Haeberli deuteron")
		PrintCalculatedQuantities(A,Z,E,Q)

	return string_list
