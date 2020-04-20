# Columns are Ex, X, Y, E
import sys
import os

def FloatToStr( a ):
	try:
		float(a)
		return str( round( float(a), 3 ) ).replace('.','_')
	except:
		return "XXX"
		


# Open the file
in_file_file = sys.argv[1]
in_file = open( in_file_file, 'r' )
in_file_dir = os.path.dirname(in_file_file)

if in_file_dir == "":
	rm_file_dir = "."
else:
	rm_file_dir = in_file_dir



for file_name in os.listdir( rm_file_dir ):
	if file_name.endswith('.dat'):
		os.remove(file_name)

if in_file_dir != "":
	in_file_dir += "/"

ex = []
x = []
y = []
e = []


for line in in_file:
	line_arr = line.split(',')
	
	if len(line_arr) >= 4:
		ex.append( line_arr[0] )
		x.append( line_arr[1] )
		y.append( line_arr[2] )
		e.append( line_arr[3].rstrip('\n') )

# Close the file
in_file.close()

# Write to files
for i in range(0, len(ex) ):
	if i == 0 or ex[i-1] != ex[i]:
		out_file = open( in_file_dir + "add_" + FloatToStr(ex[i]) + ".dat", 'a')
	
	try:
		float(x[i])
		float(y[i])
		float(e[i])
		if float(x[i]) != 0 and float(y[i]) != 0 and float(e[i]) != 0:
			out_str = str(x[i]) + "\t" + str(y[i]) + "\t" + str(e[i]) + "\n"
			out_file.write(out_str)
	except:
		continue
	
	if i < len(ex) - 1 and ex[i+1] != ex[i]:
		out_file.close()

