#!/bin/bash
# Runs ptolemyBash, but for everything
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
PTOLEMY_SCRIPT_DIR="/home/ptmac/Documents/SPECTRUM_ANALYSIS_CODE/PtolemyCode/"
deuteron_array=( "AC" "B" "DNR" "DR" "HSS" "LH" "PP")
proton_array=( "BG" "KD" "M" "P" "V" )
# TODO 3He and 4He

usage(){
	cat << EOF
ptolemy-mega-bash.sh template.sh reaction-type[dp,pd,ha,...]
template.sh must include ROOT_FILE_DIR, PARAMETER_DIR, INPUT_FILE_DIR, OUTPUT_FILE_DIR, and PTOLEMY_OPTION_FILE, but not the input or output potentials.
EOF
}

# Assign which arrays to use - ensure length of reaction is 2
if [[ ${#2} -eq 2 ]]
then
	# Assign incoming array
	case ${2:0:1} in
		d)
			ARR1=("${deuteron_array[@]}")
		;;
		p)
			ARR1=("${proton_array[@]}")
		;;
		h)
			echo "h"
		;;
		a)
			echo "a"
		;;
		*)
			echo "${1} is not an allowed option!"
			exit 1
		;;
	esac
	# Assign outgoing array
	case ${2:1:2} in
		d)
			ARR2=("${deuteron_array[@]}")
		;;
		p)
			ARR2=("${proton_array[@]}")
		;;
		h)
			echo "h"
		;;
		a)
			echo "a"
		;;
		*)
			echo "${1} is not an allowed option!"
			exit 1
		;;
	esac

	# Now loop over the two arrays and run some ptolemy!
	for i in "${ARR1[@]}"
	do
		POTENTIAL_IN="${i}"
		export POTENTIAL_IN
		
		for j in "${ARR2[@]}"
		do
			POTENTIAL_OUT="${j}"
			export POTENTIAL_OUT

			# Now run the ptolemyBash script
			if [ -e "${1}" ]
			then
				"${PTOLEMY_SCRIPT_DIR}/"ptolemyBash.sh "${1}"
			else
				usage
				exit 1
			fi
		done
	done
else
	echo "Reaction ${2} not allowed - it must be two characters long. p = proton, d = deuteron, h = 3He, a = 4He --> combine two!"
	exit 1
fi


