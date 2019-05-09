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
#  * Becchetti and Greenlees (BG)
#  * Koning and Delaroche (KD)
#  * Menet (M)
#  * Perey (P)
#  * Varner (V)
# 
# Deuterons
#  * An and Cai (AC)
#  * Bojowald (B)
#  * Daehnick (relativistic) (DR)
#  * Daehnick (non-relativistic) (DNR)
#  * Han, Shi, and Shen (HSS)
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
# ObtainPTList generates the input parameters for Ptolemy based on a given reaction
def ObtainPTList( Ex, optical_model_in, optical_model_out, opt_dct ):
	# Change the parameters based on the reaction
	reaction_par = [ opt_dct["A"], opt_dct["Z"], opt_dct["ELAB"], Ex, opt_dct["M_Target"], opt_dct["M_Projectile"], opt_dct["M_Ejectile"], opt_dct["M_Product"] ]

	# Define a flag if reaction is elastic
	flag_elastic = 0

	# (d,p) reaction -----------------------------------------------------
	if opt_dct["reaction_type"] == "dp":
		# N.B. The target mass increases here
		a = PotentialSelect("d", optical_model_in, 0, reaction_par)
		b = PotentialSelect("p", optical_model_out, 1, reaction_par)

	# (p,d) reaction -----------------------------------------------------		
	elif opt_dct["reaction_type"] == "pd":
		# N.B. The target mass decreases here	
		a = PotentialSelect("p", optical_model_in, 0, reaction_par)
		b = PotentialSelect("d", optical_model_out, -1, reaction_par)

	# (d,d) reaction -----------------------------------------------------
	elif opt_dct["reaction_type"] == "dd":
		# N.B. The target mass stays the same here
		# THIS IS ELASTIC SCATTERING
		a = PotentialSelect("d", optical_model_in, 0, reaction_par)
		flag_elastic = 1

	# (h,a) reaction -----------------------------------------------------		
	elif opt_dct["reaction_type"] == "ha":
		# N.B. The target mass decreases here
		a = PotentialSelect("h", optical_model_in, 0, reaction_par)
		b = PotentialSelect("a", optical_model_out, -1, reaction_par)

	# Include the model names
	name_list = ModelNames( opt_dct["reaction_type"] )
	
	# Now combine the two lists of parameters
	if flag_elastic == 0:
		s = []
		for i in range(0, len(a)):
			for j in range(0, len(b)):
				s.append( a[i] + b[j] )
	else:
		s = a

	# Calculate the items for consideration in the list of optical models given
	omn_list = GetModelNumberList( opt_dct["reaction_type"], optical_model_in, optical_model_out )

	return s, name_list, omn_list


# Select the optical model potential based on the particle and the optical model input
def PotentialSelect(particle, optical_model, massDiff, reaction_par):
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
		d_list = []
	
		if optical_model == "AC":
			d_list.append( AnCai(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )

		elif optical_model == "PP":
			d_list.append( PereyPerey(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )

		elif optical_model == "LH":
			d_list.append( LohrHaeberli(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )

		elif optical_model == "HSS":
			d_list.append( HanShiShen(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )

		elif optical_model == "B":
			d_list.append( Bojowald(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )

		elif optical_model == "DNR":
			d_list.append( DaehnickNR(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )

		elif optical_model == "DR":
			d_list.append( DaehnickR(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )

		elif optical_model == "ALL-D":
			d_list.append( HanShiShen(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
			d_list.append( AnCai(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
			d_list.append( Bojowald(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
			d_list.append( DaehnickR(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
			d_list.append( DaehnickNR(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
			d_list.append( LohrHaeberli(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
			d_list.append( PereyPerey(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )

		else:
			raise ValueError("Not an allowed deuteron potential.")

		return d_list


	

	# PROTONS
	elif particle == "p":
		p_list = []

		if optical_model == "KD":
			p_list.append( KoningDelaroche(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )

		elif optical_model == "P":
			p_list.append( Perey(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )

		elif optical_model == "M":
			p_list.append( Menet(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )

		elif optical_model == "V":
			p_list.append( Varner(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )

		elif optical_model == "BG":
			p_list.append( BecchettiGreenlees(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
		
		elif optical_model == "ALL-P":
			p_list.append( KoningDelaroche(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
			p_list.append( Varner(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
			p_list.append( Menet(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
			p_list.append( BecchettiGreenlees(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
			p_list.append( Perey(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
			
		else:
			raise ValueError("Not an allowed proton potential.")

		return p_list

	
	# HELIUM-3
	elif particle == "h":
		h_list = []
		if optical_model == "P":
			h_list.append( Pang(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
		
		else:
			raise ValueError("Not an allowed 3He potential.")

		return h_list

	# ALPHA
	elif particle == "a":
		a_list = []
		if optical_model == "BP":
			a_list.append( BassaniPicard(A + massDiff, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H) )
		
		else:
			raise ValueError("Not an allowed alpha potential.")

		return a_list

	else:
		raise ValueError("Not an allowed particle.")


# Returns a list of the model names based on which one was used
def ModelNames( reaction_type ):
	# Returns the names of the two model potentials combined
	p = ProtonModelNumber()
	d = DeuteronModelNumber()

	# TODO - WRITE THESE THINGS
	h = []
	a = []
	name_list = []

	# Select the right potentials
	particle = []
	for i in range(0, len(reaction_type)):
		if "p" == reaction_type[i]:
			particle.append(p)
		elif "d" == reaction_type[i]:
			particle.append(d)
		elif "h" == reaction_type[i]:
			particle.append(h)
		elif "a" == reaction_type[i]:
			particle.append(a)

	# Check size of particle is correct
	if len(particle) != 2:
		print("TOO MANY MODELS!!")
		exit(1)

	# Check if same particle
	if particle[0] == particle[1]:
		flag_same_particle = 1
	else:
		flag_same_particle = 0


	# Generate the name list, but constrain it to the same models if elastic scattering
	for i in range(0, len(particle[0]) ):
		for j in range(0, len(particle[1]) ):
			if (flag_same_particle == 1 and i == j ) or flag_same_particle == 0:
				name_list.append( particle[0][i] + "_" + particle[1][j] )
	
	return name_list




def GetModelNumberList( reaction_type, optical_model_in, optical_model_out ):
	# Define the dictionaries to use
	flag_elastic = 0
	if reaction_type == "dp":
		dct_1 = deuteron_dct
		dct_2 = proton_dct	

	elif reaction_type == "pd":
		dct_1 = proton_dct
		dct_2 = deuteron_dct

	elif reaction_type == "dd":
		dct_1 = deuteron_dct
		dct_2 = deuteron_dct
		flag_elastic = 1
	
	else:
		raise ValueError("Not an allowed reaction type.")
		exit(1)

	# Now create the list
	omn_list = []
	if flag_elastic == 0:
		for i in range( dct_1[ optical_model_in ][0], dct_1[ optical_model_in ][1] ):
			for j in range( dct_2[ optical_model_out ][0], dct_2[ optical_model_out ][1] ):
				omn_list.append( dct_2["len"]*i + j )
	else:
		for i in range( dct_1[ optical_model_in ][0], dct_1[ optical_model_in ][1] ):
			omn_list.append(i)

		

	return omn_list












































