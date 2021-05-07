# opticalmodel_globals
# Contains global variables for the optical model calculations
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# GLOBAL CONSTANTS
import numpy as np
amu = 931.494	# amu in MeV/c^2
PRINT = 0
sep = "\t"
div = "--------------------------------------------------"
DIV = "=================================================="
# ----------------------------------------------------------------------------------------------- #
# Print out the calculated quantities in the string list
def PrintOpticalModel(string_list, name):
	print(DIV)
	print(name + " potential:")
	print(div)
	for i in range(0,len(string_list)):
			print(string_list[i])

# ----------------------------------------------------------------------------------------------- #
def PrintCalculatedQuantities(A,Z,E,Q):
	print(div)
	print("A" + sep + str(A))
	print("Z" + sep + str(Z))
	print("E" + sep + str(E))
	print("Q" + sep + str(Q))

# ----------------------------------------------------------------------------------------------- #
# Calculate Q value
def CalcQ( M_Target, M_Projectile, M_Ejectile, M_Product ):
	return ( (M_Target + M_Projectile) - (M_Ejectile + M_Product) )*amu

# ----------------------------------------------------------------------------------------------- #
# Calculate separation energy for neutron or proton
def CalcSepEn( M_Light, M_Heavy, reaction_type ):
	# Neutron separation energy
	if reaction_type in [ "dp", "pd", "ha", "ah" ]:
		return 939.5654133 + amu*(M_Light - M_Heavy)

	# Proton separation energy
	elif reaction_type in [ "th", "ht", "at", "ta" ]:
		return 938.2720813 + amu*(M_Light - M_Heavy)
	
	# No separation energy
	else:
		return -1.0

		


# ----------------------------------------------------------------------------------------------- #
# Calculate trivial quantities
def CalcTrivials(A, Z, Ebeam, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, H):
	# Number of neutrons
	N = A - Z
	
	# Calculate Q value
	Q = CalcQ( M_Target, M_Projectile, M_Ejectile, M_Product )
	
	# Calculate energy
	if H == 0:
		E = Ebeam
	elif H == 1:
		E = Ebeam + Q - Ex

	# Return list
	triv_list = [N, Q, E]

	return triv_list

# ----------------------------------------------------------------------------------------------- #
# Make the string list from the calculated quantities
def MakeStringList(v,r,a,rc0):
	stringList = []
	stringList.append("v = " +    str(round(v[0],3)) + " r0 = " +    str(round(r[0],3)) + " a = " +    str(round(a[0],3)))
	stringList.append("vi = " +   str(round(v[1],3)) + " ri0 = " +   str(round(r[1],3)) + " ai = " +   str(round(a[1],3)))
	stringList.append("vsi = " +  str(round(v[2],3)) + " rsi0 = " +  str(round(r[2],3)) + " asi = " +  str(round(a[2],3)))
	stringList.append("vso = " +  str(round(v[3],3)) + " rso0 = " +  str(round(r[3],3)) + " aso = " +  str(round(a[3],3)))
	stringList.append("vsoi = " + str(round(v[4],3)) + " rsoi0 = " + str(round(r[4],3)) + " asoi = " + str(round(a[4],3)) + " rc0 = " + str(round(rc0,3)))
	return stringList

# ----------------------------------------------------------------------------------------------- #
def CheckP(p):
	if p != 0 and p != 1:
		raise ValueError("p must have a value of 0 or 1")

# ----------------------------------------------------------------------------------------------- #
# DWUCK STUFF!!!!
# Define a function to write a block of 8 characters padded with spaces at the end
def WriteBlock(string, n = 8):
	if len(string) > n:
		print("Not allowed!")
		return " "*n
	else:
		return string + " "*(n - len(string))

# Return + or - based on the sign of the number
def GetSignChar(num):
	if num < 0: return "-"
	elif num >= 0: return "+"
	else: return "?"

# Return a number rounded to a particular length
def RoundNumToLength(num,length):
	if num == 0:
		power = 2
	else:
		power = max( np.ceil( np.log10(abs(num)) ), 2 )
	
	return format(num, "0" + str(length) + "." + str(int(length - power - 1)) + "f" )
	
# Combine these to write a block for specifying DWUCK optical model input
def WriteDWUCKOMPar(par):
	return WriteBlock(GetSignChar(par) + RoundNumToLength(abs(par),6) )
	
def WriteDWUCKSmallNum(par):
	return WriteBlock( format(par, "4.1f" ) )
	
def WriteDWUCKSignSmallNum(par):
	return WriteBlock( GetSignChar(par) + format(abs(par), "04.1f" ) )	
		
# Define the DWUCK optical model input parameters
def WriteDWUCKOMBlock(v,r,a,rc0):
	string_list = []
	string_list.append( WriteBlock("+01.") + WriteDWUCKOMPar(-v[0]) + WriteDWUCKOMPar(r[0]) + WriteDWUCKOMPar(a[0]) + WriteBlock("") + WriteDWUCKOMPar(-v[1]) + WriteDWUCKOMPar(r[1]) + WriteDWUCKOMPar(a[1]) )
	string_list.append( WriteBlock("+02.") + WriteDWUCKOMPar(0.00) + WriteDWUCKOMPar(0.00) + WriteDWUCKOMPar(0.00) + WriteBlock("") + WriteDWUCKOMPar(4*v[2]) + WriteDWUCKOMPar(r[2]) + WriteDWUCKOMPar(a[2]) )
	string_list.append( WriteBlock("-04.") + WriteDWUCKOMPar(-4*v[3]) + WriteDWUCKOMPar(r[3]) + WriteDWUCKOMPar(a[3]) + WriteBlock("") + WriteDWUCKOMPar(-4*v[4]) + WriteDWUCKOMPar(r[4]) + WriteDWUCKOMPar(a[4]) )
	string_list.append( WriteBlock( format( rc0, "07.3f" ) ) )
	return string_list

































