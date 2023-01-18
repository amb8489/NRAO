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


alpha_plt, r, x, beta_plt, beta_unfold_plt, RR, LL, GG, CC, gamma, transmission_plt = [], [], [], [], [], [], [], [], [], [], []
FRange = np.linspace(MSinputs.start_freq_GHz, MSinputs.end_freq_GHz, MSinputs.resoultion)
for F in FRange:
    aa, t, bta, rr, xx, R, L, G, C = floquet_line.abrx(F)
    RR.append(R)
    LL.append(L)
    GG.append(G)
    CC.append(C)
    beta_plt.append(bta)
    alpha_plt.append(aa)
    r.append(rr)
    x.append(xx)
    transmission_plt.append(t)

total = time.time() - s
print("total time: ", time.time() - s)
print("% calc conduct: ", (floquet_line.tot / total) * 100)

RR, LL, GG, CC, gamma = np.array(RR), np.array(LL), np.array(GG), np.array(CC), np.array(gamma)
I = .2
I3 = I * I * I
w = FRange * PI2
WW = w * w
CLWWI = CC * LL * WW * I
CRwI = CC * RR * w * I
GLwI = GG * LL * w * I
RGI = RR * GG * I
GLIIIwDiv3 = GG * LL * I3 * (w / 3)
CLIIIWWDiv3 = CC * LL * I3 * (WW / 3)
YYI = gamma * gamma * I  # TODO

# ---------------------------- plots----------------------------


# exit(999)


fig, (plt1, plt2, plt3, plt4, plt5, plt6) = plt.subplots(6)

plt1.plot(FRange, beta_plt)
plt1.set_title('beta_plt Unfolded')
plt1.plot(FRange, floquet_line.unfold(beta_plt))



plt2.set_title('Alpha')
floquet_line.FindPumpZone(3, np.array(alpha_plt))
print(floquet_line.target_pump_zone_start)
plt2.axvspan(FRange[int(floquet_line.target_pump_zone_start)], FRange[int(floquet_line.target_pump_zone_end)],
             facecolor='b', alpha=0.3)
plt2.axvspan(FRange[int(floquet_line.target_pump_zone_start / 3)], FRange[int(floquet_line.target_pump_zone_end / 3)],
             facecolor='g', alpha=0.5)
plt2.plot(FRange, alpha_plt)




plt3.set_title('R')
plt3.plot(FRange, r)

plt4.set_title('X')
plt4.plot(FRange, x)

plt5.set_title('Transmission')
plt5.plot(transmission_plt)


plt.yscale("log")
plt6.set_title('circuit values')
plt6.plot(FRange, np.abs(CLWWI))
plt6.plot(FRange, np.abs(CRwI))
plt6.plot(FRange, np.abs(GLwI))
plt6.plot(FRange, np.abs(RGI))
plt6.plot(FRange, np.abs(GLIIIwDiv3))
plt6.plot(FRange, np.abs(CLIIIWWDiv3))
plt.yscale("log")

plt.show()
