'''
Testing file for calculating A B R X
'''

import time
import numpy as np
import scipy
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.MicroStrip.FloquetLine import SuperConductingFloquetLine
from SuperConductivityEquations.SCE import SuperConductivity
from Utills.Constants import PI2
from Utills.Functions import nanoMeters_to_Meters, microMeters_to_Meters, mm_To_Meters, toGHz
from TransmissionLineEquations.MicroStrip.SC_MicroStrip_TL import SuperConductingMicroStripModel

s = time.time()

# ---------------------------- inputs ----------------------------
a, r, x, beta, betaUf, freqs, RR, LL, GG, CC, gamma, transmission = [], [], [], [], [], [], [], [], [], [], [], []

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
T = 4
pn = 1.008e-6
tanD = 0
Jc = 200000000

# ---------------------------- model of the Super conductor
super_conductivity_model = SuperConductivity(T, Tc, pn)

# ---------------------------- models of the MicroStripModel -
#                      one for an unloaded line , one for a loaded line
loaded_line_model = SuperConductingMicroStripModel(Height, width_loaded, line_thickness, er, tanD, Jc)
unloaded_line_model = SuperConductingMicroStripModel(Height, width_unloaded, line_thickness, er, tanD, Jc)

# ---------------------------- model of the floquet line
Floquet_line = SuperConductingFloquetLine(unit_Cell_Len, D0, loads_Widths, loaded_line_model, unloaded_line_model,
                                          super_conductivity_model, width_unloaded, width_loaded, line_thickness, Jc)

# ---------------------------- calculations -------------------
FRange = np.linspace(toGHz(1), toGHz(25), 1000)
for F in FRange:
    aa, t, bta, rr, xx, R, L, G, C = Floquet_line.abrx(F)

    RR.append(R)
    LL.append(L)
    GG.append(G)
    CC.append(C)
    beta.append(bta)
    a.append(aa)
    r.append(rr)
    x.append(xx)
    transmission.append(t)

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

# fig, a1 = plt.subplots(1)
# a1.plot(freqs, beta)
# a1.set_title('beta Unfolded')
# a1.plot(freqs,Floquet_line.unfold(beta))
# a1.axvspan(Floquet_line.ChoosePumpZoneA // 3, Floquet_line.ChoosePumpZoneB // 3, facecolor='g', alpha=0.5)

fig, (a1, a2, a3, a4, a5) = plt.subplots(5)
a1.plot(freqs, beta)
a1.set_title('beta Unfolded')
a1.plot(freqs, Floquet_line.unfold(beta))

a2.set_title('A')
a2.plot(freqs, a)

a3.set_title('R')
a3.plot(freqs, r)

a4.set_title('X')
a4.plot(freqs, x)
plt.subplots_adjust(hspace=1)
Floquet_line.FindPumpZone(a)
a2.axvspan(Floquet_line.ChoosePumpZoneA , Floquet_line.ChoosePumpZoneB , facecolor='g', alpha=0.5)

# a5.plot(freqs, np.abs(CLWWI))
# a5.plot(freqs, np.abs(CRwI))
# a5.plot(freqs, np.abs(GLwI))
# a5.plot(freqs, np.abs(RGI))
# a5.plot(freqs, np.abs(GLIIIwDiv3))
# a5.plot(freqs, np.abs(CLIIIWWDiv3))
a5.plot(transmission)
plt.yscale("log")

plt.show()
