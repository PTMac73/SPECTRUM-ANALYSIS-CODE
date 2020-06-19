#!/bin/bash
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# Loop over .ps files
CONVERT="inkscape --export-area-drawing --export-dpi=600 --export-type=pdf"
for f in $PWD/*.ps
do
	# Generate the file name
	FILENAME="${f%.ps}.pdf"

	# Check if the file name exists
	if [ -e $FILENAME ]
	then
		# Check if you want to overwrite
		echo "Would you like to overwrite `basename ${FILENAME}` [Y/N]"
		read OPTION

		# Overwrite if they chose yes
		if [[ $OPTION = "y" || $OPTION = "y" ]]
		then
			$( $CONVERT "${f}" )
			echo "Overwrote `basename ${FILENAME}`"
		fi
	else
		# Create a new file
		$( $CONVERT "${f}" )
		echo "`basename ${FILENAME}` created"
	fi
done
