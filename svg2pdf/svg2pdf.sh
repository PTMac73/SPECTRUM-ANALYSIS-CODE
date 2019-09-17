#!/bin/bash
# svg2pdf - does what it says on the tin
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# Export to pdf
for i in $@
do
	inkscape --export-dpi=600 --export-pdf="${i%%.svg}.pdf" "${i}"
done
