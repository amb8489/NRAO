'''
Testing file for calculating A B R X
'''
import time

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from Fluqet_Line_Equations.MicroStrip.FloquetLine import SuperConductingFloquetLine
from Inputs.MicroStripInputs import MicroStripInputs
from SuperConductivityEquations.SCE import SuperConductivity
from TransmissionLineEquations.MicroStrip.SC_MicroStrip_TL import SuperConductingMicroStripModel
from Utills.Constants import PI2


# ---------------------------- unit cell inputs from paper


def simulate(model_type, inputs):
    if model_type == "MS":
        pass
    elif model_type == "CPW":
        pass
    else:
        return f"unknown model type {model_type}"

    # ---------------------------- dependency models ----------------------------
    super_conductivity_model = SuperConductivity(inputs.op_temp, inputs.crit_temp, inputs.normal_resistivity)
    Central_line_model = SuperConductingMicroStripModel(inputs.height, inputs.central_line_width,
                                                        inputs.line_thickness, inputs.er, inputs.tangent_delta,
                                                        inputs.crit_current)
    Load_line_models = [
        SuperConductingMicroStripModel(inputs.height, width, inputs.line_thickness, inputs.er,
                                       inputs.tangent_delta,
                                       inputs.crit_current) for width in inputs.load_widths]
    floquet_line = SuperConductingFloquetLine(inputs.unit_cell_length, inputs.D0, inputs.load_lengths,
                                              Load_line_models,
                                              Central_line_model,
                                              super_conductivity_model, inputs.central_line_width,
                                              inputs.load_widths,
                                              inputs.line_thickness, inputs.crit_current)

    # ---------------------------- calculations -------------------
    alpha_plt, r, x, beta_plt, beta_unfold_plt, RR, LL, GG, CC, gamma, transmission_plt = [], [], [], [], [], [], [], [], [], [], []
    FRange = np.linspace(inputs.start_freq_GHz, inputs.end_freq_GHz, inputs.resoultion)
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

    plot_width = 1
    plot_height = 1
    dpi = 100

    fig1 = Figure(figsize=(plot_width, plot_height), dpi=dpi)
    axes1 = fig1.add_subplot(111)
    fig1.suptitle("ALPHAS")
    axes1.set_xlabel('Frequency [GHz]')
    axes1.set_ylabel('Frequency [GHz]')
    axes1.plot(FRange, alpha_plt)

    floquet_line.FindPumpZone(3, alpha_plt)
    axes1.axvspan(FRange[int(floquet_line.target_pump_zone_start)], FRange[int(floquet_line.target_pump_zone_end)],
                  facecolor='b', alpha=0.3)
    axes1.axvspan(FRange[int(floquet_line.target_pump_zone_start / 3)],
                  FRange[int(floquet_line.target_pump_zone_end / 3)],
                  facecolor='g', alpha=0.5)

    fig2 = Figure(figsize=(plot_width, plot_height), dpi=dpi)
    axes2 = fig2.add_subplot(111)
    fig2.suptitle("BETAS")
    axes2.set_xlabel('Frequency [GHz]')
    axes2.set_ylabel('Frequency [GHz]')
    axes2.plot(FRange, beta_plt)
    axes2.plot(FRange, floquet_line.unfold(beta_plt))

    fig3 = Figure(figsize=(plot_width, plot_height), dpi=dpi)
    axes3 = fig3.add_subplot(111)
    fig3.suptitle("R")
    axes3.set_xlabel('Frequency [GHz]')
    axes3.set_ylabel('Frequency [GHz]')
    axes3.plot(FRange, r)

    fig4 = Figure(figsize=(plot_width, plot_height), dpi=dpi)
    axes4 = fig4.add_subplot(111)
    fig4.suptitle("X")
    axes4.set_xlabel('Frequency [GHz]')
    axes4.set_ylabel('Frequency [GHz]')
    axes4.plot(FRange, x)

    fig5 = Figure(figsize=(plot_width, plot_height), dpi=dpi)
    axes5 = fig5.add_subplot(111)
    fig5.suptitle("TRANSMISSION")
    axes5.set_xlabel('Frequency [GHz]')
    axes5.set_ylabel('Frequency [GHz]')
    axes5.plot(FRange, transmission_plt)

    # todo
    fig6 = Figure(figsize=(plot_width, plot_height), dpi=dpi)
    axes6 = fig6.add_subplot(111)
    fig6.suptitle("CIRCUIT")
    axes6.set_xlabel('Frequency [GHz]')
    axes6.set_ylabel('Frequency [GHz]')
    axes6.plot(FRange, FRange)

    return [[fig1, fig2], [fig3, fig4], [fig5, fig6]]

    # return {
    #     "freqs": FRange.tolist(),
    #     "alpha": [alpha_plt],
    #     "beta_plt": [beta_plt],
    #     "r": [r],
    #     "x": [x],
    #
    #     "transmission_plt": [transmission_plt],
    #     "circuit": [CLWWI, CRwI, GLwI, RGI, GLIIIwDiv3, CLIIIWWDiv3, YYI],
    #
    #     "target_pump_zone_start": [floquet_line.target_pump_zone_start],
    #     "target_pump_zone_end": [floquet_line.target_pump_zone_end],
    # }
