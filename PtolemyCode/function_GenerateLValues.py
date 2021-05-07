# generateLValues(N,d) [FUNCTION]
# Generates a list of states for consideration for transfer reactions onto a target. N is the 
# relevant proton or neutron number that changes in the reaction. d specifies whether it is 
# addition of a particle [1] or removal [0]. This function will grab these states (based on the 
# shell model (see Krane Fig. 5.6, p. 123)) and separate the properties into the number of nodes 
# (starts from 0), the orbital angular momentum, 2*the total angular momentum, and JP (a string 
# e.g. "1/2+").
# =============================================================================================== #
# OTHER FUNCTIONS
# MakeList(n) - Makes lists of length n
# GetParity(L) - Returns parity of state for a given L
# PrintStates(node,J,L) - Prints each state in a list
# CombineQuantities(*objs) - Concatenate n objects into a list
# JLToJP(J,L) - Generates JP values from J and L
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# N -> the neutron number/proton number of the target for calculating 
# 	   occupancies
# d -> the direction in which to grab states. E.g. If N = 60, then 1 (up)
# 	   will give states from N = 50 to N = 126. 0 (down) will give states
# 	   from N = 20 to N = 50.
# 	   For nucleon addition, d = 1
#      For nucleon removal, d = 0
# =============================================================================================== #
# IMPORTANT TO NOTE
# As it stands, this will generate unique values of (L,node). However,this will give two L = 2 
# values if your nucleon occupies the shell between 126 and 184, since there is a 2d and 3d level. 
# This will need to be accounted for in your spreadsheet if you stray that high. BEWARE!
# =============================================================================================== #
import numpy as np
import sys
import copy

# GLOBAL VARIABLES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
magic_numbers = [0,2,8,20,28,50,82,126,184]
L_letters = ["s","p","d","f","g","h","i","j","k"]


# FUNCTION TO MAKE A LIST OF LISTS OF LENGTH N ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def MakeList(n):
	list = []
	for i in range(0,n):
		list.append([])
	return list

# FUNCTION TO RETURN THE PARITY OF A STATE GIVEN ITS ANGULAR MOMENTUM ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def GetParity(L):
	if L % 2 == 1:
		parity = "-"
	if L % 2 == 0:
		parity = "+"
	return parity

# PRINTS STATES GIVEN NODES, J AND L N.B. THESE ARE 1D LISTS! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def PrintStates(J,L,node):
	# Test how long the list is
	flag = 0
	try:
		len(J)
	except TypeError:
		flag = 1
	
	# Flag = 1 if there is only one value
	if flag == 0:
		for i in range(0,len(J)):
				print("".join([ str(node[i] + 1), str(L_letters[L[i]]),"[", str(J[i]), "/2", "]", GetParity(L[i])]))
	else:
		print("".join([ str(L_letters[L]),"[", str(J), "/2", "]", GetParity(L)]))
	return
	
	
# FUNCTION TO JOIN N LISTS (OR NOT AS THE CASE MAY BE) TOGETHER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def CombineQuantities(*objects):
	combination = []
	for i in objects:
		if type(i) == list:
			combination += i
		else:	
			combination.append(i)
	
	return combination

# FUNCTION TO CREATE JP VALUES FROM J AND L ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def JLToJP(J,L):
	# Determine how long J and L are
	flag = 0
	try:
		len(J)
	except TypeError:
		flag = 1
	
	# Now do the conversion
	if flag == 0:
		# Twas a list
		JP = MakeList(len(J))
		for i in range(0,len(J)):
			JP[i] = str(J[i]) + "/2" + GetParity(L[i])
	else:
		# Twas a singular quantity
		JP = str(J) + "/2" + GetParity(L)
	return JP

# FUNCTION TO REDUCE THE NUMBER OF STATES SO THAT EACH HAS A UNIQUE VALUE OF L ~~~~~~~~~~~~~~~~~~ #
#def ReduceStates( L_full, J_full, node_full, desired_duplicate_list ):
def ReduceStates( L_full, J_full, node_full, LMAX ):
	# Find out where there are duplicate [L,node] states
	indexArray = []
	for i in range( 0, len(L_full) ):
		if ( i < len(L_full) - 1 and L_full[i] == L_full[i+1] and node_full[i] != node_full[i+1] ) or L_full[i] > LMAX:
			indexArray.append(i)

	# Now delete those duplicate elements from J, L, and node
	[ L_final, J_final, node_final ] = [ copy.deepcopy( L_full ), copy.deepcopy( J_full ), copy.deepcopy( node_full ) ]
	for i in range(0,len(indexArray)):
		del L_final[ indexArray[i] ]
		del J_final[ indexArray[i] ]
		del node_final[ indexArray[i] ]
		
		# Need to lower the indices to delete right elements of these new arrays
		indexArray = [x-1 for x in indexArray]
		
	# Generate J and JP
	JP_final = JLToJP(J_final,L_final)
	
	# Print levels
	#PrintStates(J_full,L_full,node_full)
	#print("-----")
	#PrintStates(J_final,L_final,node_final)

	# Return the final quantities
	return L_final, J_final, JP_final, node_final
		

# FUNCTION TO GENERATE THE VALUES OF L, JP, AND NODES FOR THE PTOLEMY INPUT FILES ~~~~~~~~~~~~~~~ #
def GenerateSpinParity(opt_dct):
	Z = opt_dct["Z"]
	N = opt_dct["A"] - Z
	d = opt_dct["D"]
	LMAX = opt_dct["LMAX"]
	
	# N is the number of neutrons
	# Z is the number of protons
	# d is the direction (i.e. which shells to sample based on addition to or removal from residual nucleus)

	# Define a list of desired duplicate L's which should not be removed
	#desired_duplicate_list = [2]
	
	# 8 shell gaps - generate list of length 7 to store each list
	L = MakeList(8) # L is the angular momentum for each of the J-states
	J = MakeList(8)	# J is the total spin x 2 (so can simply append "/2" after it), from low energy to high
	node = MakeList(8) # node is the number of nodes in the wavefunction = principal quantum number - 1
	
	# Go between min and max
	# 000 -> 002 (0s1/2)
	L[0] = 0
	node[0] = 0
	
	# 002 -> 008 (0p3/2, 0p1/2)
	J[1] = [3,1]
	L[1] = [1,1]
	node[1] = [0,0]
	
	# 008 -> 020 (0d5/2, 1s1/2, 0d3/2)
	J[2] = [5,1,3]
	L[2] = [2,0,2]
	node[2] = [0,1,0]
	
	# 020 -> 028 (0f7/2)
	J[3] = 7
	L[3] = 3
	node[3] = 0

	# 028 -> 050 (1p3/2, 0f5/2, 0p1/2, 0g9/2)
	J[4] = [3,5,1,9]
	L[4] = [1,3,1,4]
	node[4] = [1,0,1,0]

	# 050 -> 082
	J[5] = [7,5,3,1,11]
	L[5] = [4,2,2,0,5]
	node[5] = [0,1,1,2,0]
	
	# 082 -> 126
	J[6] = [9,7,5,3,1,13]
	L[6] = [5,3,3,1,1,6]
	node[6] = [0,1,1,2,2,0]

	# 126 -> 184
	J[7] = [9,5,11,7,1,3,15]
	L[7] = [4,2,6,4,0,1,7]
	node[7] = [1,2,0,1,3,1,0]
	
	# Now work out which shells need to be sampled
	k_n, k_p = 0, 0
	
	# Calculate the upper bound of the shell of interest
	while N > magic_numbers[k_n]:
		k_n += 1
		
	while Z > magic_numbers[k_p]:
		k_p += 1
	
	# Now have upper bound of magic numbers. Rescale k's based on which states to look at (want to look at k and k-1)
	if d == 0:
		# This is a removal reaction, so look at current shell and shell below
		k_n -= 1
		k_p -= 1
	elif d == 1:
		# This is an addition reaction, so look at current shell and shell above
		pass
	else:
		sys.exit("Error. d can only have a value of 1 (add to target) or 0 (lose from target).")

	# Now choose depending on nuclear configuration
	# EVEN-EVEN
	if N % 2 == 0 and Z % 2 == 0:
		# The nucleus has a total angular momentum of 0 and even parity.
		L_final = [0]
		J_final = [0]
		
		# Calculate the combined node states
		if k_n == 0:
			node_comb_n = node[k_n]
		else:
			node_comb_n = CombineQuantities( node[k_n], node[k_n-1] )
		
		if k_p == 0:
			node_comb_p = node[k_p]
		else:
			node_comb_p = CombineQuantities( node[k_p], node[k_p-1] )
			
		# Sort the node states - just choose the maximum node possible.
		node_final = [max( node_comb_n + node_comb_p )]
		JP_final = ["0+"]

		return L_final, J_final, JP_final, node_final
		
	# ODD Z, N, OR BOTH
	else:
		# Calculate neutron levels (if N is odd)
		if N % 2 == 1:
			if k_n == 0:
				L_comb_n = L[k_n]
				J_comb_n = J[k_n]
				node_comb_n = node[k_n]
			else:
				#L_comb_n = CombineQuantities( L[k_n], L[k_n-1] )				# High A NDBD work
				#J_comb_n = CombineQuantities( J[k_n], J[k_n-1] )
				#node_comb_n = CombineQuantities( node[k_n], node[k_n-1] )
				L_comb_n = CombineQuantities( L[k_n+1], L[k_n], L[k_n-1] )		# Low A ISS work
				J_comb_n = CombineQuantities( J[k_n+1], J[k_n], J[k_n-1] )
				node_comb_n = CombineQuantities( node[k_n+1], node[k_n], node[k_n-1] )
				

			# Now zip together the states
			Z_n = zip( L_comb_n, J_comb_n, node_comb_n )
			
			# Sort the states
			L_full_n = [ sorted(Z_n)[i][0] for i in range( 0, len(Z_n) ) ]
			J_full_n = [ sorted(Z_n)[i][1] for i in range( 0, len(Z_n) ) ]
			node_full_n = [ sorted(Z_n)[i][2] for i in range( 0, len(Z_n) ) ]

			# Reduce the states to remove duplicates
			L_final_n, J_final_n, JP_final_n, node_final_n = ReduceStates( L_full_n, J_full_n, node_full_n, LMAX )

			# Print levels
			#PrintStates( J_final_n, L_final_n, node_final_n )
			
		# Calculate proton levels (if Z is odd)
		if Z % 2 == 1:
			if k_p == 0:
				L_comb_p = L[k_p]
				J_comb_p = J[k_p]
				node_comb_p = node[k_p]
			else:
				L_comb_p = CombineQuantities( L[k_p], L[k_p-1] )
				J_comb_p = CombineQuantities( J[k_p], J[k_p-1] )
				node_comb_p = CombineQuantities( node[k_p], node[k_p-1] )
	
			# Now zip together the states
			Z_p = zip( L_comb_p, J_comb_p, node_comb_p )

			# Sort the states
			L_full_p = [ sorted(Z_p)[i][0] for i in range( 0, len(Z_p) ) ]
			J_full_p = [ sorted(Z_p)[i][1] for i in range( 0, len(Z_p) ) ]
			node_full_p = [ sorted(Z_p)[i][2] for i in range( 0, len(Z_p) ) ]

			# Reduce the states to remove duplicates
			L_final_p, J_final_p, JP_final_p, node_final_p = ReduceStates( L_full_p, J_full_p, node_full_p, LMAX )

			# Print levels
			#PrintStates( J_final_p, L_final_p, node_final_p )


		# ODD-EVEN or EVEN-ODD
		if Z % 2 == 1 and N % 2 == 0:
			return L_final_p, J_final_p, JP_final_p, node_final_p

		elif N % 2 == 1 and Z % 2 == 0:
			return L_final_n, J_final_n, JP_final_n, node_final_n

		else:
			# ODD-ODD -> have to sum up each state in a quantum mechanical way to create a new state
			return 0, 0, 0, 0
			# TODO Finish me! (if you need to)


# RETURN THE INFORMATION FOR A GIVEN VALUE OF L ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def GetNodes(N, Z, d, L):
	# Determine how long L is
	try:
		len(L)
	except TypeError:
		L = [L]

	# Generate all the levels for a given number of nucleons and the shells that are being observed
	L_full, J_full, node_full = GenerateSpinParity(N, Z, d)

	# Now reduce the number of states to only the desired L values
	L_final, J_final, node_final = [],[], []
	for i in range(0, len(L_full)):
		for j in range(0,len(L)):
			if L_full[i] == L[j]:
				L_final.append(L_full[i])
				J_final.append(J_full[i])
				node_final.append(node_full[i])
	
	# Print levels	
	#PrintStates(J_final,L_final,node_final)

	# Generate J and JP
	JP_final = JLToJP(J_final,L_final)
	
	return L_final, J_final, JP_final, node_final


