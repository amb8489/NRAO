'''
Testing file for calculating A B R X
'''
import numpy as np
from Fluqet_Line_Equations.MicroStrip.FloquetLine import SuperConductingFloquetLine
from Inputs.MicroStripInputs import MicroStripInputs
from SuperConductivityEquations.SCE import SuperConductivity
from TransmissionLineEquations.MicroStrip.SC_MicroStrip_TL import SuperConductingMicroStripModel

# ---------------------------- unit cell inputs from paper
MSinputs = MicroStripInputs()


def simulate():
    # ---------------------------- inputs ----------------------------
    MSinputs = MicroStripInputs()

    # ---------------------------- dependency models ----------------------------
    super_conductivity_model = SuperConductivity(MSinputs.op_temp, MSinputs.crit_temp, MSinputs.normal_resistivity)
    Central_line_model = SuperConductingMicroStripModel(MSinputs.height, MSinputs.central_line_width,
                                                        MSinputs.line_thickness, MSinputs.er, MSinputs.tangent_delta,
                                                        MSinputs.crit_current)
    Load_line_models = [
        SuperConductingMicroStripModel(MSinputs.height, width, MSinputs.line_thickness, MSinputs.er,
                                       MSinputs.tangent_delta,
                                       MSinputs.crit_current) for width in MSinputs.load_widths]
    Floquet_line = SuperConductingFloquetLine(MSinputs.unit_cell_length, MSinputs.D0, MSinputs.load_lengths,
                                              Load_line_models,
                                              Central_line_model,
                                              super_conductivity_model, MSinputs.central_line_width,
                                              MSinputs.load_widths,
                                              MSinputs.line_thickness, MSinputs.crit_current)

    # ---------------------------- calculations -------------------
    a, r, x, beta, betaUf, freqs, RR, LL, GG, CC, gamma, transmission = [], [], [], [], [], [], [], [], [], [], [], []
    FRange = np.linspace(MSinputs.start_freq_GHz, MSinputs.end_freq_GHz, MSinputs.resoultion)
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
        "freqs": FRange.tolist(),
        "alpha": a
    }
