#!/bin/bash
# svg2pdf - does what it says on the tin
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# Department of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# Export to pdf
for i in $@
do
	inkscape -z -D --export-dpi=600 --file="${i}" --export-pdf="PDF-${i%%.svg}.pdf" 
done
