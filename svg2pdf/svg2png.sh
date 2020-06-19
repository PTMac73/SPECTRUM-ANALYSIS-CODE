#!/bin/bash
# svg2png - does what it says on the tin
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# Department of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# Export to pdf
for i in $@
do
	inkscape --export-area-drawing --export-dpi=300 --export-type=png "${i}"
	#inkscape -z -D --export-dpi=300 --file="${i}" --export-png="${i%%.svg}.png"
	echo "Created ${i%%.svg}.png"
done
