# Generates DWUCK input files
# =============================================================================================== #
# Patrick MacGregor
# Nuclear Physics Research Group
# School of Physics and Astronomy
# The University of Manchester
# =============================================================================================== #

import opticalmodel_protons as omp
import opticalmodel_deuterons as omd
import opticalmodel_globals as omg
from dwuck_options import *

u = 931.49410242

def MassExcessToMass( Delta, A ):
	return ( Delta + A*u )/u
	
# j = 0 => l-1/2; j = 1 => l+1/2
def MakeNLJ(n,l,j):
	return str(n) + spdf[l] + str(2*(l+j) - 1) + "/2"


# GLOBAL VARIABLES
DTHET=0.1000
ELAB=18.9460
Z_Target = 12
Z_Projectile = 1
Z_Ejectile = 1
Z_Product = 12
Z_Core = 12
Z_Transfer = 0
A_Target = 28
A_Projectile = 2
A_Ejectile = 1
A_Product = 29
A_Core = 28
A_Transfer = 1
M_Target = MassExcessToMass( -15.0188, A_Target )
M_Projectile = MassExcessToMass( 13.1357, A_Projectile )
M_Ejectile = MassExcessToMass( 7.2889, A_Ejectile )
M_Product = MassExcessToMass( -10.6028, A_Product )
M_Core = MassExcessToMass( -15.0188, A_Core )
M_Transfer = 939.56542052/u
Q = ( M_Target + M_Projectile - M_Ejectile - M_Product )*u
Sn = ( M_Core + M_Transfer - M_Product )*u

target="28Mg"
reaction="(d,p)"



# ----------------------------------------------------------------------------------------------- #
# Define a function to get unbound string
def GetUn(b):
	if b == 1:
		return "un"
	else:
		return ""
		
# N.B. some useful functions in omg and dwuck_options

# Define function to write DWUCK block
def WriteDWUCKOutput( b_end_of_file = 0 ):
	# Get dictionary inputs
	Ex = dwuck_options["ex"]
	n = dwuck_options["n"]
	l = dwuck_options["l"]
	j = dwuck_options["j"] # j = 0 => l-1/2; j = 1 => l+1/2
	THET1 = dwuck_options["th_s"]
	nlj=MakeNLJ(n,l,j)
	
	if Ex > Sn:
		unbound = 1
	else:
		unbound = 0

	# Open the file and calculate optical model outputs
	file_out = dwuck_options["out_file"]
	om_in = omd.AnCai(A_Target, Z_Target, ELAB, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, 0, 1)
	om_out = omp.KoningDelaroche(A_Product, Z_Product, ELAB, Ex, M_Target, M_Projectile, M_Ejectile, M_Product, 1, 1)
	
	# Initial stuff
	file_out.write( "2001000000200000    " + target + reaction + " " + format(int(1000*Ex), "4.0f") + " keV  " + nlj + " " + GetUn(unbound) + "bound FR\n")
	file_out.write( omg.WriteBlock("090.") + omg.WriteBlock(format(THET1,"3.1f")) + omg.WriteBlock("0.1") + "\n")
	file_out.write( omg.WriteBlock("+30+01") + "\n" )
	if Ex > 4:
		sgn = "-"
	else:
		sgn = "+"
	file_out.write( omg.WriteBlock("+00.30") + omg.WriteBlock(sgn + "120.") + "\n" )
	file_out.write( omg.WriteDWUCKOMPar(ELAB) + omg.WriteDWUCKSmallNum(A_Projectile) + omg.WriteDWUCKSmallNum(Z_Projectile) + omg.WriteDWUCKSmallNum(A_Target) + omg.WriteDWUCKSmallNum(Z_Target) + om_in[3] + 2*omg.WriteBlock("") + omg.WriteBlock(" 2.0") + "\n")
	
	# Now add input - I know it's (d,p) for the time being
	for i in range(0,3):
		file_out.write( om_in[i] + "\n" )

	# Now onto second half of reaction
	file_out.write( omg.WriteDWUCKOMPar(Q - Ex ) + omg.WriteDWUCKSmallNum(A_Ejectile) + omg.WriteDWUCKSmallNum(Z_Ejectile) + omg.WriteDWUCKSmallNum(A_Product) + omg.WriteDWUCKSmallNum(Z_Product) + om_out[3] + 2*omg.WriteBlock("") + omg.WriteBlock("+01.") + "\n")

	# Now add output - I know it's (d,p) for the time being
	for i in range(0,3):
		file_out.write( om_out[i] + "\n" )
		
	# Add the rest
	file_out.write( omg.WriteDWUCKOMPar(Ex - Sn) + omg.WriteDWUCKSmallNum(A_Transfer) + omg.WriteDWUCKSmallNum(Z_Transfer) + omg.WriteDWUCKSmallNum(A_Core) + omg.WriteDWUCKSmallNum(Z_Core) + omg.WriteBlock("+01.30") + 2*omg.WriteBlock("") + omg.WriteBlock("+01.") + "\n")
	file_out.write("+01.    -01.    +01.28  +00.65\n")
	if j == 1: v_so_rl = "-24.00"
	elif j == 0: v_so_rl = "+24.00"
	file_out.write( omg.WriteBlock("-04.") + omg.WriteBlock(v_so_rl) + omg.WriteBlock("+01.10") + omg.WriteBlock("+00.65") + "\n" )
	file_out.write( omg.WriteDWUCKSignSmallNum(n) + omg.WriteDWUCKSignSmallNum(l) + omg.WriteDWUCKSignSmallNum(2*l+2*j-1) + omg.WriteDWUCKSignSmallNum(1.000) + omg.WriteDWUCKSignSmallNum(58.0) + "\n" )
	
	# Write STUFF ABOUT DEUTERON!
	file_out.write("""+400.   0.0     1.0     1.0               REID SOFT CORE DEUTERON L=0
  -1.2485295E+02  -1.2432747E+02  -1.2345849E+02  -1.2225587E+02  -1.2073277E+02
  -1.1890501E+02  -1.1679051E+02  -1.1440858E+02  -1.1177939E+02  -1.0892348E+02
  -1.0586135E+02  -1.0261318E+02  -9.9198676E+01  -9.5636973E+01  -9.1946568E+01
  -8.8145330E+01  -8.4250501E+01  -8.0278694E+01  -7.6245856E+01  -7.2167224E+01
  -6.8057268E+01  -6.3929657E+01  -5.9797217E+01  -5.5671884E+01  -5.1564667E+01
  -4.7486346E+01  -4.3445532E+01  -3.9451709E+01  -3.5513011E+01  -3.1636959E+01
  -2.7830557E+01  -2.4100366E+01  -2.0452563E+01  -1.6887376E+01  -1.3420502E+01
  -1.0053428E+01  -6.7904970E+00  -3.6354232E+00  -5.9129861E-01   2.3393867E+00
   5.1559215E+00   7.8674707E+00   1.0460003E+01   1.2932184E+01   1.5283225E+01
   1.7512881E+01   1.9621428E+01   2.1609637E+01   2.3478726E+01   2.5230319E+01
   2.6866388E+01   2.8389191E+01   2.9801218E+01   3.1105129E+01   3.2303705E+01
   3.3399795E+01   3.4396279E+01   3.5370705E+01   3.6207421E+01   3.6947788E+01
   3.7594025E+01   3.8148577E+01   3.8614116E+01   3.8993533E+01   3.9289935E+01
   3.9506623E+01   3.9647078E+01   3.9714934E+01   3.9713953E+01   3.9647990E+01
   3.9520967E+01   3.9336833E+01   3.9099532E+01   3.8812965E+01   3.8480962E+01
   3.8107245E+01   3.7695402E+01   3.7248860E+01   3.6770864E+01   3.6264458E+01
   3.6018571E+01   3.5541737E+01   3.5034584E+01   3.4498380E+01   3.3934431E+01
   3.3344098E+01   3.2728804E+01   3.2090037E+01   3.1429361E+01   3.0748412E+01
   3.0048899E+01   2.9332605E+01   2.8601378E+01   2.7857127E+01   2.7101812E+01
   2.6337435E+01   2.5566029E+01   2.4789643E+01   2.4010329E+01   2.3230129E+01
   2.2451058E+01   2.1675090E+01   2.0904142E+01   2.0140058E+01   1.9384599E+01
   1.8639424E+01   1.7906078E+01   1.7185987E+01   1.6480439E+01   1.5790582E+01
   1.5117413E+01   1.4461776E+01   1.3824359E+01   1.3205687E+01   1.2606132E+01
   1.2025905E+01   1.1465070E+01   1.0923542E+01   1.0401099E+01   9.8973916E+00
   9.4119500E+00   8.9441991E+00   8.4934701E+00   8.0590144E+00   7.6400177E+00
   7.2356147E+00   6.8449046E+00   6.4669657E+00   6.1008702E+00   5.7456985E+00
   5.4005532E+00   5.0645719E+00   4.7369390E+00   4.4168968E+00   4.1037549E+00
   3.7968983E+00   3.4957945E+00   3.1999983E+00   2.9091554E+00   2.6230048E+00
   2.3413787E+00   2.0642015E+00   1.7914875E+00   1.5233359E+00   1.2599262E+00
   1.0015108E+00   7.4840765E-01   5.0099114E-01   2.5968261E-01   2.4940109E-02
  -2.0275233E-01  -4.2289566E-01  -6.3498689E-01  -8.3853015E-01  -1.0330474E+00
  -1.2180888E+00  -1.3932424E+00  -1.5581433E+00  -1.7124818E+00  -1.8560105E+00
  -1.9885503E+00  -2.1099956E+00  -2.2203180E+00  -2.3195683E+00  -2.4078781E+00
  -2.4854594E+00  -2.5526031E+00  -2.6096763E+00  -2.6571184E+00  -2.6954359E+00
  -2.7251967E+00  -2.7470225E+00  -2.7615815E+00  -2.7695797E+00  -2.7717516E+00
  -2.7688514E+00  -2.7616428E+00  -2.7508891E+00  -2.7373442E+00  -2.7217425E+00
  -2.7047899E+00  -2.6871552E+00  -2.6694623E+00  -2.6522824E+00  -2.6361282E+00
  -2.6214478E+00  -2.6086206E+00  -2.5979540E+00  -2.5896806E+00  -2.5839574E+00
  -2.5808659E+00  -2.5804127E+00  -2.5825324E+00  -2.5870903E+00  -2.5938870E+00
  -2.6026634E+00  -2.6131068E+00  -2.6248578E+00  -2.6375174E+00  -2.6506552E+00
  -2.6638172E+00  -2.6765347E+00  -2.6883328E+00  -2.6987386E+00  -2.7072903E+00
  -2.7135446E+00  -2.7170849E+00  -2.7175282E+00  -2.7145318E+00  -2.7077993E+00
  -2.6970851E+00  -2.6821992E+00  -2.6630098E+00  -2.6394461E+00  -2.6114992E+00
  -2.5792224E+00  -2.5427304E+00  -2.5021977E+00  -2.4578560E+00  -2.4099902E+00
  -2.3589346E+00  -2.3050671E+00  -2.2488040E+00  -2.1905933E+00  -2.1309080E+00
  -2.0702388E+00  -2.0090867E+00  -1.9479557E+00  -1.8873449E+00  -1.8277416E+00
  -1.7696134E+00  -1.7134024E+00  -1.6595176E+00  -1.6083302E+00  -1.5601677E+00
  -1.5153096E+00  -1.4739839E+00  -1.4363638E+00  -1.4025660E+00  -1.3726493E+00
  -1.3466147E+00  -1.3244054E+00  -1.3059093E+00  -1.2909602E+00  -1.2793422E+00
  -1.2707923E+00  -1.2650064E+00  -1.2616432E+00  -1.2603307E+00  -1.2606724E+00
  -1.2622533E+00  -1.2646468E+00  -1.2674216E+00  -1.2701486E+00  -1.2724074E+00
  -1.2737931E+00  -1.2739222E+00  -1.2724388E+00  -1.2690198E+00  -1.2633798E+00
  -1.2552752E+00  -1.2445077E+00  -1.2309272E+00  -1.2144334E+00  -1.1949776E+00
  -1.1725625E+00  -1.1472421E+00  -1.1191203E+00  -1.0883489E+00  -1.0551250E+00
  -1.0196874E+00  -9.8231274E-01  -9.4331057E-01  -9.0301853E-01  -8.6179676E-01
  -8.2002203E-01  -7.7808177E-01  -7.3636790E-01  -6.9527060E-01  -6.5517226E-01
  -6.1644146E-01  -5.7942733E-01  -5.4445417E-01  -5.1181651E-01  -4.8177470E-01
  -4.5455105E-01  -4.3032651E-01  -4.0923819E-01  -3.9137739E-01  -3.7678848E-01
  -3.6546847E-01  -3.5736733E-01  -3.5238907E-01  -3.5039344E-01  -3.5119841E-01
  -3.5458325E-01  -3.6029214E-01  -3.6803837E-01  -3.7750897E-01  -3.8836970E-01
  -4.0027037E-01  -4.1285034E-01  -4.2574417E-01  -4.3858729E-01  -4.5102165E-01
  -4.6270118E-01  -4.7329709E-01  -4.8250281E-01  -4.9003857E-01  -4.9565558E-01
  -4.9913960E-01  -5.0031406E-01  -4.9904249E-01  -4.9523037E-01  -4.8882625E-01
  -4.7982226E-01  -4.6825389E-01  -4.5419913E-01  -4.3777693E-01  -4.1914501E-01
  -3.9849718E-01  -3.7605997E-01  -3.5208891E-01  -3.2686425E-01  -3.0068646E-01
  -2.7387133E-01  -2.4674494E-01  -2.1963841E-01  -1.9288274E-01  -1.6680354E-01
  -1.4171596E-01  -1.1791983E-01  -9.5694981E-02  -7.5297007E-02  -5.6953357E-02
  -4.0859925E-02  -2.7178146E-02  -1.6032642E-02  -7.5094618E-03  -1.6549286E-03
   1.5248839E-03   2.0640452E-03   3.6036217E-05  -4.4475923E-03  -1.1239148E-02
  -2.0157277E-02  -3.0989955E-02  -4.3497940E-02  -5.7418627E-02  -7.2470249E-02
  -8.8356349E-02  -1.0477046E-01  -1.2140092E-01  -1.3793571E-01  -1.5406733E-01
  -1.6949750E-01  -1.8394178E-01  -1.9713385E-01  -2.0882960E-01  -2.1881072E-01
  -2.2688799E-01  -2.3290401E-01  -2.3673549E-01  -2.3829493E-01  -2.3753177E-01
  -2.3443297E-01  -2.2902297E-01  -2.2136310E-01  -2.1155038E-01  -1.9971581E-01
  -1.8602211E-01  -1.7066103E-01  -1.5385010E-01  -1.3582917E-01  -1.1685649E-01
  -9.7204567E-02  -7.7155817E-02  -5.6998108E-02  -3.7020213E-02  -1.7507285E-02
   1.2635858E-03   1.9027664E-02   3.5536656E-02   5.0562503E-02   6.3900855E-02
   7.5374145E-02   8.4834236E-02   9.2164593E-02   9.7281949E-02   1.0013745E-01
   1.0071725E-01   9.9042575E-02   9.5169193E-02   8.9186417E-02   8.1215535E-02
   7.1407774E-02   5.9941802E-02   4.7020813E-02   3.2869247E-02   1.7729197E-02
""")

	if b_end_of_file == 1:
		file_out.write("9                   END OF DATA for DWUCK5 test cases ")


# ----------------------------------------------------------------------------------------------- #

# Get input parameters from file/script

# Write paramaters to file

