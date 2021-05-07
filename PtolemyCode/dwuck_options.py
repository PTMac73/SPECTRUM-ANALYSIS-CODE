# Define default inputs dictionary	
dwuck_options = {
	"ex": 4.36,
	"n": 0,
	"l": 3,
	"j": 1,
	"th_s": 0.0,
	"out_file": 0
}

spdf = ['s','p','d','f','g','h','i','j']

def SetDWOptions(ex,n,l,j,th_s,out_file):
	dwuck_options["ex"] = ex
	dwuck_options["n"] = n
	dwuck_options["l"] = l
	dwuck_options["j"] = j
	dwuck_options["th_s"] = th_s
	dwuck_options["out_file"] = out_file
