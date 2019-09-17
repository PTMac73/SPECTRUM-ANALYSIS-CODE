#!/bin/bash
# nameFigure.sh renames one or more files to be Figures in Patrick's digital lab book
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# GENERATE PREFIX
PREFIX=`date +%Y-%m-%d_`
FIGURE_DIR="/home/ptmac/Documents/Notebooks/Digital-Lab-Book/figures"

# RENAME FILES
for f in $@
do
	if [ -e $f ]
	then
		mv "${f}" "${FIGURE_DIR}/${PREFIX}${f}"
		echo "${PREFIX}${f}" | xclip
	else
		echo "${f} does not exist!"
	fi
done

