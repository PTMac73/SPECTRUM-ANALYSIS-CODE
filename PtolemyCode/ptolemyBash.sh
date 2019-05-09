#!/bin/bash
# ptolemyBash.sh
# Does the full Ptolemy analysis and outputs the relevant text files
# N.B. This is the centralised software - send files to this and it should save them in the 
# relevant folder
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# FORMAT
# To execute the script, you must include the global variables file
# ./ptolemyBash.sh "~/Documents/03. Munich Data Analysis (Feb 2018)/Ptolemy Input Files (124Te)/globalVariables.sh" for example
# =============================================================================================== #
# SWITCHES
SWITCH_DELETE_FILE=1
SWITCH_WRITE_INPUT=1
SWITCH_RUN_PTOLEMY=0
SWITCH_CLEAN=0
SWITCH_CSV_ARRAY=0

# FIXED DIRECTORIES
PTOLEMY_DIR=~/Software/Ptolemy/
PTOLEMY_ANALYSIS_DIR="/home/ptmac/Documents/SPECTRUM_ANALYSIS_CODE/PtolemyCode/"

# Check for help option
usage() {
	echo "Usage: "
	echo "  ptolemyBash.sh -h | --help"
	echo "  ptolemyBash.sh <input_shell.sh>"
	echo ""
}

for i in $@
do
	if [[ "$i" == "-h" ]] || [[ "$i" == "--help" ]]
	then
		usage
		cat << EOH
Options:
  h | --help                 Opens the help dialogue
  <input_shell.sh>           Runs the ptolemyBash script with the given input 
                               parameters (defined later).

ptolemyBash controls the creation of Ptolemy input and output files. This is
done through the <input_shell.sh> script, and some other pre-defined scripts.
The stages of the script can be controlled with switches at the top, and are
detailed below:
  (1) DELETE all previous input and ouput files.
  (2) WRITE new input files for the given input.
  (3) RUN Ptolemy on all of the input files, generating output files.
  (4) CLEAN all the new ouput files so that all of the desired numbers are
      extracted.
  (5) COMBINE all of the output files into a .csv file to be pasted into a 
      spreadsheet.

The <input_shell.sh> defines a number of global variables, which are then used
in the main script. It also defines the location of a list of excitation 
energies, as well as directories and the reaction parameters used in Python. The
global variables are:
  POTENTIAL_IN               The abbreviation for the input potential. These are
                               detailed in the opticalmodel_X.py files.
  POTENTIAL_OUT              The abbreviation for the output potential. These 
                               are detailed in the opticalmodel_X.py files.
  PARAMETER_DIR              This is the directory where the energy list and the Python option
                               file are stored.
  INPUT_FILE_DIR             This is the directory where the Ptolemy input files
                               are stored.
  OUTPUT_FILE_DIR            This is the directory where the Ptolemy output 
                               files are stored.
  PTOLEMY_OPTION_FILE        Location of the Python reaction input parameter 
                               file.

These variables are then made global by using the "export" command.

EOH
		exit 0
	fi
done

# LOAD VARIABLE DIRECTORIES
if [ -e "${1}" ]
then
	. "${1}"
else
	usage
	exit 1
fi

FOLDER_LENGTH="${#INPUT_FILE_DIR}"
clear
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Deletes all the files in a given folder (if they exist) and outputs a
# message to the console
delete_file_type(){
	# The first argument is the file type (e.g. ".txt"), the second argument
	# is the directory
	flag=0
	for file in "$2"*"$1"
	do
		if [[ "$file" != "$2*$1" ]]
		then
			rm "${file}"
			flag=1
		fi
	done
	
	# Send message
	if [[ $flag == 1 ]]
	then
		# Convert first argument to uppercase and remove first character
		upperFile=${1^^}
		echo "Deleted ${upperFile:1} files"
	fi
}

# Check if a folder exists, and make it if it doesn't
check_folder_exists(){
	if [ ! -d ${1} ]
	then
		echo -e "${1##*Data/} does not exist. Making directory."
		mkdir ${1}
	fi
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CHECK DIRECTORIES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
check_folder_exists ${INPUT_FILE_DIR}
check_folder_exists ${OUTPUT_FILE_DIR}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DELETE FILES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if [ $SWITCH_DELETE_FILE == 1 ]
then
	delete_file_type .in "${INPUT_FILE_DIR}"
	delete_file_type .out "${OUTPUT_FILE_DIR}"
	delete_file_type .out-clean "${OUTPUT_FILE_DIR}"
fi
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CREATE FILES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Run ptolemyMaster.py -> writes input file
if [ $SWITCH_WRITE_INPUT == 1 ]
then
	python "${PTOLEMY_ANALYSIS_DIR}WritePtolemyInputFile.py" "${PTOLEMY_OPTION_FILE}"
fi
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ RUN PTOLEMY ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Run ptolemy for each of the input files and store in the right folder
if [ $SWITCH_RUN_PTOLEMY == 1 ]
then
	for FILE in "${INPUT_FILE_DIR}"*.in ; do
		# Get length of input file name
		FULL_LENGTH="${#FILE}"
	
		# Calculate the length of the part we want
		OUTPUT_LENGTH=$FULL_LENGTH-$FOLDER_LENGTH-3
	
		# Grab the substring we want using lengths and add ".out"
		OUTPUT_NAME="${FILE:FOLDER_LENGTH:OUTPUT_LENGTH}.out"
		
		# Run Ptolemy
		"${PTOLEMY_DIR}"ptolemy <"${FILE}">"${OUTPUT_FILE_DIR}${OUTPUT_NAME}"
	
		# Echo message
		FULLFILE="${OUTPUT_FILE_DIR}${OUTPUT_NAME}"
		echo "Created ${FULLFILE##/home*/}"
	done
fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ RUN PTCLEAN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if [ $SWITCH_CLEAN == 1 ]
then
	for OUTFILE in "${OUTPUT_FILE_DIR}"*.out; do
		# Run ptclean script
		python "${PTOLEMY_DIR}"ptclean.py "${OUTFILE}"
		echo "Clean file ${OUTFILE##/home*/}-clean created"
	done
fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CREATE CSV ARRAY ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# First write a file list for python to read
CLEAN_NAME="CleanFileList.txt"
if [ $SWITCH_CSV_ARRAY == 1 ]
then
	# Clear the cleanFileList
	if [ -e "${OUTPUT_FILE_DIR}${CLEAN_NAME}" ]
	then
		rm "${OUTPUT_FILE_DIR}${CLEAN_NAME}"
	fi
	
	# Create new clean file list
	touch "${OUTPUT_FILE_DIR}${CLEAN_NAME}"
	
	# Fill the clean file list
	for OUTCLEAN in "${OUTPUT_FILE_DIR}"*.out-clean; do
		echo $OUTCLEAN >> "${OUTPUT_FILE_DIR}${CLEAN_NAME}"
	done
	
	# Now run the python script to create the mahoosive CSV file
	CSV_NAME="${OUTPUT_FILE_DIR}PT_Raw.csv"
	python "${PTOLEMY_ANALYSIS_DIR}"CSVFileCreator.py "${OUTPUT_FILE_DIR}${CLEAN_NAME}" "${CSV_NAME}"
fi







