# generateLValues(N,d) [FUNCTION]
# Generates a list of states for consideration for transfer reactions onto a target. N is the 
# relevant proton or neutron number that changes in the reaction. d specifies whether it is 
# addition of a particle [1] or removal [0]. This function will grab these states (based on the 
# shell model (see Krane Fig. 5.6, p. 123)) and separate the properties into the number of nodes 
# (starts from 0), the orbital angular momentum, 2*the total angular momentum, and JP (a string 
# e.g. "1/2+").
# =============================================================================================== #
# OTHER FUNCTIONS
# makeList(n) - Makes lists of length n
# returnParity(L) - Returns parity of state for a given L
# printStates(node,J,L) - Prints each state in a list
# combineQuantities(c1,c2) - Concatenate two things into a list
# JLToJP(J,L) - Generates JP values from J and L
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# LAST EDITED: 08/10/18
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

# Global variables! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
magicNumbers = [0,2,8,20,28,50,82,126,184]
L_Letters = ["s","p","d","f","g","h","i","j","k"]

# Function to make a list of lists of length n ~~~~~~~~~~~~~~~~~~~~~~~~~ #
def makeList(n):
	list = []
	for i in range(0,n):
		list.append([])
	return list

# Function to return the parity of a state given its angular momentum ~~ #
def returnParity(L):
	if (-1)**L == 1:
		parity = "+"
	if (-1)**L == -1:
		parity = "-"
	return parity

# Prints states given nodes, J and L N.B. These are 1D lists! ~~~~~~~~~~ #
def printStates(J,L,node):
	# Test how long the list is
	flag = 0
	try:
		len(J)
	except TypeError:
		flag = 1
	
	# Flag = 1 if there is only one value
	if flag == 0:
		for i in range(0,len(J)):
				print("".join([ str(node[i] + 1), str(L_Letters[L[i]]),"[", str(J[i]), "/2", "]", returnParity(L[i])]))
	else:
		print("".join([ str(L_Letters[L]),"[", str(J), "/2", "]", returnParity(L)]))
	return
	
	
# Function to join two lists (or not as the case may be) together ~~~~~~ #
def combineQuantities(c1,c2):
	if type(c1) == list and type(c2) == list:
		combination = c1 + c2
	elif type(c1) == list and type(c2) != list:
		combination = c1 + [c2]
	elif type(c1) != list and type(c2) == list:
		combination = [c1] + c2
	else:
		combination = [c1] + [c2]
	return combination

# Function to create JP values from J and L ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
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
		JP = makeList(len(J))
		for i in range(0,len(J)):
			JP[i] = str(J[i]) + "/2" + returnParity(L[i])
	else:
		# Twas a singular quantity
		JP = str(J) + "/2" + returnParity(L)
	return JP
		

# Function to generate the values of L, JP, and nodes for the ptolemy input files.
def generateLValues(N,d):
	# 8 Gaps - generate list of length 7 to store each list
	L = makeList(8) # L is the angular momentum for each of the J-states
	J = makeList(8)	# J is the total spin x 2 (so can simply append "/2" after it), from low energy to high
	node = makeList(8) # node is the number of nodes in the wavefunction = principal quantum number - 1
	
	# Go between min and max
	# 000 -> 002
	L[0] = 0
	node[0] = 0
	
	# 002 -> 008
	J[1] = [3,1]
	L[1] = [1,1]
	node[1] = [0,0]
	
	# 008 -> 020
	J[2] = [5,1,3]
	L[2] = [2,0,2]
	node[2] = [0,1,0]
	
	# 020 -> 028
	J[3] = 7
	L[3] = 3
	node[3] = 0

	# 028 -> 050
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
	
	# Now select the levels to test as a single array - define value to test magic numbers
	k = 0
	# Lose particle from target. Therefore look at hole states below magic number after N.
	while N > magicNumbers[k]:
		k += 1
	# Now have magic number above N. 
	if d == 0:
		# Look at previous 2 states (k-1 and k-2)
		pass
	elif d == 1:
		# Look at states above and below (k and k-1) or rescale for reusing code
		k += 1
	else:
		sys.exit("Error. d can only have a value of 1 (add to target) or 0 (lose from target).")

	# Now that k is scaled, calculate initial and final values
	if k > 1:
		# Combine lists for an output of all states that need to be considered
		L_comb = combineQuantities(L[k-2], L[k-1])
		J_comb = combineQuantities(J[k-2], J[k-1])
		node_comb = combineQuantities(node[k-2], node[k-1])
	elif k == 1:
		# Fewer states here, so only do the possible states
		L_comb = L[k-1]
		J_comb = J[k-1]
		node_comb = node[k-1]
	else:
		if d == 0:
			# This is when there are too few particles to get states
			sys.exit("Error. Cannot lose particles from the target when there aren't any particles to give away!")
		elif d == 1:
			# This is when we run out of particles to add
			sys.exit("Error. Mass is too high for me to handle!")
	
	# Now sort states in terms of L - zip together the J_states and nodes to L
	Z = zip(L_comb,J_comb,node_comb)
	
	# Sort the states
	L_full = [sorted(Z)[i][0] for i in range(0,len(Z))]
	J_full = [sorted(Z)[i][1] for i in range(0,len(Z))]
	node_full = [sorted(Z)[i][2] for i in range(0,len(Z))]
	
	# Now reduce states - want unique L's and nodes
	indexArray = []
	
	# Find out where there are duplicate [L,node] states
	for i in range(0,len(L_full)-1):
		if [ L_full[i], node_full[i] ] == [ L_full[i+1], node_full[i+1] ]:
			indexArray.append(i)
	
	# Print levels
	#printStates(J_full,L_full,node_full)
	
	# Return the final quantities
	return L_full, J_full, node_full

# Return a unique value of l ----------------------------------------------------------------------
def getReducedStates(N,d):
	# Get all the states
	L_final, J_final, node_final = generateLValues(N,d)

	# Find out where there are duplicate [L,node] states
	indexArray = []
	for i in range(0,len(L_full)-1):
		if [ L_final[i], node_final[i] ] == [ L_final[i+1], node_final[i+1] ]:
			indexArray.append(i)
	
	# Now delete those duplicate elements from J, L, and node
	print(indexArray)
	print("Banana")
	for i in range(0,len(indexArray)):
		del L_final[ indexArray[i] ]
		del J_final[ indexArray[i] ]
		del node_final[ indexArray[i] ]
		
		# Need to lower the indices to delete right elements of these new arrays
		indexArray = [x-1 for x in indexArray]
		
	# Generate J and JP
	JP_final = JLToJP(J_final,L_final)
	
	# Print levels
	#printStates(J_final,L_final,node_final)
	
	# Return the final quantities
	return L_final, J_final, JP_final, node_final

# Return the information for a given value of l ---------------------------------------------------
def getNodes(N,d,L):
	# Determine how long L is
	try:
		len(L)
	except TypeError:
		L = [L]

	# Generate all the levels for a given number of nucleons and the shells that are being observed
	L_full, J_full, node_full = generateLValues(N,d)

	# Now reduce the number of states to only the desired L values
	L_final, J_final, node_final = [],[], []
	for i in range(0, len(L_full)):
		for j in range(0,len(L)):
			if L_full[i] == L[j]:
				L_final.append(L_full[i])
				J_final.append(J_full[i])
				node_final.append(node_full[i])
	
	# Print levels	
	#printStates(J_final,L_final,node_final)

	# Generate J and JP
	JP_final = JLToJP(J_final,L_final)
	
	return L_final, J_final, JP_final, node_final

# Return a unique value of l ----------------------------------------------------------------------
def getSpecificStates(N,d):
	# Get all the states
	L_final, J_final, node_final = generateLValues(N,d)
	
	# Find out where there are duplicate [L,node] states
	indexArray = []
	for i in range(0,len(L_final)-1):
		if [ L_final[i], node_final[i] ] == [ L_final[i+1], node_final[i+1] ] and L_final[i] != 2:
			indexArray.append(i)

	# Now delete those duplicate elements from J, L, and node
	for i in range(0,len(indexArray)):
		del L_final[ indexArray[i] ]
		del J_final[ indexArray[i] ]
		del node_final[ indexArray[i] ]
		
		# Need to lower the indices to delete right elements of these new arrays
		indexArray = [x-1 for x in indexArray]
		
	# Generate J and JP
	JP_final = JLToJP(J_final,L_final)
	
	# Print levels
	#printStates(J_final,L_final,node_final)
	
	# Return the final quantities
	return L_final, J_final, JP_final, node_final


