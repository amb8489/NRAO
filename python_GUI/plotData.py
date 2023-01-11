'''
Testing file for calculating A B R X
'''
import numpy as np
from Fluqet_Line_Equations.MicroStrip.FloquetLine import SuperConductingFloquetLine
from SuperConductivityEquations.SCE import SuperConductivity
from Utills.Functions import nanoMeters_to_Meters, microMeters_to_Meters, toGHz
from TransmissionLineEquations.MicroStrip.SC_MicroStrip_TL import SuperConductingMicroStripModel



# ---------------------------- unit cell inputs from paper
unit_Cell_Len = microMeters_to_Meters(2300)
l1 = microMeters_to_Meters(50)
central_Line_width = microMeters_to_Meters(1.49)
load_width1 = central_Line_width * 1.2

D0 = .0007666666666666666666
D1 = 5e-5
D2 = 5e-5
D3 = .0001
loads_legths = [D1, D2, D3]
number_of_loads = len(loads_legths)

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


def simulate():
    a, r, x, beta, betaUf, freqs, RR, LL, GG, CC, gamma, transmission = [], [], [], [], [], [], [], [], [], [], [], []

    # ---------------------------- model of the Super conductor
    super_conductivity_model = SuperConductivity(T, Tc, pn)

    # ---------------------------- models of the MicroStripModel -

    Central_line_model = SuperConductingMicroStripModel(Height, central_Line_width, line_thickness, er, tanD, Jc)
    # list of individual load widths from left to right widths
    Load_widths = [load_width1, load_width1, load_width1]
    Load_line_models = [SuperConductingMicroStripModel(Height, width, line_thickness, er, tanD, Jc) for width in
                        Load_widths]

    # ---------------------------- model of the floquet line
    Floquet_line = SuperConductingFloquetLine(unit_Cell_Len, D0, loads_legths, Load_line_models, Central_line_model,
                                              super_conductivity_model, central_Line_width, Load_widths, line_thickness, Jc)

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



    return {

        "freqs":FRange.tolist(),
        "alpha":a
    }
