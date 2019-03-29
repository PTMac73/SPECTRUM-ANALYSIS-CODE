# functionPtolemyParameters
# Calculates the Ptolemy parameters for a number of initial target parameters
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# INITIAL PARAMETERS
# A ------------- Mass number of the target
# Z ------------- Charge of the target
# Ebeam --------- Energy of the beam in the lab frame in MeV
# Ex ------------ Excitation energy in MeV
# M_Target ------ Mass of the target (a.m.u.)
# M_Projectile -- Mass of the projectile (a.m.u.)
# M_Ejectile ---- Mass of the ejectile (a.m.u.)
# M_Product ----- Mass of the product (a.m.u.)
# p ------------- A boolean that determines whether it is initial (0) or final (1) in the reaction
# 
# N.B. All masses are to be in a.m.u.
# =============================================================================================== #
# ALLOWED POTENTIALS
# Protons
#  * Koning and Delaroche (KD)
#  * Perey (P)
# 
# Deuterons
#  * An and Cai (AC)
#  * Perey and Perey (PP)
#  * Lohr and Haeberli (LH)
#
# Helium-3
#  * Pang (P)
#
# Alpha
#  * Bassani and Picard (BP)
#
# =============================================================================================== #
import numpy as np
from opticalmodel_protons import *
from opticalmodel_deuterons import *
from opticalmodel_helium3 import *
from opticalmodel_alpha import *
from opticalmodel_globals import *


# FUNCTIONS ===================================================================================== #
# obtainPTList generates the input parameters for Ptolemy based on a given reaction
def obtainPTList(reaction, A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, optical_model_in, optical_model_out):
	# Change the parameters based on the reaction
	reaction_par = [A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product]
	# (d,p) reaction -----------------------------------------------------
	if reaction == "dp":
		# N.B. The target mass increases here
		a = potentialSelect("d", optical_model_in, 0, reaction_par)
		b = potentialSelect("p", optical_model_out, 1, reaction_par)

	# (p,d) reaction -----------------------------------------------------		
	elif reaction == "pd":
		# N.B. The target mass decreases here	
		a = potentialSelect("p", optical_model_in, 0, reaction_par)
		b = potentialSelect("d", optical_model_out, -1, reaction_par)

	# (d,d) reaction -----------------------------------------------------
	elif reaction == "dd":
		# N.B. The target mass stays the same here
		a = potentialSelect("d", optical_model_in, 0, reaction_par)
		b = potentialSelect("d", optical_model_out, 0, reaction_par)

	# (h,a) reaction -----------------------------------------------------		
	elif reaction == "ha":
		# N.B. The target mass decreases here
		a = potentialSelect("h", optical_model_in, 0, reaction_par)
		b = potentialSelect("a", optical_model_out, -1, reaction_par)
	return a + b


# Select the optical model potential based on the particle and the optical model input
def potentialSelect(particle, optical_model, massDiff, reaction_par):
	A = reaction_par[0]
	Z = reaction_par[1]
	Ebeam = reaction_par[2]
	Ex = reaction_par[3]
	M_Target = reaction_par[4]
	M_Projectile = reaction_par[5]
	M_Ejectile = reaction_par[6]
	M_Product = reaction_par[7]

	if massDiff == 0:
		H = 0
	else:
		H = 1

	# DEUTERONS
	if particle == "d":
		if optical_model == "AC":
			return AnCai(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H)

		elif optical_model == "PP":
			return PereyPerey(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H)

		elif optical_model == "LH":
			return LohrHaeberli(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H)
		
		else:
			raise ValueError("Not an allowed deuteron potential.")

	# PROTONS
	elif particle == "p":
		if optical_model == "KD":
			return KoningDelaroche(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H)

		elif optical_model == "P":
			return Perey(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H)
		
		else:
			raise ValueError("Not an allowed proton potential.")

	
	# HELIUM-3
	elif particle == "h":
		if optical_model == "P":
			return Pang(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H)
		
		else:
			raise ValueError("Not an allowed 3He potential.")

	# ALPHA
	elif particle == "a":
		if optical_model == "BP":
			return BassaniPicard(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H)
		
		else:
			raise ValueError("Not an allowed alpha potential.")

	else:
		raise ValueError("Not an allowed particle.")



obtainPTList("pd", 124, 52, 22, 0, 123.9028179, 1.00782503224, 2.01410177811, 122.9042698, "P", "LH")













