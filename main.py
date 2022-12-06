import numpy as np

from Fluqet_Line_Equations.microStrip.Fluqet_line_support_equations import ABCD_TL, Pd, Bloch_impedance_Zb
from Fluqet_Line_Equations.microStrip.FloquetLine import SCFL_Model
from SuperConductivityEquations.SCE import conductivity, Zs
from utills_funcs_and_consts.Functions import nanoMeter_to_Meter, microMeter_to_Meters
from TransmissionLineEquations.microStrip.SC_MicroStrip_TL import SuperConductingMicroStripModel
import time

freq = 100000
epsilon_r = 10
height = nanoMeter_to_Meter(250)
thickness = nanoMeter_to_Meter(60)
ground_thickness = nanoMeter_to_Meter(300)
width = microMeter_to_Meters(1.49)
tc = 14.28
temp = 0
pn = 1.008e-6
tanD = 0

# ---------------------------- unit cell inputs from paper
unit_Cell_Len = microMeter_to_Meters(2300)
l1 = microMeter_to_Meters(50)
a = 1.2
b = 2
line = SuperConductingMicroStripModel(height, width, thickness, epsilon_r, tanD, False)






# CALC CONDUCTIVITY
conuct = conductivity(freq, temp, tc, pn)






# CALC ZS good
zs = Zs(freq, conuct, thickness)






# CALC G1 G2 good
g1 = line.G1(width, height, thickness)
g2 = line.G2(width, height, thickness)






# calc efm effective_dielectric_constant could be a source of issue
# todo confirm this this the dialetric const to use (good if its the right one)
effective_dielectric_const = line.epsilon_effst(epsilon_r, width,height,thickness)






# CALC Z AND Y USING G1 G2 EFM AND ZS good
Z = line.series_impedance_Z(zs, g1, g2, freq)
Y = line.shunt_admittance_Y(effective_dielectric_const, g1, freq)






# CALC PROP CONSTANT AND ZC USING Z AND Y good
prop_const = line.propagation_constant(Z, Y)
Zc = line.characteristic_impedance(Z, Y)



L1 = .5 * ((unit_Cell_Len / 3) - l1)
L2 = l1
L3 = (unit_Cell_Len / 3) - .5 * (l1 + l1)
L4 = l1
L5 = (unit_Cell_Len / 3) - .5 * (3 * l1)
L6 = 2 * l1
L7 = .5 * ((unit_Cell_Len / 3) - (3 * l1))




mat1 = ABCD_TL(Zc, prop_const, unit_Cell_Len)



Zb = Bloch_impedance_Zb(mat1)[0]
pb = Pd(mat1)


a = pb.real
b = pb.imag
r = Zb.real
x = Zb.imag










