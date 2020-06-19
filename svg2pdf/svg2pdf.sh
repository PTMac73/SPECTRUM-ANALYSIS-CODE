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
	inkscape --export-area-drawing --export-dpi=600 --export-type=pdf "${i}"
	#inkscape -z -D --export-dpi=600 --file="${i}" --export-pdf="${i%%.svg}.pdf"
	echo "Created ${i%%.svg}.pdf"
done
