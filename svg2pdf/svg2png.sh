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
	inkscape -z -D --export-dpi=300 --file="${i}" --export-png="PNG-${i%%.svg}.png"
	echo "Created PNG-${i%%.svg}.png"
done
