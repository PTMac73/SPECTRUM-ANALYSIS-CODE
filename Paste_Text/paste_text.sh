#!/bin/bash
# Inserts useful blocks of text to the clipboard
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
# FUNCTIONS
# LaTeX Figures
figure(){
cat << EOH
\\begin{figure}[h!]
	\\centering
	\\includegraphics[width=\textwidth]{\detokenize{•}}
	\\caption{•}
	\\label{fig:•}
\\end{figure}
EOH
}

# Code header
header(){
cat << EOF
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #
EOF
}


# MAIN SCRIPT ----------------------------------------------------------------------------------- #
# Check for options
case "$1" in

	# Run helpfile
	-h|--help )
		echo "Help file needed"
		exit 0
		;;

	# Change number horizontally
	--lfig)
		figure  | xclip
		exit 0
		;;
	
	# Change number vertically
	--head)
		header | xclip
		exit 0
		;;

	# File directory the only other thing
	*)	
		exit 1
		;;
esac






