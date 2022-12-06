'''
Testing file for calculating A B R X
'''

import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.microStrip.FloquetLine import Super_Conducting_Floquet_Line
from SuperConductivityEquations.SCE import SuperConductivity
from utills_funcs_and_consts.Constants import PI2
from utills_funcs_and_consts.Functions import nanoMeters_to_Meters, microMeters_to_Meters, mm_To_Meters, toGHz
from TransmissionLineEquations.microStrip.SC_MicroStrip_TL import SuperConductingMicroStripModel

s = time.time()

# ---------------------------- inputs ----------------------------
a, r, x, beta, betaUf, freqs, RR, LL, GG, CC, gamma = [], [], [], [], [], [], [], [], [], [], []

# ---------------------------- unit cell inputs from paper
unit_Cell_Len = microMeters_to_Meters(2300)
l1 = microMeters_to_Meters(50)
width_unloaded = microMeters_to_Meters(1.49)
width_loaded = width_unloaded * 1.2

D0 = .0007666666666666666666
D1 = 5e-5
D2 = 5e-5
D3 = .0001
loads_Widths = [D1, D2, D3]
number_of_loads = len(loads_Widths)

# ---------------------------- SC inputs
er = 10
Height = nanoMeters_to_Meters(250)
line_thickness = nanoMeters_to_Meters(60)
ground_thickness = nanoMeters_to_Meters(300)
Tc = 14.28
T = 0
pn = 1.008e-6
tanD = 0
Jc = 1

# secoind paper inputs
# ---------------------------- unit cell inputs from paper
# width_unloaded = microMeters_to_Meters(1)
# width_loaded = microMeters_to_Meters(4)
# D0 = mm_To_Meters(1.34)
# D1 = microMeters_to_Meters(100)
# D2 = microMeters_to_Meters(100)
# D3 = microMeters_to_Meters(95)
# unit_Cell_Len = mm_To_Meters(4.02)
#
# In_Order_loads_Widths = [D1, D2, D3]
# number_of_loads = len(In_Order_loads_Widths)
#
# # ---------------------------- SC inputs
# Height = nanoMeters_to_Meters(300)
# line_thickness = nanoMeters_to_Meters(60)
# ground_thickness = nanoMeters_to_Meters(300)
# Tc = 14.7
# T = 4  # what equatioins to use when temp is > 0
# pn = 0.00000132
# er = 11.44
# tanD = 1.48351e-5
# Jc = 1


# ---------------------------- models of the MicroStripModel -
#                      one for an unloaded line , one for a loaded line
loaded_line_model = SuperConductingMicroStripModel(Height, width_loaded, line_thickness, er, tanD, Jc)
unloaded_line_model = SuperConductingMicroStripModel(Height, width_unloaded, line_thickness, er, tanD, Jc)

# ---------------------------- model of the Super conductor
super_conductivity_model = SuperConductivity(T, Tc, pn)

# ---------------------------- model of the floquet line
Floquet_line = Super_Conducting_Floquet_Line(unit_Cell_Len, D0, loads_Widths, loaded_line_model, unloaded_line_model,
                                             super_conductivity_model, width_unloaded, width_loaded, line_thickness, Jc)

# ---------------------------- calculations -------------------
FRange = np.linspace(toGHz(6.6), toGHz(25), 1000)
for F in FRange:
    aa, bta, unfolded, rr, xx, R, L, G, C = Floquet_line.abrx(F)

    RR.append(R)
    LL.append(L)
    GG.append(G)
    CC.append(C)
    beta.append(bta)
    betaUf.append(unfolded)
    a.append(aa)
    r.append(rr)
    x.append(xx)
    freqs.append(F)

total = time.time() - s
print("total time: ", time.time() - s)
print("% calc conduct: ", (Floquet_line.tot / total) * 100)

RR, LL, GG, CC, gamma = np.array(RR), np.array(LL), np.array(GG), np.array(CC), np.array(gamma)

I = .2
I3 = I * I * I

w = FRange * PI2
WW = w * w

# todo gamma*I
CLWWI = CC * LL * WW * I
CRwI = CC * RR * w * I
GLwI = GG * LL * w * I
RGI = RR * GG * I
GLIIIwDiv3 = GG * LL * I3 * (w / 3)
CLIIIWWDiv3 = CC * LL * I3 * (WW / 3)
YYI = gamma * gamma * I  # TODO

# ---------------------------- plots----------------------------
fig, (a1, a2, a3, a4, a5) = plt.subplots(5)
a1.plot(freqs, beta)
a1.set_title('beta Unfolded')
a1.plot(freqs, betaUf)

a2.set_title('A')
a2.plot(freqs, a)

a3.set_title('R')
a3.plot(freqs, r)

a4.set_title('X')
a4.plot(freqs, x)
plt.subplots_adjust(hspace=1)
a2.axvspan(Floquet_line.ChoosePumpZoneA // 3, Floquet_line.ChoosePumpZoneB // 3, facecolor='g', alpha=0.5)

a5.plot(freqs, np.abs(CLWWI))
a5.plot(freqs, np.abs(CRwI))
a5.plot(freqs, np.abs(GLwI))
a5.plot(freqs, np.abs(RGI))
a5.plot(freqs, np.abs(GLIIIwDiv3))
a5.plot(freqs, np.abs(CLIIIWWDiv3))
plt.yscale("log")

plt.show()
