#!/bin/bash
# XMG-MgStates.sh
# Takes the assigned peak files and compiles them all into one graph
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# PTOLEMY_DATA is of the form "X[TAB]Y"
# EXPERIMENTAL_DATA is of the form "X[TAB]Y[TAB]E"
# =============================================================================================== #
# Fixed parameters
SCRIPT_DIR="/home/ptmac/Documents/SPECTRUM_ANALYSIS_CODE/XMGraceMg/"

# SWITCHES
SWITCH_DELETE_FILE=1
SWITCH_CREATE_FILE=1
SWITCH_USE_CURRENT_TXT=0
SWITCH_WRITE_BATCH_FILE=1
SWITCH_XMGRACE=1
SWITCH_CONVERT=1
SWITCH_COMBINE_PDF=1

# Parameter to change whether X-Axes appear
X_AXIS_FOR_EACH=1

# Number of graphs per page (vertical graphs = -1 => do a full page)
HORZ_GRAPH_NUM=4
VERT_GRAPH_NUM=3

# Temporary number that works with test_if_num function
TEMP_NUM=0

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Deletes all the files in a given folder (if they exist) and ouputs a message to the console
delete_file_type(){
	# The first argument is the file type (e.g. ".txt")
	flag=0
	for file in "${FILE_DIR}"*"$1"
	do
		if [[ "$file" != "${FILE_DIR}*$1" ]]
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

# Tests if the first argument is a number, and returns the second (default) if it is not
test_if_num(){
	RE="^[0-9]+$"
	if [[ $1 =~ $RE ]]
	then
		TEMP_NUM=$1
	else
		TEMP_NUM=$2
	fi
}

# Test if something is a directory
test_if_dir(){
	if [ ! -d "${1}" ]
	then
		# If not directory, test if it is a file and take parent directory
		if [ -f "${1}" ]
		then
			echo "File given - taking parent directory..."
			FILE_DIR="${1%/*}/"
		else
			# Exit if neither file nor directory
			echo "Not a directory or a file. Try again!"
			exit 1
		fi
	else
		# Is a directory - ensure there is a slash on the end
		if [ "${1: -1}" != "/" ]
		then
			FILE_DIR="${1}/"
		else
			FILE_DIR="${1}"
		fi
	fi
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
for i in "$@"
do
	case "$i" in

		# Run helpfile
		-h|--help )
			echo "Help file needed"
			exit 0
			;;

		# Change number horizontally
		--horz=*)
			HORZ_GRAPH_NUM="${i#*=}"
			shift
			test_if_num $HORZ_GRAPH_NUM 4
			HORZ_GRAPH_NUM=$TEMP_NUM
			;;
		
		# Change number vertically
		--vert=*)
			VERT_GRAPH_NUM="${i#*=}"
			test_if_num $VERT_GRAPH_NUM 3
			VERT_GRAPH_NUM=$TEMP_NUM
			shift
			;;

		# File directory the only other thing
		*)	
			test_if_dir "${i}"
			shift
			;;
	esac
done


# SET DIRECTORIES
BASE_FILE="${FILE_DIR}/base.dat"
B_FILE="${FILE_DIR}/batch_file"
FILE_LIST="${FILE_DIR}/file_list"
IMAGE_FILE="${FILE_DIR}/full_page"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DELETE FILES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Delete all .pdf, .agr, .txt, and .ps files in the folder if there are any
if [ $SWITCH_DELETE_FILE == 1 ]
then
	delete_file_type ".pdf"
	delete_file_type ".ps"
	delete_file_type ".agr"
	delete_file_type ".txt"
	delete_file_type ".dat"
fi
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CREATE DAT FILES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if [ $SWITCH_CREATE_FILE == 1 ]
then
	# Create new dat files (if create text flag is 1)
	if [[ $SWITCH_USE_CURRENT_TXT == 0 ]]
	then
		delete_file_type ".dat"
		python "${SCRIPT_DIR}"XMGFileCreator.py "${FILE_DIR}"
		echo "Created DAT files"
	else
		echo "Using current DAT files in directory only"
	fi

	# Create the base file (for defining legends in XMGrace)
	touch "${BASE_FILE}"

	# Fill the base file
	echo "0 0" >> "${BASE_FILE}"

	##### MAKE A LIST OF ALL THE FILES AND STORE IN A TEXT FILE
	# Create a file containing all the file directories
	# First delete the old file list
	if [ -e "${FILE_DIR}/${FILE_LIST}"*.txt ]
	then
		rm "${FILE_DIR}/${FILE_LIST}"*.txt
		echo "Deleted file lists"
	fi	
	
	# Now fill some file list(s)
	if [ $VERT_GRAPH_NUM != -1 ]
	then
		# Do multiple pages
		DAT_COUNTER=0
		# Count the number of .txt files
		for f in "${FILE_DIR}"*Ex*.dat
		do
			DAT_COUNTER=$((DAT_COUNTER+1))
		done
		
		# Now calculate how many in total
		GRAPHS_PER_PAGE=$((HORZ_GRAPH_NUM*VERT_GRAPH_NUM))
		
		# Now calculate number of file lists
		if [ $((DAT_COUNTER%GRAPHS_PER_PAGE)) -eq 0 ]
		then
			NUM_FILELIST=$((DAT_COUNTER/GRAPHS_PER_PAGE))
		else
			NUM_FILELIST=$((DAT_COUNTER/GRAPHS_PER_PAGE + 1))
		fi
		
		# Now generate file lists
		ZERO_FLAG=0
		if [ $NUM_FILELIST -lt 10 ]
		then
			eval touch "${FILE_LIST}"{1..$NUM_FILELIST}".txt"
		else
			ZERO_FLAG=1
			eval touch "${FILE_LIST}"{01..$NUM_FILELIST}".txt"
		fi
		
		
		# Now put the relevant file directories into the list of files
		FILE_COUNTER=0
		FILE_LIST_COUNTER=1
		for f in "${FILE_DIR}"*Ex*.dat
		do
			# Get the file name as a variable
			E_DATA=$f
			PT_DATA=${E_DATA/Ex/PT}
			
			# Work out where the directory string needs to go
			if [ $FILE_COUNTER -ge $GRAPHS_PER_PAGE ]
			then
				FILE_LIST_COUNTER=$((FILE_LIST_COUNTER+1))
				FILE_COUNTER=0
			fi
			
			# Work out whether to append a zero or not
			if [ $ZERO_FLAG -eq 1 ] && [ $FILE_LIST_COUNTER -lt 10 ]
			then
				j="0"
			else
				j=""
			fi
			
			# Store the data
			echo "${E_DATA}" >> "${FILE_DIR}/${FILE_LIST}${j}${FILE_LIST_COUNTER}.txt"
			echo "${PT_DATA}" >> "${FILE_DIR}/${FILE_LIST}${j}${FILE_LIST_COUNTER}.txt"
		
			# Iterate the file counter
			FILE_COUNTER=$((FILE_COUNTER+1))
		done
	else
		# Do a full page
		NUM_FILELIST=1
		FILELIST_DIR="${FILE_DIR}/${FILE_LIST}${NUM_FILELIST}.txt"

		touch "${FILELIST_DIR}"

		# Now put all the relevant file directories into the list of files
		for f in "${FILE_DIR}"*Ex*.dat
		do
			E_DATA=$f
			PT_DATA=${E_DATA/Ex/PT}
			echo "${E_DATA}" >> "${FILELIST_DIR}"
			echo "${PT_DATA}" >> "${FILELIST_DIR}"
		done
	fi
	
fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CREATE BATCH FILE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if [ $SWITCH_WRITE_BATCH_FILE == 1 ]
then
	# Delete the batch file
	if [[ -e "${B_FILE}*.txt" ]]
	then
		rm "${B_FILE}*.txt"
	fi
	
	# Create a new batch file
	if [[ $ZERO_FLAG == 1 ]]
	then
		eval touch "${B_FILE}"{01..$NUM_FILELIST}".txt"
	else
		eval touch "${B_FILE}"{1..$NUM_FILELIST}".txt"
	fi
	# Run python script to write a batch file (called bFile[N], where [N] is an integer)
	i=1
	while [ $i -le $NUM_FILELIST ]
	do
		# Append zero if necessary
		j=""
		if [[ $ZERO_FLAG -eq 1 ]] && [ $i -lt 10 ]
		then
			j="0"
		fi
		
		
		if [ $X_AXIS_FOR_EACH = 1 ]
		then
			python "${SCRIPT_DIR}"XMGFullPage.py "${FILE_LIST}${j}${i}.txt" "${B_FILE}${j}${i}.txt" "${BASE_FILE}" "${HORZ_GRAPH_NUM}" "${VERT_GRAPH_NUM}"
		else
			# TODO NEED TO WRITE THIS FEATURE
			#python "${SCRIPT_DIR}"XMGFullPageCompact.py "${FILE_LIST}${j}${i}.txt" "${B_FILE}${j}${i}.txt" "${BASE_FILE}"
			echo "BANANAS!"
		fi
	i=$((i+1))
	done
fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ RUN XMGRACE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if [ $SWITCH_XMGRACE == 1 ]
then
	for g in "${B_FILE}"*".txt"
	do
		gracebat -batch "${g}" -nosafe
	done
	echo "Created PS files and AGR files"
fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONVERT PS FILES TO PDF ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if [ $SWITCH_CONVERT == 1 ]
then
	for h in "${IMAGE_FILE}"*".ps"
	do
		# Now convert PS files to PDF
		PS_FILE=$h
		PDF_FILE=${PS_FILE%%ps}pdf
		BOUND_LINE="$(sed "2q;d" "$h")"
		# Grab last two numbers
		B_WIDTH="$(echo $BOUND_LINE | cut -d' ' -f4)"
		B_HEIGHT="$(echo $BOUND_LINE | cut -d' ' -f5)"

		# Convert PS files to PDF files with GS
		gs -o "${PDF_FILE}" -sDEVICE=pdfwrite -g"${B_WIDTH}0"x"${B_HEIGHT}0" -dPDFFitPage -dPDFSETTINGS=/prepress -dHaveTrueTypes=true -dEmbedAllFonts=true -dSubsetFonts=false -c ".setpdfwrite <</NeverEmbed [ ]>> setdistillerparams" -f "${PS_FILE}" > /dev/null
	done
	

	echo "Created PDF file"
fi

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONCATENATE PDF FILES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if [ $SWITCH_COMBINE_PDF == 1 ]
then
	# Count the number of files that match $IMAGE_FILE*.pdf
	FILE_COUNTER=0
	for i in "${IMAGE_FILE}"*".pdf"
	do
		FILE_COUNTER=$((FILE_COUNTER+1))
	done
	
	# Now combine if file counter > 1
	TEMPSTRING=""
	if [ $FILE_COUNTER -gt 0 ]
	then
		for j in "${IMAGE_FILE}"*".pdf"
		do
			TEMPSTRING="${TEMPSTRING} ${j}"
		done
	
		# Now have list of files - put into ghostscript command
		gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile="${IMAGE_FILE}FULL.pdf" $TEMPSTRING
	fi
fi

















