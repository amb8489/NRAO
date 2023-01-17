import time
import numpy as np
from Fluqet_Line_Equations.MicroStrip.FloquetLine import SuperConductingFloquetLine
from SuperConductivityEquations.SCE import SuperConductivity
from TransmissionLineEquations.MicroStrip.SC_MicroStrip_TL import SuperConductingMicroStripModel
from Utills.Constants import PI2


def mkGraphs(StartFreq, EndFreq, resolution, unit_Cell_Len, D0, loads_Widths, width_unloaded, width_loaded, er,
             Height, line_thickness, Tc, pn, tanD, T, Jc):
    s = time.time()

    FreqRange = np.linspace(int(StartFreq), int(EndFreq), int(resolution))

    # ---------------------------- models of the MicroStripModel -
    #                      one for an unloaded line , one for alpha_plt loaded line
    loaded_line_model = SuperConductingMicroStripModel(Height, width_loaded, line_thickness, er, tanD, Jc)
    unloaded_line_model = SuperConductingMicroStripModel(Height, width_unloaded, line_thickness, er, tanD, Jc)

    # ---------------------------- model of the Super conductor
    super_conductivity_model = SuperConductivity(T, Tc, pn)

    # ---------------------------- model of the floquet line
    Floquet_line = SuperConductingFloquetLine(unit_Cell_Len, D0, loads_Widths, loaded_line_model, unloaded_line_model,
                                              super_conductivity_model, width_unloaded, width_loaded, line_thickness,
                                              Jc)

    a, r, x, beta, betaUf, freqs, RR, LL, GG, CC, gamma, transmission = [], [], [], [], [], [], [], [], [], [], [], []
    for F in FreqRange:
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

    # RR, LL, GG, CC, gamma = np.array(RR), np.array(LL), np.array(GG), np.array(CC), np.array(gamma)
    #
    # I = .2  # todo
    # I3 = I * I * I
    #
    # w = FreqRange * PI2
    # WW = w * w
    #
    # # todo gamma*I
    # CLWWI = CC * LL * WW * I
    # CRwI = CC * RR * w * I
    # GLwI = GG * LL * w * I
    # RGI = RR * GG * I
    # GLIIIwDiv3 = GG * LL * I3 * (w / 3)
    # CLIIIWWDiv3 = CC * LL * I3 * (WW / 3)
    # YYI = gamma * gamma * I  # TODO

    # ---------------------------- plots----------------------------

    return {
        "Freqs": FreqRange.tolist(),
        "Alpha": a,
        "Beta": Floquet_line.unfold(beta),
        "r": r,
        "x": x
    }
