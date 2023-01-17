'''
Test file for calculating A B R X
'''

import time
import numpy as np
from matplotlib import pyplot as plt
from Fluqet_Line_Equations.MicroStrip.FloquetLine import SuperConductingFloquetLine
from Inputs.MicroStripInputs import MicroStripInputs
from SuperConductivityEquations.SCE import SuperConductivity
from Utills.Constants import PI2
from TransmissionLineEquations.MicroStrip.SC_MicroStrip_TL import SuperConductingMicroStripModel

s = time.time()

# ---------------------------- inputs ----------------------------
MSinputs = MicroStripInputs()

# ---------------------------- dependency models ----------------------------
super_conductivity_model = SuperConductivity(MSinputs.op_temp, MSinputs.crit_temp, MSinputs.normal_resistivity)
Central_line_model = SuperConductingMicroStripModel(MSinputs.height, MSinputs.central_line_width,
                                                    MSinputs.line_thickness, MSinputs.er, MSinputs.tangent_delta,
                                                    MSinputs.crit_current)
Load_line_models = [
    SuperConductingMicroStripModel(MSinputs.height, width, MSinputs.line_thickness, MSinputs.er, MSinputs.tangent_delta,
                                   MSinputs.crit_current) for width in MSinputs.load_widths]
floquet_line = SuperConductingFloquetLine(MSinputs.unit_cell_length, MSinputs.D0, MSinputs.load_lengths,
                                          Load_line_models,
                                          Central_line_model,
                                          super_conductivity_model, MSinputs.central_line_width, MSinputs.load_widths,
                                          MSinputs.line_thickness, MSinputs.crit_current)

# ---------------------------- calculations -------------------






a, r, x, beta, betaUf, freqs, RR, LL, GG, CC, gamma, transmission = [], [], [], [], [], [], [], [], [], [], [], []
FRange = np.linspace(MSinputs.start_freq_GHz, MSinputs.end_freq_GHz, MSinputs.resoultion)
for F in FRange:
    aa, t, bta, rr, xx, R, L, G, C = floquet_line.abrx(F)
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
print("% calc conduct: ", (floquet_line.tot / total) * 100)


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
# a1.axvspan(Floquet_line.target_pump_zone_start // 3, Floquet_line.target_pump_zone_end // 3, facecolor='g', alpha=0.5)

fig, (a1, a2, a3, a4, a5) = plt.subplots(5)
a1.plot(freqs, beta)
a1.set_title('beta Unfolded')
a1.plot(freqs, floquet_line.unfold(beta))

a2.set_title('A')
a2.plot(freqs, a)

a3.set_title('R')
a3.plot(freqs, r)

a4.set_title('X')
a4.plot(freqs, x)
plt.subplots_adjust(hspace=1)
# Floquet_line.FindPumpZone(a)
a2.axvspan(floquet_line.target_pump_zone_start, floquet_line.target_pump_zone_end, facecolor='g', alpha=0.5)





# # a5.plot(freqs, np.abs(CLWWI))
# # a5.plot(freqs, np.abs(CRwI))
# # a5.plot(freqs, np.abs(GLwI))
# # a5.plot(freqs, np.abs(RGI))
# # a5.plot(freqs, np.abs(GLIIIwDiv3))
# # a5.plot(freqs, np.abs(CLIIIWWDiv3))
# a5.plot(transmission)
# plt.yscale("log")








plt.show()



