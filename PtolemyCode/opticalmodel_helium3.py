# opticalmodel_helium3
# Functions for helium-3 optical models
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
from opticalmodel_globals import *
import numpy as np

# Pang is the potential used for 3He
def Pang(A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H):
	# CHECK VALUE OF H
	CheckP(H)

	# CALCULATE TRIVIAL PARAMETERS
	[N, Q, E] = CalcTrivials(A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H)
	
	# Calculate more involved parameters
	A3 = A**(1.0/3.0)
	rc = 1.24*A3 + 0.12
	EC = 1.728*Z*2/rc
	ETA = float(N-Z)/float(A)
	VSI_ASYM = 35 + (34.2*ETA)
	
	# Calculate final parameters
	v = 118.3 + (-0.13*( Ebeam - EC ) )
	vi = 38.5/( 1 + np.exp( ( 156.1 - ( Ebeam - EC ) )/52.4 ) )
	vsi = VSI_ASYM/( 1 + np.exp( ( ( Ebeam - EC ) - 30.8 )/106.4 ) )
	if Ebeam < 85:
		vso = 1.7 + (-0.02*Ebeam)
	else:
		vso = 0
	vsoi = 0
	
	r0 = ( 1.3*A3 - 0.48 )/A3
	ri0 = ( 1.31*A3 - 0.13 )/A3
	rsi0 = ri0
	rso0 = ( 0.64*A3 +1.18 )/A3
	rsoi0 = 0.0
	
	a = 0.820
	ai = 0.840
	asi = 0.840
	aso = 0.130
	asoi = 0.0
	
	rc0 = rc/A3
	
	# Format final paramaters into a list of strings
	v_list = [v, vi, vsi, vso, vsoi]
	r_list = [r0, ri0, rsi0, rso0, rsoi0]
	a_list = [a, ai, asi, aso, asoi]
	string_list = MakeStringList(v_list,r_list,a_list,rc0)

	if PRINT == 1:
		PrintOpticalModel(string_list, "Pang 3He")
		PrintCalculatedQuantities(A,Z,E,Q)
		print(DIV)
		print("EC" + sep+ str(EC))
		print("ETA" + sep + str(ETA))
		print("VSI_ASYM" + sep + str(VSI_ASYM))
		print("rc" + sep + str(rc))
		print(DIV)
	return string_list
