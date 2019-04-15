#!/bin/bash
# nameFigure.sh renames one or more files to be Figures in Patrick's digital lab book
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# GENERATE PREFIX
PREFIX=`date +%Y∙%V_%d%b%y-`

# RENAME FILES
for f in $@
do
	if [ -e $f ]
	then
		mv "${f}" "${PREFIX}${f}"
	else
		echo "${f} does not exist!"
	fi
done

